from tortoise import Tortoise


async def setup_db():
    await Tortoise.init(
        db_url='sqlite://database/db.sqlite3',
        modules={'models': ['database.models']}
    )
    await Tortoise.generate_schemas(safe=True)


async def main():
    await setup_db()