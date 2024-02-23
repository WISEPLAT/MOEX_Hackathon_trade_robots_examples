import typing

from app.tiskers.views import (
    TiskerAddView,
    TiskerListView,
    TiskerUpdateView,
    TiskerDeleteView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/tisker.add", TiskerAddView)
    app.router.add_view("/tisker.update", TiskerUpdateView)
    app.router.add_view("/tisker.delete", TiskerDeleteView)
    app.router.add_view("/tisker.list", TiskerListView)