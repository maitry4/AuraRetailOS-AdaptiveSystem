from pricing.pricing_strategy import PricingStrategy
from decimal import Decimal

class EmergencyPricing(PricingStrategy):
    """
    <<Concrete Strategy>>
    Applies a 50% surcharge to non-essential items, but 0 cost for essentials.
    Note: For this demo, we assume essentials are 'water' and 'first_aid_kit'.
    """
    ESSENTIALS = {"water", "first_aid_kit", "emergency_ration"}

    def compute_price(self, product_id: str, base_price: float) -> Decimal:
        if product_id in self.ESSENTIALS:
            return Decimal("0.00")
        
        surcharged = Decimal(str(base_price)) * Decimal("1.50")
        return surcharged.quantize(Decimal("0.01"))

    @property
    def strategy_name(self) -> str:
        return "EMERGENCY_SURCHARGE"
