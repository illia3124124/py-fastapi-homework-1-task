from __future__ import annotations

import datetime

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class MovieDetailResponseSchema(BaseModel):
    id: int = Field(..., gt=0, description="Database primary key")
    name: str = Field(..., max_length=255, description="Movie title")
    date: datetime.date = Field(..., description="Release date")
    score: float = Field(..., ge=0.0, le=100.0, description="Rating (0-100)")
    genre: str = Field(..., max_length=255, description="Primary genre")
    overview: str = Field(..., description="Short synopsis")
    crew: str = Field(..., description="Crew list or JSON string")
    orig_title: str = Field(..., max_length=255, description="Original title")
    status: str = Field(..., max_length=50, description="Release status")
    orig_lang: str = Field(..., max_length=50, description="Original language code")
    budget: float = Field(..., ge=0, description="Budget in currency units")
    revenue: float = Field(..., ge=0, description="Revenue in currency units")
    country: str = Field(..., min_length=2, max_length=3, description="Country code (ISO) or name")

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema] = Field(..., description="Movies on the current page")
    prev_page: Optional[str] = Field(None, description="URL or relative path to the previous page, or null if none")
    next_page: Optional[str] = Field(None, description="URL or relative path to the next page, or null if none")
    total_pages: int = Field(..., ge=0, description="Total number of pages")
    total_items: int = Field(..., ge=0, description="Total number of items")

    model_config = ConfigDict(from_attributes=True)
