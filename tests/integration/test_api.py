from fastapi.testclient import TestClient

from app.interfaces.api import create_app


def test_upload_returns_reviewable_order_draft():
    app = create_app(
        extractor=lambda _: """Supplier: Acme Supplies
Quotation No: Q-2026-001
Currency: EUR
Item: Lenovo Laptop | Qty: 5 | Unit Price: 1200.00 | Line Total: 6000.00
Total: 6000.00
"""
    )

    response = TestClient(app).post(
        "/api/order-drafts",
        files={"file": ("quote.pdf", b"%PDF-1.4", "application/pdf")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "NEEDS_REVIEW"
    assert body["quotation"]["supplier_name"] == "Acme Supplies"
    assert body["quotation"]["items"][0]["quantity"] == 5
    assert body["submitted"] is False


def test_upload_rejects_non_pdf():
    client = TestClient(create_app())

    response = client.post(
        "/api/order-drafts",
        files={"file": ("quote.txt", b"not a pdf", "text/plain")},
    )

    assert response.status_code == 415


def test_upload_page_serves_the_demo_shell_and_static_assets():
    client = TestClient(create_app())

    page = client.get("/")
    stylesheet = client.get("/static/styles.css")
    script = client.get("/static/app.js")

    assert page.status_code == 200
    assert "From supplier PDF" in page.text
    assert 'data-upload-form' in page.text
    assert stylesheet.status_code == 200
    assert "--green" in stylesheet.text
    assert script.status_code == 200
    assert "showFile" in script.text
