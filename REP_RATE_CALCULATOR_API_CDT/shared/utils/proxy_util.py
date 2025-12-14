import json

class ProxyUtil:
    @staticmethod
    def create_response(status_code, body):
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(body)
        }
    
    def extract_client_info(event):
        headers = event.get("headers", {})
        ip_address = headers.get("X-Forwarded-For") or \
                    event.get("requestContext", {}).get("identity", {}).get("sourceIp", "unknown")
        user_agent = headers.get("User-Agent") or headers.get("user-agent") or "unknown"

        return {"ip": ip_address, "user_agent": user_agent}