from sqlalchemy.orm import Session

from services.company import get_all_companies
from services.stock import get_stock


def get_stocks_catalog_page(db: Session, limit: int = None, page: int = None, search_value: str = None):
    companies = get_all_companies(db)

    if search_value:
        companies = [company for company in companies if search_value.lower() in company.name.lower()]

    if limit is not None and page is not None:
        index_from = limit * (page - 1)

        if index_from > len(companies):
            return []

        index_to = min(len(companies), limit * page)

        companies = companies[index_from:index_to]

    result = []

    for company in companies:
        stock = get_stock(company.ticker, db)

        result.append({
            "id": company.ticker,
            "description": company.description,
            "companyName": company.name,
            "companyIcon": company.icon,
            "background": company.background,
            "stockPrice": stock.price
        })

    return result
