from rest_framework import serializers

from . import models


class stockSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.stock
        fields = [
            "ticker",
            "created",
            "last_updated",
            "name",
        ]

class strategySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.strategy
        fields = [
            "last_updated",
            "created",
            "label",
        ]

class traderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.trader
        fields = [
            "created",
            "last_updated",
        ]

class tradestatSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.tradestat
        fields = [
            "priceUpdateDateTime",
            "last_updated",
            "price",
            "created",
            "stock",
        ]
