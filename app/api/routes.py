from fastapi import APIRouter
from .endpoints import news, stocks, analysis, watchlist, users

# Create main router
router = APIRouter()

# Include all endpoint routers
router.include_router(
    news.router,
    prefix="/news",
    tags=["news"],
    responses={
        200: {"description": "Success"},
        500: {"description": "Internal server error"}
    }
)

router.include_router(
    stocks.router,
    prefix="/stock-info",
    tags=["stocks"],
    responses={
        200: {"description": "Success"},
        500: {"description": "Internal server error"}
    }
)

# Add analysis router
router.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["analysis"],
    responses={
        200: {"description": "Success"},
        500: {"description": "Internal server error"}
    }
)

# Add watchlist router
router.include_router(
    watchlist.router,
    prefix="/watchlist",
    tags=["watchlist"],
    responses={
        200: {"description": "Success"},
        500: {"description": "Internal server error"}
    }
)

# Add users router
router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    responses={
        200: {"description": "Success"},
        500: {"description": "Internal server error"}
    }
)