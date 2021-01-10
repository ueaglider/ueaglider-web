from typing import Optional, Any

from ueaglider.data.db_session import create_session
from ueaglider.data.gliders import Gliders, Missions, Dives, Targets


def get_glider_count() -> int:
    session = create_session()
    return session.query(Gliders).count()


def get_mission_count() -> int:
    session = create_session()
    return session.query(Missions).count()


def get_dive_count() -> int:
    session = create_session()
    return session.query(Dives).count()


def list_missions() -> dict:
    session = create_session()
    missions = session.query(Missions).order_by(Missions.MissionID.desc()).all()
    session.close()
    return missions


def get_mission_by_id(mission_id):
    if not mission_id:
        return None
    session = create_session()
    mission = session.query(Missions).filter(Missions.MissionID == mission_id).first()
    session.close()
    return mission


def get_mission_targets(mission_id) -> Optional[Any]:
    if not mission_id:
        return None

    mission_id = int(mission_id)

    session = create_session()

    targets = session.query(Targets) \
        .filter(Targets.MissionID == mission_id) \
        .all()

    session.close()
    lon, lat, name = [], [], []
    for target in targets:
        lon.append(target.Longitude)
        lat.append(target.Latitude)
        name.append(target.Name)

    return targets


def targets_to_json(targets) -> dict:
    features = []
    for i, target in enumerate(targets):
        tgt_popup = "Target: " + target.Name + "<br>Lat: " + str(target.Latitude) + "<br>Lon: " + str(
            target.Longitude) + "<br>GOTO: " + target.Goto + "<br>Raduis: " + str(target.Radius) + ' m'
        target_item = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    target.Longitude,
                    target.Latitude
                ]
            },
            "type": "Feature",
            "properties": {
                "popupContent": tgt_popup
            },
            "id": i
        }
        features.append(target_item)

    tgtdict = {
        "type": "FeatureCollection",
        "features": features
    }
    return tgtdict
