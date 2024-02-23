from typing import List
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc

from app.tiskers.schemes import (
    TiskerRequestSchema,
    TiskerResponseSchema,
    TiskerListResponseSchema,
    TiskerDeleteRequestSchema,
)
from app.web.app import View
from app.web.mixins import (
    AuthRequiredMixin,
    AuthUserRequiredMixin,
)
from app.web.utils import json_response
from app.tiskers.models import Tisker


class TiskerAddView(AuthUserRequiredMixin, View):
    @request_schema(TiskerRequestSchema)
    @response_schema(TiskerResponseSchema, 200)
    @docs(
        tags=["tiskers"],
        summary="Add tisker add view",
        description="Add tisker to database",
    )
    async def post(self) -> Response:
        tisker: str = self.data["tisker"]
        name: str = self.data["name"]

        try:
            tisker: Tisker = await self.store.tiskers.create_tisker(
                tisker=tisker, name=name
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=TiskerResponseSchema().dump(tisker))


class TiskerUpdateView(AuthUserRequiredMixin, View):
    @request_schema(TiskerResponseSchema)
    @response_schema(TiskerResponseSchema, 200)
    @docs(
        tags=["tiskers"],
        summary="Add tisker update view",
        description="Update tisker in database",
    )
    async def put(self) -> Response:
        id: int = self.data["id"]
        tisker: str = self.data["tisker"]
        name: str = self.data["name"]
        
        try:
            tisker: Tisker = await self.store.tiskers.update_tisker(
                id=id, tisker=tisker, name=name
            )
        except exc.IntegrityError as e:
            if "23505" in e.orig.pgcode:
                raise HTTPConflict

        return json_response(data=TiskerResponseSchema().dump(tisker))


class TiskerDeleteView(AuthUserRequiredMixin, View):
    @request_schema(TiskerDeleteRequestSchema)
    @response_schema(TiskerResponseSchema, 200)
    @docs(
        tags=["tiskers"],
        summary="Add tisker delete view",
        description="Delete tisker from database",
    )
    async def delete(self) -> Response:
        tisker: str = self.data["tisker"]

        tisker: Tisker = await self.store.tiskers.delete_tisker(tisker=tisker)

        return json_response(data=TiskerResponseSchema().dump(tisker))


class TiskerListView(AuthUserRequiredMixin, View):  # AuthRequiredMixin,
    @response_schema(TiskerListResponseSchema, 200)
    @docs(
        tags=["tiskers"],
        summary="Add tisker list view",
        description="Get list tiskers from database",
    )
    async def get(self) -> Response:
        tiskers: List[Tisker] = await self.store.tiskers.list_tiskers()
        return json_response(TiskerListResponseSchema().dump({"tiskers": tiskers}))
