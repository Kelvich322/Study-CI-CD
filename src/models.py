import asyncio
import logging

from sqlalchemy import Column, Integer, String

from .database import Base, async_session, engine

logging.basicConfig(level=logging.INFO)


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String(256), index=True, nullable=False)
    cook_time = Column(Integer, index=True, nullable=False)
    views = Column(Integer, index=True, default=0)
    ingredients = Column(String, nullable=False)
    description = Column(String)


async def fill_test_data(Base, session, engine) -> None:
    """
    Заполняет ДБ тестовыми данными
    """
    recipes = [
        Recipe(
            title="Спагетти Карбонара",
            cook_time=20,
            ingredients="Спагетти, яйца, бекон, пармезан, чеснок, соль, перец",
            description="Классическая итальянская паста с беконом и соусом из яиц и сыра.",
        ),
        Recipe(
            title="Овсянка с ягодами",
            cook_time=10,
            ingredients="Овсяные хлопья, молоко/вода, мед, клубника, черника",
            description="Полезный завтрак с овсянкой и свежими ягодами.",
        ),
        Recipe(
            title="Греческий салат",
            cook_time=15,
            ingredients="Помидоры, огурцы, красный лук, оливки, сыр фета, оливковое масло, лимонный сок",
            description="Освежающий салат в средиземноморском стиле.",
        ),
        Recipe(
            title="Шоколадный мусс",
            cook_time=30,
            ingredients="Темный шоколад, сливки, сахар, яйца",
            description="Нежный десерт с насыщенным шоколадным вкусом.",
        ),
        Recipe(
            title="Куриный суп с лапшой",
            cook_time=40,
            ingredients="Куриная грудка, лапша, морковь, лук, сельдерей, зелень, соль, перец",
            description="Ароматный домашний суп, идеальный для холодного дня.",
        ),
    ]
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        session.add_all(recipes)
        await session.commit()

    logging.info("Тестовые данные успешно добавлены")


if __name__ == "__main__":

    async def main():
        async with async_session() as session:
            await fill_test_data(Base, session, engine)

    asyncio.run(main())
