from sqlalchemy.orm import Session

from models.company import Company as CompanyBase

from services.tinkoff_parser import get_company_data_by_ticker


def create_company(ticker: str, db: Session):
    try:
        icon, description, name, background, text_color = get_company_data_by_ticker(ticker)
    except:
        return None

    company = CompanyBase(
        ticker=ticker,
        name=name,
        icon=icon,
        description=description,
        background=background,
        text_color=text_color
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return company


def get_all_companies(db: Session):
    return db.query(CompanyBase).all()


def get_company(ticker: str, db: Session):
    return db.query(CompanyBase).filter(CompanyBase.ticker == ticker).first()


def remove_company(ticker: str, db: Session):
    company = db.query(CompanyBase).filter(CompanyBase.ticker == ticker).delete()

    db.commit()

    return company
