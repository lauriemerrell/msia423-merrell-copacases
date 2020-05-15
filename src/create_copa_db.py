import logging.config
import config

import pymysql
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, Numeric, String

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('create_copa_db')

Base = declarative_base()


class COPA_Case_Attributes(Base):
    """Create a data model for the table `copa_case_attributes`.
    """

    __tablename__ = 'copa_case_attributes'

    id = Column(Integer, primary_key=True)

    # columns to hold case attributes
    case_type = Column(String(20), unique=False, nullable=False)
    current_category = Column(String(40), unique=False, nullable=False)
    police_shooting = Column(Boolean, unique=False, nullable=False)
    beat = Column(String(18), unique=False, nullable=False)
    race_complainants = Column(String(40), unique=False, nullable=False)
    sex_complainants = Column(String(36), unique=False, nullable=False)
    age_complainants = Column(String(24), unique=False, nullable=False)
    race_officers = Column(String(40), unique=False, nullable=False)
    sex_involved_officers = Column(String(36), unique=False, nullable=False)
    age_officers = Column(String(24), unique=False, nullable=False)
    years_on_force_officers = Column(String(18), unique=False, nullable=False)
    complaint_day = Column(Integer, unique=False, nullable=False)
    complaint_month = Column(Integer, unique=False, nullable=False)

    # columns to hold predicted probabilities from final model
    pred_outcome = Column(String(24), unique=False, nullable=False)
    pred_prob = Column(Numeric, unique=False, nullable=False)

    def __repr__(self):
        return '<Case %i>' % self.id


def create_db(engine_string=None):
    """Creates a database with the data models inherited from `Base` (Tweet and TweetScore).

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    if engine_string is None:
        return ValueError("`engine_string` must be provided")

    engine = sql.create_engine(engine_string)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    """Create database with configured SQLAlchemy URI.
    """
    try:
        create_db(engine_string=config.SQLALCHEMY_DATABASE_URI)
        logger.warning("Table created in database.")
    except sql.exc.SQLAlchemyError as e1:
        logger.error("Couldn't connect to database. If you're trying to connect to RDS, are you on the NU VPN? :P")
        logger.error(e1)
    except ValueError as e2:
        logger.error(e2)