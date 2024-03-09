from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated


intpk = Annotated[int, mapped_column(primary_key=True)]
str_20 = Annotated[str,  mapped_column(String(20))]
autoint = Annotated[int, mapped_column(autoincrement='auto')]

class Base(DeclarativeBase):
    pass


class AreasCountryOrm(Base):
    __tablename__ = 'areas_country'
    num_country: Mapped[autoint]
    country_id: Mapped[intpk]
    country_name: Mapped[str] = mapped_column(String(20), nullable=False)


class AreasRegionOrm(Base):
    __tablename__ = 'areas_region'
    num_region: Mapped[autoint]
    country_id: Mapped[int] = mapped_column(ForeignKey('areas_country.country_id', ondelete='CASCADE'))
    region_id: Mapped[intpk]
    region_name: Mapped[str] = mapped_column(String(40), nullable=False)


class AreasCityOrm(Base):
    __tablename__ = 'areas_city'
    num_city: Mapped[autoint]
    region_id: Mapped[int] = mapped_column(ForeignKey('areas_region.region_id', ondelete='CASCADE'))
    city_id: Mapped[intpk]
    city_name: Mapped[str] = mapped_column(String(40), nullable=False)


# class VacanciesOrm(Base):
#     __tablename__ = 'vacancies'
#     num_vacancy: Mapped[autoint]
