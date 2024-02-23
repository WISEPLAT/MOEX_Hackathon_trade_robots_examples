from rest_framework import viewsets, permissions

from . import serializers
from . import models


class stockViewSet(viewsets.ModelViewSet):
    """ViewSet for the stock class"""

    queryset = models.stock.objects.all()
    serializer_class = serializers.stockSerializer
    permission_classes = [permissions.IsAuthenticated]


class strategyViewSet(viewsets.ModelViewSet):
    """ViewSet for the strategy class"""

    queryset = models.strategy.objects.all()
    serializer_class = serializers.strategySerializer
    permission_classes = [permissions.IsAuthenticated]


class traderViewSet(viewsets.ModelViewSet):
    """ViewSet for the trader class"""

    queryset = models.trader.objects.all()
    serializer_class = serializers.traderSerializer
    permission_classes = [permissions.IsAuthenticated]


class tradestatViewSet(viewsets.ModelViewSet):
    """ViewSet for the tradestat class"""

    queryset = models.tradestat.objects.all()
    serializer_class = serializers.tradestatSerializer
    permission_classes = [permissions.IsAuthenticated]
