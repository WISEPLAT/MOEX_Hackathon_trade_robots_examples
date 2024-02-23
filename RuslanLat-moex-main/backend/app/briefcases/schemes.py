from marshmallow import Schema, fields


class BriefcaseSchema(Schema):
    tisker = fields.Str(required=True)
    user_id = fields.Int()
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)
    amount = fields.Float(required=True)


class BriefcaseRequestSchema(BriefcaseSchema):
    pass


class BriefcaseResponseSchema(Schema):
    id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    tisker_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)
    amount = fields.Float(required=True)


class BriefcaseTotalUpdateResponseSchema(Schema):
    id = fields.Int(required=True)
    tisker_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)
    amount = fields.Float(required=True)


class BriefcaseTotalUpdateRequestSchema(Schema):
    tisker_id = fields.Int(required=True)
    user_id = fields.Int()
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)
    amount = fields.Float(required=True)


class BriefcaseTotalJsonResponseSchema(Schema):
    tisker = fields.Str(required=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)
    amount = fields.Float(required=True)


class BriefcaseListRequestSchema(Schema):
    user_id = fields.Int()


class BriefcaseListResponseSchema(Schema):
    briefcases = fields.Nested(BriefcaseResponseSchema, many=True)


class BriefcaseTotalListResponseSchema(Schema):
    briefcases = fields.Nested(BriefcaseTotalUpdateResponseSchema, many=True)


class BriefcaseTotalJoinListResponseSchema(Schema):
    briefcases = fields.Nested(BriefcaseTotalJsonResponseSchema, many=True)
