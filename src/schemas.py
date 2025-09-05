from pydantic import BaseModel


class FullRecipe(BaseModel):
    title: str
    cook_time: int
    ingredients: str
    description: str


class RecipeIn(FullRecipe): ...


class RecipeOut(FullRecipe):
    id: int

    class Config:
        orm_mode = True


class RecipeLite(BaseModel):
    id: int
    title: str
    cook_time: int
    views: int
