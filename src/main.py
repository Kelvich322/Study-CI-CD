from typing import Dict, List, Sequence

from fastapi import FastAPI, HTTPException, Path, status, Depends
from sqlalchemy import asc, desc
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from .database import engine, get_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.get("/recipes/", response_model=List[schemas.RecipeLite])
async def recipes(db: AsyncSession = Depends(get_db)) -> Sequence[models.Recipe]:
    res = await db.execute(
        select(models.Recipe).order_by(
            desc(models.Recipe.views), asc(models.Recipe.cook_time)
        )
    )
    return res.scalars().all()


@app.get(
    "/recipes/{id}",
    response_model=schemas.FullRecipe,
    responses={
        404: {
            "model": Dict[str, str],
            "description": "Рецепт не найден",
            "content": {
                "application/json": {"example": {"detail": "Рецепт не найден"}}
            },
        }
    },
)
async def recipe(
    id: int = Path(..., title="Id of recipe", ge=0), db: AsyncSession = Depends(get_db)
) -> models.Recipe:
    try:
        res = await db.execute(
            select(models.Recipe).filter(models.Recipe.id == id).with_for_update()
        )
        recipe = res.scalars().one()
        recipe.views += 1
        await db.commit()
        return recipe
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Рецепт не найден")


@app.post(
    "/recipes/", response_model=schemas.FullRecipe, status_code=status.HTTP_201_CREATED
)
async def add_recipe(
    recipe: schemas.RecipeIn, db: AsyncSession = Depends(get_db)
) -> models.Recipe:
    new_recipe = models.Recipe(**recipe.model_dump())
    db.add(new_recipe)
    await db.commit()
    return new_recipe
