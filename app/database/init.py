from tortoise import Tortoise
from app.database.config import TORTOISE_ORM

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    # await Tortoise.generate_schemas()