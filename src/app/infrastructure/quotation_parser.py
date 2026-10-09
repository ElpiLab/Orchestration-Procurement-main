import re

from app.domain.models import ExtractionResult, Quotation, QuotationItem


def _value(line: str, label: str) -> str | None:
    match = re.search(rf"^{re.escape(label)}\s*:\s*(.+)$", line, re.IGNORECASE)
    return match.group(1).strip() if match else None


def _number(value: str, field: str) -> float:
    try:
        number = float(value.replace(",", "").strip())
    except ValueError as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if number < 0:
        raise ValueError(f"{field} must not be negative")
    return number


def parse_quotation_text(text: str) -> ExtractionResult:
    supplier = reference = currency = None
    total_amount = None
    items: list[QuotationItem] = []
    warnings: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        supplier = supplier or _value(line, "Supplier")
        reference = reference or _value(line, "Quotation No")
        currency = currency or _value(line, "Currency")

        if line.lower().startswith("total:"):
            raw_total = _value(line, "Total")
            if raw_total is not None:
                total_amount = _number(raw_total, "total")
        elif line.lower().startswith("item:"):
            parts = {
                key.strip().lower(): value.strip()
                for key, value in (
                    part.split(":", 1)
                    for part in line.removeprefix("Item:").split("|")
                    if ":" in part
                )
            }
            description = line.removeprefix("Item:").split("|", 1)[0].strip()
            if not description or "qty" not in parts or "unit price" not in parts:
                warnings.append("Item is missing product description, quantity, or unit price")
                continue
            quantity = _number(parts["qty"], "quantity")
            if quantity <= 0 or quantity != int(quantity):
                raise ValueError("quantity must be a positive whole number")
            line_total = (
                _number(parts["line total"], "line total")
                if "line total" in parts
                else None
            )
            items.append(
                QuotationItem(
                    product_description=description,
                    quantity=int(quantity),
                    unit_price=_number(parts["unit price"], "unit price"),
                    line_total=line_total,
                )
            )

    missing_fields = [
        name
        for name, value in (
            ("supplier_name", supplier),
            ("quotation_reference", reference),
            ("currency", currency),
            ("items", items),
            ("total_amount", total_amount),
        )
        if not value
    ]

    calculated_total = sum(
        item.line_total if item.line_total is not None else item.quantity * item.unit_price
        for item in items
    )
    if total_amount is not None and items and abs(calculated_total - total_amount) > 0.01:
        warnings.append(
            f"calculated total {calculated_total:.2f} does not match "
            f"extracted total {total_amount:.2f}"
        )

    return ExtractionResult(
        quotation=Quotation(
            supplier_name=supplier,
            reference=reference,
            currency=currency,
            items=items,
            total_amount=total_amount,
        ),
        warnings=warnings,
        missing_fields=missing_fields,
    )
