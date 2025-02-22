from bot.handlers.products import router as products_router
from bot.handlers.common import router as common_router
from bot.handlers.commands import router as commands_router

routers = [commands_router, products_router, common_router]