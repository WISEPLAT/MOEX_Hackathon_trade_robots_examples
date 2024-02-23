from marshmallow import Schema, fields


class TiskerSchema(Schema):
    tisker = fields.Str(required=True)
    name = fields.Str(required=True)


class TiskerRequestSchema(TiskerSchema):
    pass


class TiskerDeleteRequestSchema(Schema):
    tisker = fields.Str(required=True)


class TiskerResponseSchema(Schema):
    id = fields.Int(required=True)
    tisker = fields.Str(required=True)
    name = fields.Str(required=True)


class TiskerListResponseSchema(Schema):
    tiskers = fields.Nested(TiskerResponseSchema, many=True)