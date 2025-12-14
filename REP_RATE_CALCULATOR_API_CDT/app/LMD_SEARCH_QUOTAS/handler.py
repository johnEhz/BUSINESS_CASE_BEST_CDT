"""Lambda getBankQuotas: retorna las cuotas/tasas disponibles por banco para un monto y plazo específicos."""
from shared.utils.proxy_util import ProxyUtil
from shared.utils.financial_utils import FinancialUtil
from shared.repository.rates_repo import RatesReporistory
from decimal import Decimal
import json

rates_repo = RatesReporistory()

def lambda_handler(event, context):

    try:
        if 'body' in event:
            try:
                request_body = json.loads(event['body'])
            except json.JSONDecodeError:
                return ProxyUtil.create_response(400, {'error': 'Invalid JSON in request body'})
        else:
            request_body = event

        amount_str = request_body.get('amount')
        term_days_str = request_body.get('term_in_days')
        
        if not amount_str or not term_days_str:
            return ProxyUtil.create_response(400, {'error': 'Missing required parameters: amount and term_in_days.'})

        try:
            investment_amount = Decimal(amount_str)
            term_in_days = int(term_days_str)
            
            if investment_amount <= 0 or term_in_days <= 0:
                 raise ValueError("Amounts and term must be positive.")
            
        except Exception as e:
             return ProxyUtil.create_response(400, {'error': f'Error in parameter format or value: {str(e)}'})

        bank_rates = rates_repo.get_rates_by_terms_and_amount(term_in_days, float(investment_amount))

        return ProxyUtil.create_response(200, {
            'investment_summary': {
                'amount': str(investment_amount),
                'term_days': term_in_days
            },
            'bank_rates': bank_rates
        })

    except Exception as e:
        return ProxyUtil.create_response(500, {'error': f'Internal server error during processing: {str(e)}'})