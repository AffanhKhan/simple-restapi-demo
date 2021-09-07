from python.pydantic import BaseModel, validator
from typing import Literal

crypto_prices = {'btc': {
    'current_price':50000,
    'old_prices': {
    2011: 0.8,
    2012: 2.5,
    2013: 20,
    2014: 800,
    2015: 250,
    2016: 400,
    2017: 900,
    2018: 14000,
    2019: 3600,
    2020: 8000,
    2021: 36000
}
},
'eth':{
'current_price':4000,
'old_prices':{
    2016: 1,
    2017: 10,
    2018: 1050,
    2019: 120,
    2020: 150,
    2021: 1100
}
}
}

class CalculatorEvent(BaseModel):
    query: Literal[tuple(crypto_prices.keys())]
    amount: float
    year: int

    @validator('amount')
    def amount_check(cls, v):
        if v < 0:
            raise ValueError("amount cannot be negative")
        return v
