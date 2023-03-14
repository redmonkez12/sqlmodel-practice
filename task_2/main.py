from sqlmodel import SQLModel, Field, Session, select, or_

import sqlalchemy as sa

from database import connect, create_tables


class Country(SQLModel, table=True):
    __tablename__ = "countries"

    country_id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=True)
    continent: str = Field(nullable=True)
    area: int = Field(sa_column=sa.Column(sa.BigInteger, nullable=True))
    population: int = Field(sa_column=sa.Column(sa.BigInteger, nullable=True))
    gdp: str = Field(sa_column=sa.Column(sa.BigInteger, nullable=True))


new_countries = [
    Country(name="Afghanistan", continent="Asia", area=652230, population=25500100, gdp=20343000000),
    Country(name="Albania", continent="Europe", area=28748, population=2831741, gdp=12960000000),
    Country(name="Algeria", continent="Africa", area=2381741, population=37100000, gdp=188681000000),
    Country(name="Andorra", continent="Europe", area=468, population=78115, gdp=3712000000),
    Country(name="Angola", continent="Africa", area=1246700, population=20609294, gdp=100990000000),
]

if __name__ == "__main__":
    engine = connect()
    create_tables(engine)

    with Session(engine) as session:
        session.add_all(new_countries)
        session.commit()

        statement = (
            select(Country)
            .where(or_(Country.population >= 25000000, Country.area >= 3000000))
        )

        result = session.exec(statement).all()

        for row in result:
            print(row)
