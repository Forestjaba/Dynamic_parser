from pydantic import BaseModel, root_validator

class Item(BaseModel):
    id: int
    name: str
    salePriceU: float
    brand: str
    sale: int
    rating: int
    volume: int

    @root_validator(pre=True)
    def convert_price(cls, values:dict):
        price = values.get("salePriceU")
        if price is not None:
            values["salePriceU"] = price / 100
        return values

class Items(BaseModel):
    products: list[Item]