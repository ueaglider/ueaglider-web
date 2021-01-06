import sqlalchemy
from ueaglider.data.modelbase import SqlAlchemyBase


class Gliders(SqlAlchemyBase):
    __tablename__ = 'Gliders'
    __table_args__ = {'extend_existing': True}
    GliderID = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)


class Missions(SqlAlchemyBase):
    __tablename__ = 'Missions'
    __table_args__ = {'extend_existing': True}
    MissionID = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)


class Dives(SqlAlchemyBase):
    __tablename__ = 'DiveInfo'
    __table_args__ = {'extend_existing': True}
    DiveInfoID= sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)