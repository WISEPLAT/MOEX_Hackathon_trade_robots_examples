from decimal import *
from typing import List, Optional
from sqlalchemy import func, select, update, delete, and_
from sqlalchemy.orm import joinedload, join

from app.metrics.models import Metric, MetricModel, MetricTotalJoin
from app.base.base_accessor import BaseAccessor

getcontext().prec = 2


class MetricAccessor(BaseAccessor):
    async def create_metric(
        self,
        tisker_id: int,
        value: Decimal,
        delta: Decimal,
    ) -> Optional[Metric]:
        new_metric: MetricModel = MetricModel(
            tisker_id=tisker_id,
            value=value,
            delta=delta,
        )
        async with self.app.database.session.begin() as session:
            session.add(new_metric)

        return Metric(
            id=new_metric.id,
            tisker_id=new_metric.tisker_id,
            value=new_metric.value,
            delta=new_metric.delta,
        )

    async def get_metric_id(self, tisker_id: int) -> Optional[Metric]:
        query = select(MetricModel).where(MetricModel.tisker_id == tisker_id)

        async with self.app.database.session() as session:
            metric: Optional[MetricModel] = await session.scalar(query)

        if not metric:
            return None

        return Metric(
            id=metric.id,
            tisker_id=metric.tisker_id,
            value=metric.value,
            delta=metric.delta,
        )

    async def list_metrics(self) -> List[Optional[Metric]]:
        query = select(MetricModel)

        async with self.app.database.session() as session:
            metrics: List[Optional[MetricModel]] = await session.scalars(query)

        if not metrics:
            return []

        return [
            Metric(
                id=metric.id,
                tisker_id=metric.tisker_id,
                value=metric.value,
                delta=metric.delta,
            )
            for metric in metrics.all()
        ]

    async def list_metrics_join(self) -> List[Optional[MetricTotalJoin]]:
        query = select(MetricModel).options(joinedload(MetricModel.tisker))

        async with self.app.database.session() as session:
            metrics = await session.scalars(query)

        if not metrics:
            return []
        return [
            MetricTotalJoin(
                id=metric.id,
                tisker=metric.tisker.tisker,
                name=metric.tisker.name,
                value=metric.value,
                delta=metric.delta,
            )
            for metric in metrics.all()
        ]

    async def update_metric(
        self,
        tisker_id: int,
        value: Decimal,
        delta: Decimal,
    ) -> Optional[Metric]:
        query = (
            update(MetricModel)
            .where(MetricModel.tisker_id == tisker_id)
            .values(value=value, delta=delta)
            .returning(MetricModel)
        )

        async with self.app.database.session.begin() as session:
            metric: Optional[MetricModel] = await session.scalar(query)

        if not metric:
            return None

        return Metric(
            id=metric.id,
            tisker_id=metric.tisker_id,
            value=metric.value,
            delta=metric.delta,
        )
