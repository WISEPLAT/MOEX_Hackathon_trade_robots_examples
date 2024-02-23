import random
import string

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from datetime import datetime

from Trading import models as Trading_models


def random_string(length=10):
    # Create a random string of length length
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def create_User(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_AbstractUser(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return AbstractUser.objects.create(**defaults)


def create_AbstractBaseUser(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return AbstractBaseUser.objects.create(**defaults)


def create_Group(**kwargs):
    defaults = {
        "name": "%s_group" % random_string(5),
    }
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_ContentType(**kwargs):
    defaults = {
    }
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_Trading_stock(**kwargs):
    defaults = {}
    defaults["ticker"] = ""
    defaults["name"] = ""
    defaults.update(**kwargs)
    return Trading_models.stock.objects.create(**defaults)
def create_Trading_strategy(**kwargs):
    defaults = {}
    defaults["label"] = ""
    defaults.update(**kwargs)
    return Trading_models.strategy.objects.create(**defaults)
def create_Trading_trader(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return Trading_models.trader.objects.create(**defaults)
def create_Trading_trading_history(**kwargs):
    defaults = {}
    defaults["priceUpdateDateTime"] = datetime.now()
    defaults["price"] = ""
    if "stock" not in kwargs:
        defaults["stock"] = create_Trading_stock()
    defaults.update(**kwargs)
    return Trading_models.trading_history.objects.create(**defaults)
