from typing import List, Optional
from decimal import *
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.metrics.schemes import (
    MetricRequestSchema,
    MetricResponseSchema,
    MetricListResponseSchema,
    MetricUpdateRequestSchema,
    MetricJoinListResponseSchema,
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.metrics.models import Metric, MetricTotalJoin
from app.tiskers.models import Tisker

getcontext().prec = 2


class MetricAddView(AuthUserRequiredMixin, View):
    @request_schema(MetricRequestSchema)
    @response_schema(MetricResponseSchema, 200)
    @docs(
        tags=["metrics"],
        summary="Add metric add view",
        description="Add metric to database",
    )
    async def post(self) -> Response:
        tisker: str = self.data["tisker"]
        tisker: Tisker = await self.store.tiskers.get_by_tisker(tisker=tisker)
        tisker_id: int = tisker.id
        value: Decimal = self.data["value"]
        delta: Decimal = self.data["delta"]

        try:
            metric: Metric = await self.store.metrics.create_metric(
                tisker_id=tisker_id, value=value, delta=delta
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=MetricResponseSchema().dump(metric))


class MetricUpdateView(AuthUserRequiredMixin, View):
    @request_schema(MetricUpdateRequestSchema)
    @response_schema(MetricResponseSchema, 200)
    @docs(
        tags=["metrics"],
        summary="Add metric update view",
        description="Update metric in database",
    )
    async def put(self) -> Response:
        tisker: str = self.data["tisker"]
        tisker: Tisker = await self.store.tiskers.get_by_tisker(tisker=tisker)
        tisker_id: int = tisker.id
        value: Decimal = self.data["value"]
        delta: Decimal = self.data["delta"]

        try:
            metric: Metric = await self.store.metrics.update_metric(
                tisker_id=tisker_id, value=value, delta=delta
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=MetricResponseSchema().dump(metric))


class MetricListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @response_schema(MetricListResponseSchema, 200)
    @docs(
        tags=["metrics"],
        summary="Add metric list view",
        description="Get list metrics from database",
    )
    async def get(self) -> Response:
        metrics: Optional[List[Metric]] = await self.store.metrics.list_metrics()
        return json_response(MetricListResponseSchema().dump({"metrics": metrics}))
    

class MetricJoinListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @response_schema(MetricJoinListResponseSchema, 200)
    @docs(
        tags=["metrics"],
        summary="Add metric join list view",
        description="Get list metric join from database",
    )
    async def get(self) -> Response:
        metrics: Optional[
            List[MetricTotalJoin]
        ] = await self.store.metrics.list_metrics_join()
        return json_response(
            MetricJoinListResponseSchema().dump({"metrics": metrics})
        )
