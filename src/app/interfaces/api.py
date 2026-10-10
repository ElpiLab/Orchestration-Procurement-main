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
USER_TEMPLATE_PATH = INTERFACES_DIR / "templates" / "user.html"
PROCUREMENT_TEMPLATE_PATH = INTERFACES_DIR / "templates" / "procurement.html"


def create_app(extractor: Callable[[bytes], str] | None = None) -> FastAPI:
    app = FastAPI(title="procAi")
    pdf_extractor = extractor or extract_text_from_pdf
    app.mount("/static", StaticFiles(directory=INTERFACES_DIR / "static"), name="static")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return _render_page("upload")

    @app.get("/user", response_class=HTMLResponse)
    def user_view() -> str:
        return _render_user_page()

    @app.get("/procurement", response_class=HTMLResponse)
    def procurement_view() -> str:
        return _render_procurement_page()

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
        '<tr data-review-row>'
        f'<td><strong>{escape(str(quotation.get("supplier_name") or "Not found"))}</strong>'
        '<small class="row-muted">Supplier from quotation</small></td>'
        f"<td>{escape(str(item['product_description']))}</td>"
        f"<td>{item['quantity']}</td>"
        f"<td>{_money(item['unit_price'], quotation.get('currency'))}</td>"
        f"<td>{_money(item.get('line_total'), quotation.get('currency'))}</td>"
        '<td><select class="table-select" aria-label="Supplier onboarded status" data-onboarded>'
        '<option value="">Check</option><option value="yes">Yes</option><option value="no">No</option>'
        '</select></td>'
        '<td><input class="table-input" type="text" placeholder="CC-4100" aria-label="Cost center"></td>'
        '<td><span class="row-status" data-row-status>Pending</span>'
        '<div class="row-actions"><button type="button" class="mini-button mini-button--approve" data-row-action="validate">✓</button>'
        '<button type="button" class="mini-button mini-button--reject" data-row-action="reject">×</button></div></td>'
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
        "{{MODE}}": "quotation intake" if mode == "upload" else "internal draft",
        "{{SUPPLIER}}": escape(str(quotation.get("supplier_name") or "Not found")),
        "{{REFERENCE}}": escape(str(quotation.get("reference") or "Not found")),
        "{{CURRENCY}}": escape(str(quotation.get("currency") or "—")),
        "{{TOTAL}}": _money(quotation.get("total_amount"), quotation.get("currency")),
        "{{ITEM_ROWS}}": item_rows or (
            '<tr><td colspan="8" class="empty-state">No line items extracted.</td></tr>'
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


def _render_user_page() -> str:
    return USER_TEMPLATE_PATH.read_text(encoding="utf-8")


def _render_procurement_page() -> str:
    template = PROCUREMENT_TEMPLATE_PATH.read_text(encoding="utf-8")
    rows = [
        ("PR-1042", "Helvetic Office Supplies AG", "Ergonomic office chair", "8", "CHF 465.00", "CHF 3,720.00", "Pending", "CC-4100"),
        ("PR-1041", "Alpine IT Solutions GmbH", "Lenovo ThinkPad T14", "4", "CHF 1,690.00", "CHF 6,760.00", "Validated", "CC-2200"),
        ("PR-1040", "Bern Lab Equipment AG", "Precision laboratory scale", "2", "CHF 967.50", "CHF 1,935.00", "Validated", "CC-3100"),
        ("PR-1039", "Rhone Consulting Sarl", "Procurement process workshop", "1", "CHF 4,280.00", "CHF 4,280.00", "Pending", "Missing"),
    ]
    row_content = "".join(
        f'<tr data-review-row><td><strong>{reference}</strong><small class="row-muted">{supplier}</small></td>'
        f"<td>{description}</td><td>{quantity}</td><td>{unit_price}</td><td>{line_total}</td>"
        f'<td><span class="queue-badge queue-badge--{"validated" if status == "Validated" else "pending"}">{status}</span></td>'
        f'<td>{cost_center}</td><td data-request-status="{status.lower()}"><span class="row-status" data-row-status>{status}</span>'
        '<div class="row-actions"><button type="button" class="mini-button mini-button--approve" data-row-action="validate" aria-label="Validate request">✓</button>'
        '<button type="button" class="mini-button mini-button--reject" data-row-action="reject" aria-label="Reject request">×</button></div></td></tr>'
        for reference, supplier, description, quantity, unit_price, line_total, status, cost_center in rows
    )
    return template.replace("{{REQUEST_ROWS}}", row_content)


def _render_role_placeholder(role: str) -> str:
    label = escape(role.upper())
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>procAi / {label}</title>"
        "<link rel=\"stylesheet\" href=\"/static/styles.css\"></head>"
        f"<body class=\"role-placeholder\"><main><p class=\"eyebrow\">PROCAI WORKSPACE</p>"
        f"<h1>{label} view</h1><p>This workspace is reserved for the procurement team demo.</p>"
        "<a class=\"button button--primary\" href=\"/\">Back to all</a></main></body></html>"
    )
