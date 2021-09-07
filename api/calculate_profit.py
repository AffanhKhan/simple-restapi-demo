from api.document import CalculatorEvent, crypto_prices
from python.pydantic import ValidationError
import json

def handler(event, context):
    """
    Calculates profit given a crypto ticker, amount and year in past

    sample event => {"query":"btc", "amount":100, "year":2014}

    Supported crypto queries: btc, eth
    """
    try:
        parsed_event = CalculatorEvent(**event)
    except ValidationError as exp:
        raise Exception(json.dumps(f"[BadRequest] {exp}"))

    if parsed_event.year not in crypto_prices[parsed_event.query]['old_prices']:
        raise Exception(json.dumps(f"[BadRequest] Data for requested year not available"))


    current_value = (parsed_event.amount/crypto_prices[parsed_event.query]['old_prices'][parsed_event.year]) * crypto_prices[parsed_event.query]['current_price']
    
    return round(current_value,2)
    