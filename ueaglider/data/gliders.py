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
    MissionID = sqlalchemy.Column(sqlalchemy.INT)
    Name = sqlalchemy.Column(sqlalchemy.VARCHAR)
    Latitude = sqlalchemy.Column(sqlalchemy.FLOAT)
    Longitude = sqlalchemy.Column(sqlalchemy.FLOAT)
    Radius = sqlalchemy.Column(sqlalchemy.INT)
    Goto = sqlalchemy.Column(sqlalchemy.VARCHAR)
    # Mission relationship
    MissionID: str = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("Missions.MissionID"))
    mission = orm.relation('Missions')


class Waypoints(SqlAlchemyBase):
    __tablename__ = 'Waypoints'
    __table_args__ = {'extend_existing': True}
    WaypointsID = sqlalchemy.Column(sqlalchemy.INT, primary_key=True, autoincrement=True)
    MissionID = sqlalchemy.Column(sqlalchemy.INT)
    Name = sqlalchemy.Column(sqlalchemy.VARCHAR)
    Latitude = sqlalchemy.Column(sqlalchemy.FLOAT)
    Longitude = sqlalchemy.Column(sqlalchemy.FLOAT)
    Info = sqlalchemy.Column(sqlalchemy.TEXT)
    # Mission relationship
    MissionID: str = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("Missions.MissionID"))
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
    MissionID: str = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("Missions.MissionID"))
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
    waypoints: List[Waypoints] = orm.relation("Waypoints", order_by=[
        Waypoints.WaypointsID.asc(),
    ], back_populates='mission')
    # Dives relationship
    dives: List[Dives] = orm.relation("Dives", order_by=[
        Dives.DiveInfoID.asc(),
    ], back_populates='mission')
