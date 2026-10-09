from collections.abc import Callable

from app.domain.models import OrderDraft, draft_from_extraction


def create_order_draft(
    text: str, parser: Callable[[str], object]
) -> OrderDraft:
    extraction = parser(text)
    return draft_from_extraction(extraction)
