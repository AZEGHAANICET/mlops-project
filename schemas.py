from pydantic import BaseModel, Field


class IrisInput(BaseModel):
    sepal_length: float = Field(..., ge=0, le=20, description="Sepal length in cm")
    sepal_width: float = Field(..., ge=0, le=20, description="Sepal width in cm")
    petal_length: float = Field(..., ge=0, le=20, description="Petal length in cm")
    petal_width: float = Field(..., ge=0, le=20, description="Petal width in cm")

    class Config:
        json_schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }