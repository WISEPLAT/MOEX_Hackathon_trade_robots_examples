import typing

from app.briefcases.views import (
    BriefcaseAddView,
    BriefcaseListView,
    BriefcaseTotalUpdateView,
    BriefcaseTotalAddView,
    BriefcaseTotalListView,
    BriefcaseTotalJoinListView,
    BriefcaseJoinListView
    # BriefcaseDeleteView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/briefcase.add", BriefcaseAddView)
    app.router.add_view("/briefcase.total.add", BriefcaseTotalAddView)
    app.router.add_view("/briefcase.total.update", BriefcaseTotalUpdateView)
    app.router.add_view("/briefcase.total.join.list", BriefcaseTotalJoinListView)
    app.router.add_view("/briefcase.list", BriefcaseListView)
    app.router.add_view("/briefcase.join.list", BriefcaseJoinListView)
    app.router.add_view("/briefcase.total.list", BriefcaseTotalListView)
