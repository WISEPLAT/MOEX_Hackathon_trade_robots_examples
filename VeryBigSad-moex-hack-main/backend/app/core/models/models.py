from tortoise import fields
from tortoise.models import Model


class User(Model):
    class Meta:
        table = "users"
        ordering = ["created_at"]

    id = fields.BigIntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class News(Model):
    class Meta:
        table = "news"
        ordering = ["created_at"]

    id = fields.BigIntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    text = fields.TextField()

    is_active = fields.BooleanField(default=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Backtest(Model):
    class Meta:
        table = "backtests"
        ordering = ["created_at"]

    id = fields.BigIntField(pk=True)

    date_start = fields.DateField()
    date_end = fields.DateField()

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Strategy(Model):
    class Meta:
        table = "strategies"
        ordering = ["created_at"]

    id = fields.BigIntField(pk=True)
    backtest = fields.ForeignKeyField("models.Backtest", related_name="strategies")

    name = fields.CharField(max_length=255)
    source = fields.TextField()

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
