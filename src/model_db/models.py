from typing import Annotated
import datetime
import enum
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
    text,
)


intpk = Annotated[int, mapped_column(primary_key=True, unique=True)]
strpk = Annotated[str, mapped_column(primary_key=True, unique=True)]

str_10 = Annotated[str,  mapped_column(String(10))]
str_20 = Annotated[str,  mapped_column(String(20))]
str_60 = Annotated[str,  mapped_column(String(60))]
str_100 = Annotated[str,  mapped_column(String(100))]
autoint = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Base(DeclarativeBase):
    pass


class AreasOrm(Base):
    __tablename__ = 'areas'
    id: Mapped[autoint]
    id_areas: Mapped[intpk]
    name_areas: Mapped[str]
    code_areas: Mapped[int]
    parent_id_country: Mapped[int] = mapped_column(nullable=True)
    parent_name_country: Mapped[str_20] = mapped_column(nullable=True)
    parent_id_region: Mapped[int] = mapped_column(nullable=True)
    parent_name_region: Mapped[str_60] = mapped_column(nullable=True)


class VacancyTypeOrm(Base):
    __tablename__ = 'vacancy_type'
    num_vacancy_type: Mapped[autoint]
    type_id: Mapped[strpk]
    type_name: Mapped[str_10]


class ScheduleTypeOrm(Base):
    __tablename__ = 'schedule_type'
    num_schedule_type: Mapped[autoint]
    schedule_id: Mapped[strpk]
    schedule_name: Mapped[str_60]


class ExperienceTypeOrm(Base):
    __tablename__ = 'experience_type'
    num_experience_type: Mapped[autoint]
    experience_id: Mapped[strpk]
    experience_name: Mapped[str_60]


class EmploymentTypeOrm(Base):
    __tablename__ = 'employment_type'
    num_employment_type: Mapped[autoint]
    employment_id: Mapped[strpk]
    employment_name: Mapped[str_60]


class FavoritesCompanyOrm(Base):
    __tablename__ = 'favorites_companies'
    num_company: Mapped[autoint]
    employer_id: Mapped[int]
    employer_name: Mapped[str_60]
    employer_url: Mapped[str_100]


class VacanciesOrm(Base):
    __tablename__ = 'vacancies'

    # Main information
    id: Mapped[autoint] = mapped_column(__name_pos='ID')
    vacancy_id: Mapped[intpk] = mapped_column(__name_pos='ID vacancy')
    name: Mapped[str_100] = mapped_column(__name_pos='Name vacancy')

    # Information - salary
    salary_from: Mapped[int] = mapped_column(__name_pos='Salary (from)', nullable=True)
    salary_to: Mapped[int] = mapped_column(__name_pos='Salary (to)', nullable=True)
    salary_currency: Mapped[str] = mapped_column(__name_pos='Salary (currency)', nullable=True)
    salary_gross: Mapped[bool] = mapped_column(__name_pos='Salary (gross)', nullable=True)

    # Information - address
    id_areas: Mapped[int or None] = mapped_column(ForeignKey(AreasOrm.id_areas), nullable=True)
    address_raw: Mapped[str or None] = mapped_column(nullable=True)
    address_city: Mapped[str or None] = mapped_column(nullable=True)
    address_street: Mapped[str or None] = mapped_column(nullable=True)
    address_building: Mapped[str or None] = mapped_column(nullable=True)
    address_lat: Mapped[float or None] = mapped_column(nullable=True)
    address_lng: Mapped[float or None] = mapped_column(nullable=True)
    address_description: Mapped[str or None] = mapped_column(nullable=True)
    address_id: Mapped[int or None] = mapped_column(nullable=True)

    # Main criteria
    type_id: Mapped[str] = mapped_column(ForeignKey(VacancyTypeOrm.type_id, ondelete='CASCADE'), nullable=False)
    schedule_id: Mapped[str] = mapped_column(ForeignKey(ScheduleTypeOrm.schedule_id, ondelete='CASCADE'),
                                             nullable=False)
    experience_id: Mapped[str] = mapped_column(ForeignKey(ExperienceTypeOrm.experience_id, ondelete='CASCADE'),
                                               nullable=False)
    employment_id: Mapped[str] = mapped_column(ForeignKey(EmploymentTypeOrm.employment_id, ondelete='CASCADE'),
                                               nullable=False)

    # Information about employee
    employer_id: Mapped[int or None]
    employer_url: Mapped[str or None]
    employer_alternate_url: Mapped[str or None]
    employer_logo_urls: Mapped[str]
    employer_vacancies_url: Mapped[str]
    employer_accredited_it_employer: Mapped[bool]
    employer_trusted: Mapped[bool]

    # has_test: Mapped[bool]
    # response_letter_required: Mapped[bool]
    #
    # premium: Mapped[bool]

    # department_id: Mapped[int or None]
    # department_name: Mapped[str or None]

    # address_metro_station_name: Mapped[str or None]
    # address_metro_line_name: Mapped[str or None]
    # address_metro_station_id: Mapped[float or None]
    # address_metro_line_id: Mapped[int or None]
    # address_metro_lat: Mapped[float or None]
    # address_metro_lng: Mapped[float or None]

    # response_url: Mapped[str or None]
    # sort_point_distance: Mapped[int or None]
    # published_at: Mapped[str or None]
    # created_at: Mapped[str or None]
    # archived: Mapped[bool]
    # apply_alternate_url: Mapped[str]
    # # show_logo_in_search: Mapped[bool or None]
    #
    # insider_interview_id: Mapped[str or None]
    # insider_interview_url: Mapped[str or None]
    #
    # url: Mapped[str]
    # alternate_url: Mapped[str]
    # relations: Mapped[str]
    #

    #
    # snippet_requirement: Mapped[str or None]
    # snippet_responsibility: Mapped[str or None]
    #
    # contacts_call_tracking_enabled: Mapped[bool or None]
    # contacts_email: Mapped[str or None]
    # contacts_name: Mapped[str or None]
    # contacts_phones_city: Mapped[str or None]
    # contacts_phones_comment: Mapped[str or None]
    # contacts_phones_country: Mapped[str or None]
    # contacts_phones_formatted: Mapped[str or None]
    # contacts_phones_number: Mapped[str or None]
    #
    #
    # # working_days: Mapped[str]
    # # working_time_intervals: Mapped[str]
    # # working_time_modes: Mapped[str]
    #
    # accept_temporary: Mapped[bool or None]
    # # professional_roles_id: Mapped[int]
    # # professional_roles_name: Mapped[str]
    # accept_incomplete_resumes: Mapped[bool or None]

    # # is_adv_vacancy: Mapped[bool]
