from pricing.pricing_strategy import PricingStrategy
from decimal import Decimal

class StandardPricing(PricingStrategy):
    """
    <<Concrete Strategy>>
    Standard pricing with no discounts or surcharges.
    """
    def compute_price(self, product_id: str, base_price: float) -> Decimal:
        return Decimal(str(base_price)).quantize(Decimal("0.01"))

    @property
    def strategy_name(self) -> str:
        return "STANDARD"
