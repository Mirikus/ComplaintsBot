from config import DATABASE_URL


TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.database.models"],
            "default_connection": "default",
        }
    }
}
