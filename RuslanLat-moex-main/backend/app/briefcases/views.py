from typing import List, Optional
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.briefcases.schemes import (
    BriefcaseRequestSchema,
    BriefcaseResponseSchema,
    BriefcaseListResponseSchema,
    BriefcaseListRequestSchema,
    BriefcaseTotalUpdateResponseSchema,
    BriefcaseTotalUpdateRequestSchema,
    BriefcaseTotalListResponseSchema,
    BriefcaseTotalJoinListResponseSchema
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.briefcases.models import Briefcase, BriefcaseTotal, BriefcaseTotalJoin
from app.tiskers.models import Tisker


class BriefcaseAddView(AuthUserRequiredMixin, View):
    @request_schema(BriefcaseRequestSchema)
    @response_schema(BriefcaseResponseSchema, 200)
    @docs(
        tags=["briefcases"],
        summary="Add briefcase add view",
        description="Add briefcase to database",
    )
    async def post(self) -> Response:
        tisker: str = self.data["tisker"]
        tisker: Tisker = await self.store.tiskers.get_by_tisker(tisker=tisker)
        tisker_id: int = tisker.id
        user_id: int = self.request.user.id
        price: float = self.data["price"]
        quantity: int = self.data["quantity"]
        amount: float = self.data["amount"]

        try:
            briefcase: Optional[
                Briefcase
            ] = await self.store.briefcases.create_briefcase(
                tisker_id=tisker_id,
                user_id=user_id,
                price=price,
                quantity=quantity,
                amount=amount,
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=BriefcaseResponseSchema().dump(briefcase))


class BriefcaseListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @request_schema(BriefcaseListRequestSchema)
    @response_schema(BriefcaseListResponseSchema, 200)
    @docs(
        tags=["briefcases"],
        summary="Add briefcase list view",
        description="Get list briefcases from database",
    )
    async def get(self) -> Response:
        user_id: int = self.request.user.id
        briefcases: Optional[
            List[Briefcase]
        ] = await self.store.briefcases.list_briefcases(user_id=user_id)
        return json_response(
            BriefcaseListResponseSchema().dump({"briefcases": briefcases})
        )


class BriefcaseJoinListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @request_schema(BriefcaseListRequestSchema)
    @response_schema(BriefcaseTotalJoinListResponseSchema, 200)
    @docs(
        tags=["briefcases"],
        summary="Add briefcase join list view",
        description="Get list briefcase join from database",
    )
    async def get(self) -> Response:
        user_id: int = self.request.user.id
        briefcases: Optional[
            List[BriefcaseTotalJoin]
        ] = await self.store.briefcases.list_briefcases_join(user_id=user_id)
        return json_response(
            BriefcaseTotalJoinListResponseSchema().dump({"briefcases": briefcases})
        )
    

class BriefcaseTotalAddView(AuthUserRequiredMixin, View):
    @request_schema(BriefcaseRequestSchema)
    @response_schema(BriefcaseTotalUpdateResponseSchema, 200)
    @docs(
        tags=["briefcases"],
        summary="Add briefcase total add view",
        description="Add briefcase total to database",
    )
    async def post(self) -> Response:
        tisker_id: int = self.data["tisker_id"]
        user_id: int = self.request.user.id
        price: float = self.data["price"]
        quantity: int = self.data["quantity"]
        amount: float = self.data["amount"]

        try:
            briefcase: Optional[
                BriefcaseTotal
            ] = await self.store.briefcases.create_briefcase_total(
                tisker_id=tisker_id,
                user_id=user_id,
                price=price,
                quantity=quantity,
                amount=amount,
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=BriefcaseTotalUpdateResponseSchema().dump(briefcase))


class BriefcaseTotalUpdateView(AuthUserRequiredMixin, View):
    @request_schema(BriefcaseTotalUpdateRequestSchema)
    @response_schema(BriefcaseTotalUpdateResponseSchema, 200)
    @docs(
        tags=["briefcases"],
        summary="Add briefcase update view",
        description="Update briefcase in database",
    )
    async def put(self) -> Response:
        tisker_id: int = self.data["tisker_id"]
        user_id: int = self.request.user.id
        price: float = self.data["price"]
        quantity: int = self.data["quantity"]
        amount: float = self.data["amount"]

        try:
            briefcase: BriefcaseTotal = await self.store.balances.update_balance(
                tisker_id=tisker_id,
                user_id=user_id,
                price=price,
                quantity=quantity,
                amount=amount,
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=BriefcaseTotalUpdateResponseSchema().dump(briefcase))
    

class BriefcaseTotalListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @request_schema(BriefcaseListRequestSchema)
    @response_schema(BriefcaseTotalListResponseSchema, 200)
    @docs(
        tags=["briefcases"],
        summary="Add briefcase total list view",
        description="Get list briefcase totals from database",
    )
    async def get(self) -> Response:
        user_id: int = self.request.user.id
        briefcases: Optional[
            List[BriefcaseTotal]
        ] = await self.store.briefcases.list_briefcase_totals(user_id=user_id)
        return json_response(
            BriefcaseTotalListResponseSchema().dump({"briefcases": briefcases})
        )


class BriefcaseTotalJoinListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @request_schema(BriefcaseListRequestSchema)
    @response_schema(BriefcaseTotalJoinListResponseSchema, 200)
    @docs(
        tags=["briefcases"],
        summary="Add briefcase total join list view",
        description="Get list briefcase totals join from database",
    )
    async def get(self) -> Response:
        user_id: int = self.request.user.id
        briefcases: Optional[
            List[BriefcaseTotalJoin]
        ] = await self.store.briefcases.list_briefcase_totals_join(user_id=user_id)
        return json_response(
            BriefcaseTotalJoinListResponseSchema().dump({"briefcases": briefcases})
        )