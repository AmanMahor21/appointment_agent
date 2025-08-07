from .agent_route import router as telegram_webhook


def register_routes(app):
    app.include_router(telegram_webhook)
