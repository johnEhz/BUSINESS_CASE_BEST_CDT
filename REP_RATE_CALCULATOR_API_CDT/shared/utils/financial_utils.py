import json
from decimal import Decimal, getcontext

getcontext().prec = 20

class FinancialUtil:
    @staticmethod
    def calcular_tasa_vencida(annual_effective_rate: Decimal, period_frequency: int) -> Decimal:
        frequency_decimal = Decimal(period_frequency)
        
        exponent = Decimal(1) / frequency_decimal
        base = Decimal(1) + annual_effective_rate
        equivalent_rate = base ** exponent
        period_rate = equivalent_rate - Decimal(1)

        return period_rate.quantize(Decimal('0.0000000000'))

    def calcular_roi(amount: Decimal, term_days: int, aer: Decimal, base_days_in_year: int) -> Decimal:
        exponent = Decimal(term_days) / base_days_in_year
        base = Decimal(1) + aer
        
        rate_factor = base ** exponent
        interest_factor = rate_factor - Decimal(1)
        total_interest = amount * interest_factor
        
        return total_interest.quantize(Decimal('0.01'))