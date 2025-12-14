from shared.utils.proxy_util import ProxyUtil
from shared.utils.financial_utils import FinancialUtil
from decimal import Decimal, getcontext
import json

def lambda_handler(event, context):
    try:
        try:
            if 'body' in event:
                request_body = json.loads(event['body'])    
            else:
                request_body = event 
                
        except json.JSONDecodeError:
            return ProxyUtil.create_response(400, {'error': 'Invalid JSON in request body.'})

        aer_str = request_body.get('annual_effective_rate')
        frequency_str = request_body.get('period_frequency')
        
        if not aer_str or not frequency_str:
            return ProxyUtil.create_response(400, {'error': 'Missing required parameters: annual_effective_rate and period_frequency.'})

        try:
            aer_decimal = Decimal(aer_str)
            period_frequency = int(frequency_str)
            
            if period_frequency <= 0:
                 raise ValueError("Period frequency must be a positive integer.")
            
        except Exception as e:
             return ProxyUtil.create_response(400, {'error': f'Error in parameter format or value: {str(e)}'})

        period_rate_result = FinancialUtil.calcular_tasa_vencida(aer_decimal, period_frequency)
        rate_percentage = period_rate_result * Decimal(100)
        
        return ProxyUtil.create_response(200, {
            'annual_effective_rate_used': str(aer_decimal),
            'period_frequency': period_frequency,
            'calculated_period_rate_decimal': str(period_rate_result),
            'calculated_period_rate_percentage': f"{rate_percentage.quantize(Decimal('0.0001'))}%"
        })

    except Exception as e:
        return ProxyUtil.create_response(500, {'error': f'Internal server error: {str(e)}'})