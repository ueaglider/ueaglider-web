import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from ueaglider.data.modelbase import SqlAlchemyBase

__factory = None


def global_init(db_name: str):
    global __factory

    if __factory:
        return


    if not db_name or not db_name.strip():
        raise Exception("You must specify a db file.")

    conn_str = 'mysql://root:@127.0.0.1/' + db_name.strip()
    print("Connecting to DB with {}".format(conn_str))

    # Adding check_same_thread = False after the recording. This can be an issue about
    # creating / owner thread when cleaning up sessions, etc. This is a sqlite restriction
    # that we probably don't care about in this example.
    engine = sa.create_engine(conn_str, echo=False, connect_args={"check_same_thread": False})
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import pypi_org.data.__all_models

    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    global __factory
    return __factory()