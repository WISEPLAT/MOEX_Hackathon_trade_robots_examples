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

from app.balances.schemes import (
    BalanceRequestSchema,
    BalanceResponseSchema,
    BalanceListResponseSchema,
    BalanceListRequestSchema,
    BalanceUpdateRequestSchema,
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.balances.models import Balance

getcontext().prec = 2


class BalanceAddView(AuthUserRequiredMixin, View):
    @request_schema(BalanceRequestSchema)
    @response_schema(BalanceResponseSchema, 200)
    @docs(
        tags=["balances"],
        summary="Add balance add view",
        description="Add balance to database",
    )
    async def post(self) -> Response:
        user_id: int = self.request.user.id
        balance: Decimal = self.data["balance"]

        try:
            balance: Balance = await self.store.balances.create_balance(
                user_id=user_id, balance=balance
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=BalanceResponseSchema().dump(balance))


class BalanceUpdateView(AuthUserRequiredMixin, View):
    @request_schema(BalanceUpdateRequestSchema)
    @response_schema(BalanceResponseSchema, 200)
    @docs(
        tags=["balances"],
        summary="Add balance update view",
        description="Update balance in database",
    )
    async def put(self) -> Response:
        user_id: int = self.request.user.id
        balance: Decimal = self.data["balance"]

        try:
            balance: Balance = await self.store.balances.update_balance(
                user_id=user_id, balance=balance
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=BalanceResponseSchema().dump(balance))


class BalanceListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @request_schema(BalanceListRequestSchema)
    @response_schema(BalanceListResponseSchema, 200)
    @docs(
        tags=["balances"],
        summary="Add balance list view",
        description="Get list balances from database",
    )
    async def get(self) -> Response:
        user_id: int = self.request.user.id

        balances: Optional[List[Balance]] = await self.store.balances.list_balances(
            user_id=user_id
        )
        return json_response(BalanceListResponseSchema().dump({"balances": balances}))
    

class BalanceView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @request_schema(BalanceListRequestSchema)
    @response_schema(BalanceResponseSchema, 200)
    @docs(
        tags=["balances"],
        summary="Add balance view",
        description="Get list balance from database",
    )
    async def get(self) -> Response:
        user_id: int = self.request.user.id

        balance: Optional[Balance] = await self.store.balances.get_by_balance_id(
            user_id=user_id
        )
        
        return json_response(BalanceResponseSchema().dump(balance))
