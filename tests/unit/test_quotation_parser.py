from app.infrastructure.quotation_parser import parse_quotation_text


def test_parses_quotation_header_items_and_total():
    text = """Supplier: Acme Supplies
Quotation No: Q-2026-001
Currency: EUR
Item: Lenovo Laptop | Qty: 5 | Unit Price: 1200.00 | Line Total: 6000.00
Total: 6000.00
"""

    result = parse_quotation_text(text)

    assert result.quotation.supplier_name == "Acme Supplies"
    assert result.quotation.reference == "Q-2026-001"
    assert result.quotation.currency == "EUR"
    assert result.quotation.items[0].product_description == "Lenovo Laptop"
    assert result.quotation.items[0].quantity == 5
    assert result.quotation.items[0].unit_price == 1200.0
    assert result.quotation.total_amount == 6000.0
    assert result.warnings == []


def test_reports_missing_fields_and_inconsistent_total():
    text = """Supplier: Acme Supplies
Item: Lenovo Laptop | Qty: 2 | Unit Price: 100.00
Total: 250.00
"""

    result = parse_quotation_text(text)

    assert "quotation_reference" in result.missing_fields
    assert "currency" in result.missing_fields
    assert any("does not match" in warning for warning in result.warnings)
