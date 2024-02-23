from marshmallow import Schema, fields
import json
from decimal import *


class BalanceSchema(Schema):
    user_id = fields.Int(required=True)
    balance = fields.Decimal()


class BalanceRequestSchema(BalanceSchema):
    pass


class BalanceResponseSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    balance = fields.Decimal(as_string=True)




class BalanceUpdateRequestSchema(Schema):
    balance = fields.Float()


class BalanceListRequestSchema(Schema):
    user_id = fields.Int()


class BalanceListResponseSchema(Schema):
    balances = fields.Nested(BalanceResponseSchema, many=True)
