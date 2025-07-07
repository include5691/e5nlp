import os
from pydantic import BaseModel, model_validator

from ..filters import filter_text

class Car(BaseModel):

    brand: str | None = None
    model: str | None = None
    year: int | None = None
        
    @model_validator(mode='before')
    @classmethod
    def validate(cls, data: dict) -> dict:
        data["brand"] = filter_text(data.get(os.getenv("BRAND_FIELD")))
        uf_crm_model: str = data.get(os.getenv("MODEL_FIELD"))
        uf_crm_year = data.get(os.getenv("YEAR_FIELD"))
        try:
            uf_crm_year = int(uf_crm_year)
        except:
            uf_crm_year = None
        if uf_crm_model:
            for entry in uf_crm_model.split(" "):
                if len(entry) < 4:
                    continue
                try:
                    uf_crm_year = int(entry)
                    break
                except:
                    continue
            if str(uf_crm_year) in uf_crm_model:
                uf_crm_model = uf_crm_model.replace(str(uf_crm_year), '').strip()
            data["model"] = filter_text(uf_crm_model)
        if uf_crm_year:
            data["year"] = uf_crm_year
        return data

    def get_car_name(self) -> str:
        return f"{self.brand} {self.model} {self.year}".replace("  ", " ").replace('None', '').strip()
