from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema | dict)
async def list_movies(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    per_page: int = Query(10, ge=1, le=20, description="Number of items per page"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve a paginated list of movies.

    - **page**: Page number (starting from 1)
    - **page_size**: Number of items per page (max 100)

    Returns a paginated list of movies with metadata about total pages and items.
    """
    total_items_result = await db.execute(select(func.count()).select_from(MovieModel))
    total_items = total_items_result.scalar_one()
    total_pages = (total_items + per_page - 1) // per_page

    if total_items == 0 or page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page
    movies_result = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies = movies_result.scalars().all()

    base_url = "/movies/"
    prev_page_url = f"{base_url}?page={page - 1}&page_size={per_page}" if page > 1 else None
    next_page_url = f"{base_url}?page={page + 1}&page_size={per_page}" if page < total_pages else None
    if len(movies) == 0:
        prev_page_url = None
        next_page_url = None

        return {
            "detail": "No movies found."
        }
    return MovieListResponseSchema.model_validate(
        {
            "movies": movies,
            "prev_page": prev_page_url,
            "next_page": next_page_url,
            "total_pages": total_pages,
            "total_items": total_items,
        }
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_detail(movie_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve detailed information about a specific movie by its ID.

    - **movie_id**: The unique identifier of the movie

    Returns detailed information about the movie,
    including title, release date, score, genre,
    overview, crew, original title, status,
    original language, budget, revenue, and country.
    """
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return MovieDetailResponseSchema.model_validate(movie)
