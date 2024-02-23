import typing

from app.store.database.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.store.admin.accessor import AdminAccessor
        from app.store.tiskers.accessor import TiskerAccessor
        from app.store.briefcases.accessor import BriefcaseAccessor
        from app.store.balances.accessor import BalanceAccessor
        from app.store.metrics.accessor import MetricAccessor
        from app.store.users.accessor import UserAccessor
        from app.store.users.accessor import UserLoginAccessor
        # from app.store.algopackapi.accessor import AlgoPackApiAccessor

        self.admins = AdminAccessor(app)
        self.tiskers = TiskerAccessor(app)
        self.briefcases = BriefcaseAccessor(app)
        self.balances = BalanceAccessor(app)
        self.metrics = MetricAccessor(app)
        self.users = UserAccessor(app)
        self.user_logins = UserLoginAccessor(app)
        # self.algopackapi = AlgoPackApiAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
