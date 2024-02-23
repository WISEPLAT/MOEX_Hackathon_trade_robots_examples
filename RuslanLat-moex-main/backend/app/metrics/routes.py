import typing

from app.metrics.views import (
    MetricAddView,
    MetricListView,
    MetricUpdateView,
    MetricJoinListView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application") -> None:
    app.router.add_view("/metric.add", MetricAddView)
    app.router.add_view("/metric.update", MetricUpdateView)
    app.router.add_view("/metric.list", MetricListView)
    app.router.add_view("/metric.join.list", MetricJoinListView)