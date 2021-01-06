import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from ueaglider.data.modelbase import SqlAlchemyBase
import json

# Store credentials in a external file that is never added to git or shared over insecure channels
with open('secrets.txt') as json_file:
    secrets = json.load(json_file)

__factory = None


def global_init(db_file: str):
    global __factory
    # If the factory is already running, don't run it again
    if __factory:
        return
    if not db_file or not db_file.strip():
        raise Exception("You must specify a db file.")

    # Using pymysql to talk to db, resolves lack of mypyDB
    conn_str = 'mysql+pymysql://' + secrets['sql_user'] + ':'+secrets['sql_pwd'] + '@localhost/' + db_file.strip()
    print("Connecting to DB with {}".format(conn_str))

    # Can switch echo to True for debug, SQL actions print out to terminal
    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import ueaglider.data.__all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()

