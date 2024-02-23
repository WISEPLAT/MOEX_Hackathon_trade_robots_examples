from marshmallow import Schema, fields


class UserLoginBaseSchema(Schema):
    login = fields.Str(required=True)


class UserLoginRequestSchema(UserLoginBaseSchema):
    password = fields.Str(required=True)


class UserLoginResponseSchema(UserLoginBaseSchema):
    id = fields.Int(required=True)


class UserLoginUpdateRequestSchema(UserLoginRequestSchema):
    pass


class UserLoginListResponseSchema(Schema):
    users = fields.Nested(UserLoginResponseSchema, many=True)


class UserBaseSchema(Schema):
    name = fields.Str(required=True)
    lastname = fields.Str(required=True)


class UserRequestSchema(UserBaseSchema):
    pass


class UserResponseSchema(Schema):
    id = fields.Int(required=True) 
    name = fields.Str(required=True)
    lastname = fields.Str(required=True)


class UserUpdateRequestSchema(UserResponseSchema):
    pass


class UserListResponseSchema(Schema):
    users = fields.Nested(UserResponseSchema, many=True)