import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from ueaglider.data.modelbase import SqlAlchemyBase
import json
import os
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Store credentials in a external file that is never added to git or shared over insecure channels
with open(folder+'/secrets.txt') as json_file:
    secrets = json.load(json_file)

__factory = None


def global_init():
    global __factory
    # If the factory is already running, don't run it again
    if __factory:
        return

    # Using pymysql to talk to db, resolves lack of mypyDB
    #mysql - uGliderAdmin - pqu35t3 - DseagliderNew - P3308 - h127.0.0.1
    conn_str = 'mysql+pymysql://' + secrets['sql_user'] + ':' + secrets['sql_pwd'] + '@' + secrets['remote_string']\
               + '/' + secrets['db_name']
    print("Connecting to DB with {}".format(conn_str))

    # Can switch echo to True for debug, SQL actions print out to terminal
    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import ueaglider.data.__all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    session: Session = __factory()
    session.expire_on_commit = False
    return session
