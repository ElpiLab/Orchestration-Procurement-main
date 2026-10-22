from fastapi.testclient import TestClient

from app.interfaces.api import create_app


def test_ui_contract_preserves_shared_shell_and_draftroom_hooks():
    page = TestClient(create_app()).get("/").text

    required = (
        "From supplier PDF",
        "to a draft worth reviewing.",
        "Human in the loop",
        "PROCESSING LOCAL",
        "data-upload-card",
        "data-upload-form",
        'id="quotation-file"',
        'id="instructions"',
        "Drop a quotation PDF here",
        "OPTIONAL INSTRUCTIONS",
        "Create internal draft",
        "EXTRACTION RESULT",
        "Ready for human review",
        "NEEDS_REVIEW",
        "Validation notes",
        "Fields to verify",
        "NEXT ACTIONS",
        "data-review-field",
        "data-action-feedback",
        "This is an internal draft. It has not been submitted to a supplier.",
    )
    assert all(value in page for value in required)
    assert page.count("<th>") == 8
    assert 'data-role="all"' in page
    assert 'data-role="user"' in page
    assert 'data-role="procurement"' in page


def test_ui_contract_preserves_user_and_procurement_surfaces():
    client = TestClient(create_app())
    user_page = client.get("/user").text
    procurement_page = client.get("/procurement").text

    assert all(
        value in user_page
        for value in (
            "Internal Draft",
            "Your requests at a glance",
            "Requests sent",
            "Requests needing changes",
            "Continue a draft",
            "View draft queue →",
            "user-stat-row",
        )
    )
    assert all(
        value in procurement_page
        for value in (
            "Review queue",
            "Order overview",
            "DEMO QUEUE · LOCAL ONLY",
            "Orders today",
            "Pending review",
            "Validated",
            "Total value",
            'data-queue-filter="all"',
            'data-queue-filter="pending"',
            'data-queue-filter="validated"',
            "data-queue-rows",
            "data-request-status",
            "simulated email notification",
        )
    )


def test_ui_contract_preserves_javascript_hooks_and_state_classes():
    client = TestClient(create_app())
    script = client.get("/static/app.js").text
    stylesheet = client.get("/static/styles.css").text

    for hook in (
        "is-dragging",
        "is-warning",
        "is-complete",
        "row-status--validated",
        "row-status--rejected",
        "row-status--warning",
        "queue-badge--pending",
        "queue-badge--validated",
        "queue-badge--rejected",
        "queue-tab--active",
        "Extracting quotation...",
        "showFile",
    ):
        assert hook in script
    for token in (
        "--ink",
        "--muted",
        "--paper",
        "--panel",
        "--panel-soft",
        "--green",
        "--blue",
        "--amber",
    ):
        assert token in stylesheet
    assert "Space Grotesk" in stylesheet
    assert "DM Mono" in stylesheet
