from ueaglider.data.db_session import create_session
from ueaglider.data.db_classes import Gliders, Dives

non_uea_gliders = [503, 539, 546, 566, 533, 565, 524, 999, 532, 534, 550, 602, 621, 643, 640]
not_gliders = [999]


def get_glider_count() -> int:
    session = create_session()
    gliders = session.query(Gliders).filter(Gliders.Number.notin_(non_uea_gliders)).count()
    session.close()
    return gliders


def glider_nums() -> list:
    session = create_session()
    gliders = session.query(Gliders.Number) \
        .order_by(Gliders.Number.desc()) \
        .all()
    session.close()
    return gliders


def list_gliders(non_uea=False) -> dict:
    session = create_session()
    if non_uea:
        gliders = session.query(Gliders) \
            .filter(Gliders.Number.in_(non_uea_gliders)) \
            .filter(Gliders.Number.notin_(not_gliders)) \
            .order_by(
            Gliders.Number.asc()).all()
    else:
        gliders = session.query(Gliders) \
            .filter(Gliders.Number.notin_(non_uea_gliders)) \
            .order_by(Gliders.Number.asc()) \
            .all()
    session.close()
    return gliders


def glider_info(glider_num):
    session = create_session()
    glider_instance = session.query(Gliders).filter(Gliders.Number == glider_num).first()
    mission_ids_list = []
    for value in session.query(Dives.MissionID) \
            .filter(Dives.GliderID == glider_instance.GliderID) \
            .distinct():
        mission_ids_list.append(value[0])
    session.close()
    return glider_instance, mission_ids_list
