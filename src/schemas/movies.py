from datetime import date
from typing import List, Optional, Any, Annotated

from pydantic import BaseModel, ConfigDict, BeforeValidator


def coerce_to_int(variable: Any) -> Any:
    if isinstance(variable, (float, str)) and variable:
        return int(float(variable))
    return variable


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: Annotated[int, BeforeValidator(coerce_to_int)]
    revenue: Annotated[int, BeforeValidator(coerce_to_int)]
    country: str

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int

    model_config = ConfigDict(from_attributes=True)
