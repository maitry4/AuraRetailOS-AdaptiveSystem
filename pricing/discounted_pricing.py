from pricing.pricing_strategy import PricingStrategy
from decimal import Decimal

class DiscountedPricing(PricingStrategy):
    """
    <<Concrete Strategy>>
    Applies a fixed 15% discount to all products.
    """
    def compute_price(self, product_id: str, base_price: float) -> Decimal:
        discounted = Decimal(str(base_price)) * Decimal("0.85")
        return discounted.quantize(Decimal("0.01"))

    @property
    def strategy_name(self) -> str:
        return "DISCOUNTED"
