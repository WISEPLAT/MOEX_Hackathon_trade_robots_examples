from aiohttp.web_app import Application


def setup_routes(app: Application):
    from app.admin.routes import setup_routes as admin_setup_routes
    from app.users.routes import setup_routes as user_setup_routes
    from app.briefcases.routes import setup_routes as briefcase_setup_routes
    from app.tiskers.routes import setup_routes as tisker_setup_routes
    from app.balances.routes import setup_routes as balance_setup_routes
    from app.metrics.routes import setup_routes as metric_setup_routes
    from app.web import views


    admin_setup_routes(app)
    user_setup_routes(app)
    briefcase_setup_routes(app)
    tisker_setup_routes(app)
    balance_setup_routes(app)
    metric_setup_routes(app)
    app.router.add_get("/", views.index, name="home")

