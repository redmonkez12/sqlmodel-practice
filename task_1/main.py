import datetime

from sqlmodel import SQLModel, Field, Relationship, Session, select

from database import create_tables, connect


class SalesPerson(SQLModel, table=True):
    __tablename__ = "sales_persons"

    sales_id: int = Field(default=None, primary_key=True)
    name: str
    salary: int
    commission_rate: int
    hire_date: datetime.date
    orders: list["Order"] = Relationship(
        sa_relationship_kwargs={
            "cascade": "all"
        }
    )


class Company(SQLModel, table=True):
    __tablename__ = "companies"

    company_id: int = Field(default=None, primary_key=True)
    name: str
    city: str
    orders: list["Order"] = Relationship(
        sa_relationship_kwargs={
            "cascade": "all"
        }
    )


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: int = Field(default=None, primary_key=True)
    order_date: datetime.date = Field(nullable=False)
    amount: float = Field(nullable=False)
    company_id: int = Field(foreign_key=Company.company_id, nullable=False)
    sales_id: int = Field(foreign_key=SalesPerson.sales_id, nullable=False)


engine = connect()

new_sales_people = [
    SalesPerson(name="John", salary=100000, commission_rate=6, hire_date="2006-04-01"),
    SalesPerson(name="Amy", salary=12000, commission_rate=5, hire_date="2010-05-01"),
    SalesPerson(name="Mark", salary=65000, commission_rate=12, hire_date="2008-12-25"),
    SalesPerson(name="Pam", salary=25000, commission_rate=25, hire_date="2005-01-01"),
    SalesPerson(name="Alex", salary=5000, commission_rate=10, hire_date="2007-03-02"),
]

new_companies = [
    Company(name="RED", city="Boston"),
    Company(name="ORANGE", city="New York"),
    Company(name="YELLOW", city="Boston"),
    Company(name="GREEN", city="Austin"),
]

new_orders = [
    Order(order_date="2014-01-01", company_id=3, sales_id=4, amount=10000),
    Order(order_date="2014-02-01", company_id=4, sales_id=5, amount=10000),
    Order(order_date="2014-03-01", company_id=1, sales_id=1, amount=10000),
    Order(order_date="2014-04-01", company_id=1, sales_id=4, amount=10000),
]

if __name__ == "__main__":
    create_tables(engine)

    with Session(engine) as session:
        session.add_all(new_sales_people)
        session.add_all(new_companies)
        session.add_all(new_orders)
        session.commit()

    statement = (
        select(SalesPerson.name)
        .where(SalesPerson.sales_id.not_in(
            select(Order.sales_id).join(Company).where(Company.name == "RED")
        )
        )
    )

    result = session.exec(statement).all()

    for row in result:
        print(row)
