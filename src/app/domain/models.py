from dataclasses import dataclass, field


@dataclass
class QuotationItem:
    product_description: str
    quantity: int
    unit_price: float
    line_total: float | None = None


@dataclass
class Quotation:
    supplier_name: str | None
    reference: str | None
    currency: str | None
    items: list[QuotationItem] = field(default_factory=list)
    total_amount: float | None = None


@dataclass
class ExtractionResult:
    quotation: Quotation
    warnings: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)


@dataclass
class OrderDraft:
    quotation: Quotation
    warnings: list[str]
    missing_fields: list[str]
    status: str = "NEEDS_REVIEW"
    submitted: bool = False


def draft_from_extraction(result: ExtractionResult) -> OrderDraft:
    return OrderDraft(
        quotation=result.quotation,
        warnings=result.warnings,
        missing_fields=result.missing_fields,
    )
