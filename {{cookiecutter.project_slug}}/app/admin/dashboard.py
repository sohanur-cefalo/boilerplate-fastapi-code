from fastapi import APIRouter

router = APIRouter()


@router.get("/admin/health")
def admin_health():
    return {"status": "ok"}


def register_custom_routes(app):
    """Attach optional custom admin routes (dashboards, charts)."""
    app.include_router(router)
