from hashlib import sha256
from aiohttp.web import (
    HTTPForbidden,
    HTTPUnauthorized,
)
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from aiohttp_session import new_session
from aiohttp.web_response import Response

from app.admin.schemes import (
    AdminRequestSchema,
    AdminResponseSchema
)
from app.web.app import View
from app.web.utils import json_response
from app.admin.models import Admin
import json


class AdminLoginView(View):
    @request_schema(AdminRequestSchema)
    @response_schema(AdminResponseSchema, 200)
    @docs(
        tags=["admin"],
        summary="Add admin login view",
        description="Get admin from database",
    )
    async def post(self) -> Response:
        login: str = self.data["login"]
        password: str = self.data["password"]

        admin: Admin = await self.store.admins.get_by_login(login)

        if not admin:
            raise HTTPForbidden(text="No addmin with provided login was found")
        if not admin.is_password_valid(password):
            raise HTTPForbidden(reason="Invalid credentials")

        admin_data: AdminResponseSchema = AdminResponseSchema().dump(admin)

        session = await new_session(request=self.request)
        session["admin"] = admin_data


        return json_response(data=admin_data)


class AdminCurrentView(View):
    @response_schema(AdminResponseSchema, 200)
    @docs(
        tags=["admin"],
        summary="Add admin current view",
        description="Current admin from session",
    )
    async def get(self) -> Response:

        if not hasattr(self.request, "admin"):
            raise HTTPUnauthorized

        admin_data: AdminResponseSchema = AdminResponseSchema().dump(self.request.admin)

        return json_response(data=admin_data)
