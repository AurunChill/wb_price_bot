from bot.handlers.products import router as products_router
from bot.handlers.common import router as common_router
from bot.handlers.commands import router as commands_router
from bot.handlers.admin import router as admin_router

routers = [commands_router, products_router, admin_router, common_router]