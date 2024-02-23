from marshmallow import Schema, fields


class AdminSchema(Schema):
    login = fields.Str(required=True)


class AdminRequestSchema(AdminSchema):
    password = fields.Str(required=True)


class AdminResponseSchema(AdminSchema):
    id = fields.Int(required=False)



