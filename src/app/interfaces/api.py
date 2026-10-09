from collections.abc import Callable
from html import escape
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.application.create_order_draft import create_order_draft
from app.infrastructure.pdf_extractor import extract_text_from_pdf
from app.infrastructure.quotation_parser import parse_quotation_text

INTERFACES_DIR = Path(__file__).parent
TEMPLATE_PATH = INTERFACES_DIR / "templates" / "order_drafts.html"


def create_app(extractor: Callable[[bytes], str] | None = None) -> FastAPI:
    app = FastAPI(title="Procurement Orchestration POC")
    pdf_extractor = extractor or extract_text_from_pdf
    app.mount("/static", StaticFiles(directory=INTERFACES_DIR / "static"), name="static")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return _render_page("upload")

    @app.post("/api/order-drafts")
    async def order_draft(
        file: UploadFile = File(...),
        instructions: str = Form(""),
    ) -> dict:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=415, detail="Only PDF files are supported")
        try:
            draft = create_order_draft(
                pdf_extractor(await file.read()),
                parser=lambda text: _parse(text, instructions),
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return _serialize(draft)

    @app.post("/order-drafts", response_class=HTMLResponse)
    async def order_draft_page(
        file: UploadFile = File(...),
        instructions: str = Form(""),
    ) -> str:
        result = await order_draft(file, instructions)
        return _render_page("result", result)

    return app


def _parse(text: str, instructions: str):
    del instructions
    return parse_quotation_text(text)


def _serialize(draft) -> dict:
    quotation = draft.quotation
    return {
        "status": draft.status,
        "submitted": draft.submitted,
        "warnings": draft.warnings,
        "missing_fields": draft.missing_fields,
        "quotation": {
            "supplier_name": quotation.supplier_name,
            "reference": quotation.reference,
            "currency": quotation.currency,
            "total_amount": quotation.total_amount,
            "items": [
                {
                    "product_description": item.product_description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "line_total": item.line_total,
                }
                for item in quotation.items
            ],
        },
    }


app = create_app()


def _render_page(mode: str, result: dict | None = None) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    quotation = (result or {}).get("quotation", {})
    items = quotation.get("items", [])
    warnings = (result or {}).get("warnings", [])
    missing_fields = (result or {}).get("missing_fields", [])

    item_rows = "".join(
        "<tr>"
        f"<td>{escape(str(item['product_description']))}</td>"
        f"<td>{item['quantity']}</td>"
        f"<td>{_money(item['unit_price'], quotation.get('currency'))}</td>"
        f"<td>{_money(item.get('line_total'), quotation.get('currency'))}</td>"
        "</tr>"
        for item in items
    )
    warning_content = "".join(
        f"<li>{escape(str(warning))}</li>" for warning in warnings
    ) or "<li>No validation warnings detected.</li>"
    missing_content = "".join(
        f"<span class=\"tag\">{escape(str(field))}</span>"
        for field in missing_fields
    ) or "<span class=\"tag tag--ok\">All expected fields found</span>"

    replacements = {
        "{{MODE}}": mode,
        "{{SUPPLIER}}": escape(str(quotation.get("supplier_name") or "Not found")),
        "{{REFERENCE}}": escape(str(quotation.get("reference") or "Not found")),
        "{{CURRENCY}}": escape(str(quotation.get("currency") or "—")),
        "{{TOTAL}}": _money(quotation.get("total_amount"), quotation.get("currency")),
        "{{ITEM_ROWS}}": item_rows or (
            '<tr><td colspan="4" class="empty-state">No line items extracted.</td></tr>'
        ),
        "{{WARNINGS}}": warning_content,
        "{{MISSING_FIELDS}}": missing_content,
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


def _money(value: float | None, currency: str | None) -> str:
    if value is None:
        return "Not found"
    return f"{escape(str(currency or ''))} {value:,.2f}".strip()
