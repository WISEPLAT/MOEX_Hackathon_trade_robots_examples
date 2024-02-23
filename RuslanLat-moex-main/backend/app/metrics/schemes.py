from marshmallow import Schema, fields
import json
from decimal import *


class MetricSchema(Schema):
    tisker_id = fields.Int()
    tisker = fields.Str()
    value = fields.Decimal(required=True)
    delta = fields.Decimal(required=True)

class MetricRequestSchema(MetricSchema):
    pass


class MetricResponseSchema(Schema):
    id = fields.Int(required=True)
    tisker_id = fields.Int(required=True)
    value = fields.Decimal(as_string=True)
    delta = fields.Decimal(as_string=True)


class MetricUpdateRequestSchema(MetricSchema):
    pass


class MetricListResponseSchema(Schema):
    metrics = fields.Nested(MetricResponseSchema, many=True)


class MetricJoinResponseSchema(Schema):
    id = fields.Int(required=True)
    tisker = fields.Str(required=True)
    name = fields.Str(required=True)
    value = fields.Decimal(as_string=True)
    delta = fields.Decimal(as_string=True)



class MetricJoinListResponseSchema(Schema):
    metrics = fields.Nested(MetricJoinResponseSchema, many=True)
