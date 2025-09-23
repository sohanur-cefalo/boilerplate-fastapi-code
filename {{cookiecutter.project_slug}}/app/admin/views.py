from typing import Optional
from sqladmin import ModelView

# Import models conditionally
try:
    from app.models import User  # type: ignore
except Exception:
    User = None  # type: ignore


class _BaseView(ModelView):
    page_size = 50


# Example: only registered if User exists
if User is not None:
    class UserAdmin(_BaseView, model=User):  # type: ignore
        name = "User"
        name_plural = "Users"
        # Safe defaults; columns resolved by SQLAdmin
        column_searchable_list = ["name", "email"]
        column_sortable_list = ["id", "name", "email", "created_at"]
        column_list = ["id", "name", "email", "is_active", "created_at"]


def register_custom_model_views(admin) -> None:
    """Register hand-crafted ModelViews here.

    Add your custom ModelViews and register them via `admin.add_view(YourView)`.
    """
    if User is not None:
        admin.add_view(UserAdmin)
