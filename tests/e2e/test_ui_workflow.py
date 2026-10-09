from fastapi.testclient import TestClient

from app.interfaces.api import create_app


def test_upload_ui_returns_internal_draft_page():
    app = create_app(
        extractor=lambda _: """Supplier: Acme Supplies
Quotation No: Q-2026-001
Currency: EUR
Item: Lenovo Laptop | Qty: 5 | Unit Price: 1200.00 | Line Total: 6000.00
Total: 6000.00
"""
    )

    client = TestClient(app)
    response = client.post(
        "/order-drafts",
        files={"file": ("quote.pdf", b"%PDF-1.4", "application/pdf")},
    )

    assert response.status_code == 200
    assert "EXTRACTION RESULT" in response.text
    assert "NEEDS_REVIEW" in response.text
    assert "This is an internal draft. It has not been submitted" in response.text
