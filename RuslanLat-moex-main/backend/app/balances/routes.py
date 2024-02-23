import typing

from app.balances.views import (
    BalanceAddView,
    BalanceListView,
    BalanceUpdateView,
    BalanceView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/balance.add", BalanceAddView)
    app.router.add_view("/balance.update", BalanceUpdateView)
    app.router.add_view("/balance.list", BalanceListView)
    app.router.add_view("/balance.user", BalanceView)
