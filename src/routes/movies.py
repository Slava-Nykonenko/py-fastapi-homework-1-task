from math import ceil
from typing import Annotated, Any, Sequence

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy import select, func, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import (
    MovieListResponseSchema,
    MovieDetailResponseSchema
)

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movie_list(
        db: Annotated[AsyncSession, Depends(get_db)],
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20)
) -> Sequence[Row[Any] | RowMapping | Any]:
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    total_pages = ceil(total_items / per_page)
    if total_items == 0 or page > total_pages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."

        )
    movies = await db.scalars(
        select(MovieModel).offset((page - 1) * per_page).limit(per_page)
    )

    next_page, prev_page = None, None
    if (page * per_page) < total_items:
        next_page = f"/api/v1/theater/movies/?page={page + 1}&per_page={per_page}"
    if page > 1:
        prev_page = f"/api/v1/theater/movies/?page={page - 1}&per_page={per_page}"

    return {
        "movies": movies.all(),
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_detail(
        db: Annotated[AsyncSession, Depends(get_db)], movie_id: int
):
    movie_db = await db.get(MovieModel, movie_id)
    if not movie_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )
    return movie_db
