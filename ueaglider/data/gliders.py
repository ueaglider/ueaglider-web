from typing import List

import sqlalchemy
from sqlalchemy import orm

from ueaglider.data.modelbase import SqlAlchemyBase


class Gliders(SqlAlchemyBase):
    __tablename__ = 'Gliders'
    __table_args__ = {'extend_existing': True}
    GliderID = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)
    MissionID = sqlalchemy.Column(sqlalchemy.INT)
    Name = sqlalchemy.Column(sqlalchemy.VARCHAR)
    Number = sqlalchemy.Column(sqlalchemy.INT)
    Info = sqlalchemy.Column(sqlalchemy.TEXT)


class Targets(SqlAlchemyBase):
    __tablename__ = 'Targets'
    __table_args__ = {'extend_existing': True}
    TargetsID = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)
    Name = sqlalchemy.Column(sqlalchemy.VARCHAR)
    Latitude = sqlalchemy.Column(sqlalchemy.FLOAT)
    Longitude = sqlalchemy.Column(sqlalchemy.FLOAT)
    Radius = sqlalchemy.Column(sqlalchemy.INT)
    Goto = sqlalchemy.Column(sqlalchemy.VARCHAR)
    # Mission relationship
    MissionID: str = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("Missions.Number"))
    mission = orm.relation('Missions')


class Pins(SqlAlchemyBase):
    __tablename__ = 'Waypoints'
    __table_args__ = {'extend_existing': True}
    WaypointsID = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)
    MissionID = sqlalchemy.Column(sqlalchemy.INT)
    Name = sqlalchemy.Column(sqlalchemy.VARCHAR)
    Latitude = sqlalchemy.Column(sqlalchemy.FLOAT)
    Longitude = sqlalchemy.Column(sqlalchemy.FLOAT)
    Info = sqlalchemy.Column(sqlalchemy.TEXT)
    # Mission relationship
    MissionID: str = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("Missions.Number"))
    mission = orm.relation('Missions')


class Dives(SqlAlchemyBase):
    __tablename__ = 'DiveInfo'
    __table_args__ = {'extend_existing': True}
    DiveInfoID = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)
    GliderID = sqlalchemy.Column(sqlalchemy.INT)
    MissionID = sqlalchemy.Column(sqlalchemy.INT)
    DiveNo = sqlalchemy.Column(sqlalchemy.INT)
    Latitude = sqlalchemy.Column(sqlalchemy.FLOAT)
    Longitude = sqlalchemy.Column(sqlalchemy.FLOAT)
    # Mission relationship
    MissionID: str = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("Missions.Number"))
    mission = orm.relation('Missions')


class Missions(SqlAlchemyBase):
    __tablename__ = 'Missions'
    __table_args__ = {'extend_existing': True}
    MissionID = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)
    Number = sqlalchemy.Column(sqlalchemy.INT)
    Name = sqlalchemy.Column(sqlalchemy.VARCHAR)
    StartDate = sqlalchemy.Column(sqlalchemy.DATETIME)
    EndDate = sqlalchemy.Column(sqlalchemy.DATETIME)
    Info = sqlalchemy.Column(sqlalchemy.TEXT)
    # Targets relationship
    targets: List[Targets] = orm.relation("Targets", order_by=[
        Targets.TargetsID.asc(),
    ], back_populates='mission')
    # Waypoints relationship
    waypoints: List[Pins] = orm.relation("Pins", order_by=[
        Pins.WaypointsID.asc(),
    ], back_populates='mission')
    # Dives relationship
    dives: List[Dives] = orm.relation("Dives", order_by=[
        Dives.DiveInfoID.asc(),
    ], back_populates='mission')


class User(SqlAlchemyBase):
    __tablename__ = 'Users'
    UserID = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)
    Name = sqlalchemy.Column(sqlalchemy.VARCHAR(100))
    Email = sqlalchemy.Column(sqlalchemy.VARCHAR(100))
    HashedPassword = sqlalchemy.Column(sqlalchemy.VARCHAR(255))
    LastLogin = sqlalchemy.Column(sqlalchemy.DATETIME)
    CreatedDate = sqlalchemy.Column(sqlalchemy.DATETIME)


class Audit(SqlAlchemyBase):
    __tablename__ = 'Audit'
    LogID = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)
    UserID = sqlalchemy.Column(sqlalchemy.INT)
    Date = sqlalchemy.Column(sqlalchemy.DATETIME)
    Info = sqlalchemy.Column(sqlalchemy.TEXT)
