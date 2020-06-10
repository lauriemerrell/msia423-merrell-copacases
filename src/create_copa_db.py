import logging
import pandas as pd
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


logger = logging.getLogger('create_copa_db')

Base = declarative_base()

def create_copa_db(engine_string, app_loc):
    """
    Create database with configured SQLAlchemy URI.
    Args:
        engine_string (str): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`.
        app_loc:

    Returns:
        None.
    """

    create_db(engine_string=engine_string)
    write_data_to_db(engine_string=engine_string, app_loc=app_loc)


class COPA_Case_Attributes(Base):
    """Create a data model for the table `copa_case_attributes`."""

    __tablename__ = 'copa_case_attributes'

    id = Column(Integer, primary_key=True, autoincrement=False)
    police_shooting = Column(String(10), unique=False, nullable=False)
    race_complainants = Column(String(40), unique=False, nullable=False)
    sex_complainants = Column(String(36), unique=False, nullable=False)
    age_complainants = Column(String(24), unique=False, nullable=False)
    race_officers = Column(String(40), unique=False, nullable=False)
    sex_involved_officers = Column(String(36), unique=False, nullable=False)
    age_officers = Column(String(24), unique=False, nullable=False)
    excessive_force = Column(String(10), unique=False, nullable=False)
    years_on_force_officers = Column(String(18), unique=False, nullable=False)


    # column to hold predicted outcome from final model
    pred_outcome = Column(String(24), unique=False, nullable=False)

    # pred_prob = Column(Numeric, unique=False, nullable=False)
    # columns to hold case attributes
    # case_type = Column(String(20), unique=False, nullable=False)
    # current_category = Column(String(40), unique=False, nullable=False)
    # beat = Column(String(18), unique=False, nullable=False)
    # complaint_day = Column(Integer, unique=False, nullable=False)
    # complaint_month = Column(Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Case %i>' % self.id


def create_db(engine_string=None):
    """Create a database with the data models inherited from `Base` (COPA_Case_Attributes).

    Args:
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`.

    Returns:
        None.
    """
    try:
        if engine_string is None:
            return ValueError("`engine_string` must be provided")

        logger.debug("About to create engine with engine string {}".format(engine_string))
        engine = sql.create_engine(engine_string)
        logger.debug("Engine created")
        Base.metadata.create_all(engine)
        logger.info("Table created in database")
    except Exception as e:
        logger.error(e)

def write_data_to_db(engine_string, app_loc):
    """
    Write data to configured database.
    Args:
        engine_string (str): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. Must have copa_case_attributes table already defined.
        app_loc (str): Filepath where data containing all combinations of input features with their predicted responses is saved.

    Returns:
        None.
    """
    # code from sportsco example in msia 423 class materials
    engine = sql.create_engine(engine_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        records = pd.read_csv(app_loc)
        logger.debug("Record datatypes: {}".format(records.dtypes))
        logger.debug("Records shape: {}".format(records.shape))
        logger.warning("Putting data in database - this can take approximately 40 minutes!")
        for i in range(len(records)):
            police_shooting = records['POLICE_SHOOTING'][i]
            race_complainants = records['RACE_OF_COMPLAINANTS'][i]
            sex_complainants = records['SEX_OF_COMPLAINANTS'][i]
            age_complainants = records['AGE_OF_COMPLAINANTS'][i]
            race_officers = records['RACE_OF_INVOLVED_OFFICERS'][i]
            sex_involved_officers = records['SEX_OF_INVOLVED_OFFICERS'][i]
            age_officers = records['AGE_OF_INVOLVED_OFFICERS'][i]
            years_on_force_officers = records['YEARS_ON_FORCE_OF_INVOLVED_OFFICERS'][i]
            excessive_force = str(records['EXCESSIVE_FORCE'][i])
            pred_outcome = records['pred'][i]

            case = COPA_Case_Attributes(id=i, police_shooting=police_shooting, race_complainants=race_complainants,
                                        sex_complainants=sex_complainants, age_complainants=age_complainants,
                                        race_officers=race_officers, sex_involved_officers=sex_involved_officers,
                                        age_officers=age_officers, excessive_force=excessive_force,
                                        years_on_force_officers=years_on_force_officers, pred_outcome=pred_outcome)

            session.add(case)
            if i % 100000 == 0:
                logger.info("At row {}, doing a commit".format(i))
                session.commit()
            if i == (len(records) - 1):
                session.commit()
                logger.info("At final row {}, doing final commit".format(i))

    except Exception as e:
        logger.error(e)

