from pydantic import BaseModel, model_validator
from e5lib.funcs import phone_purge

from ..filters import filter_full_name


class Customer(BaseModel):

    phone: str | None = None
    name: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate(cls, data: dict) -> dict:
        if not data.get("phone"):
            phone = data.get("PHONE")
            if phone:
                phone = phone[0].get("VALUE", None)
                phone = phone_purge(phone)
                data["phone"] = phone
        if not data.get("name"):
            name = data.get("NAME")
            if name:
                data["name"] = filter_full_name(data.get("NAME"))
        name = data.get("name")
        if name and isinstance(name, str):
            data["name"] = name.strip()
        return data
