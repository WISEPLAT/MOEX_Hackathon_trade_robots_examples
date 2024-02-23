from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("stock", api.stockViewSet)
router.register("strategy", api.strategyViewSet)
router.register("trader", api.traderViewSet)
router.register("tradestat", api.tradestatViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("Trading/stock/", views.stockListView.as_view(), name="Trading_stock_list"),
    path("Trading/stock/create/", views.stockCreateView.as_view(), name="Trading_stock_create"),
    path("Trading/stock/detail/<int:pk>/", views.stockDetailView.as_view(), name="Trading_stock_detail"),
    path("Trading/stock/update/<int:pk>/", views.stockUpdateView.as_view(), name="Trading_stock_update"),
    path("Trading/stock/delete/<int:pk>/", views.stockDeleteView.as_view(), name="Trading_stock_delete"),
    path("Trading/strategy/", views.strategyListView.as_view(), name="Trading_strategy_list"),
    path("Trading/strategy/create/", views.strategyCreateView.as_view(), name="Trading_strategy_create"),
    path("Trading/strategy/detail/<int:pk>/", views.strategyDetailView.as_view(), name="Trading_strategy_detail"),
    path("Trading/strategy/update/<int:pk>/", views.strategyUpdateView.as_view(), name="Trading_strategy_update"),
    path("Trading/strategy/delete/<int:pk>/", views.strategyDeleteView.as_view(), name="Trading_strategy_delete"),
    path("Trading/trader/", views.traderListView.as_view(), name="Trading_trader_list"),
    path("Trading/trader/create/", views.traderCreateView.as_view(), name="Trading_trader_create"),
    path("Trading/trader/detail/<int:pk>/", views.traderDetailView.as_view(), name="Trading_trader_detail"),
    path("Trading/trader/update/<int:pk>/", views.traderUpdateView.as_view(), name="Trading_trader_update"),
    path("Trading/trader/delete/<int:pk>/", views.traderDeleteView.as_view(), name="Trading_trader_delete"),
    path("Trading/tradestat/", views.tradestatListView.as_view(), name="Trading_tradestat_list"),
    path("Trading/tradestat/create/", views.tradestatCreateView.as_view(), name="Trading_tradestat_create"),
    path("Trading/tradestat/detail/<int:pk>/", views.tradestatDetailView.as_view(), name="Trading_tradestat_detail"),
    path("Trading/tradestat/update/<int:pk>/", views.tradestatUpdateView.as_view(), name="Trading_tradestat_update"),
    path("Trading/tradestat/delete/<int:pk>/", views.tradestatDeleteView.as_view(), name="Trading_tradestat_delete"),
    path("Trading/tradestat/import/", views.tradestatImportFromAPI, name="tradestatImportFromAPI"),
    path("Trading/tradestat/<str:SECID>/", views.tradestatBySECID, name="Trading_tradestat_by_SECID"),

)
