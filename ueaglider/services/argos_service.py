from ueaglider.data.db_session import create_session
from ueaglider.data.db_classes import ArgosTags


def tag_nums() -> list:
    session = create_session()
    tags = session.query(ArgosTags.TagNumber) \
        .order_by(ArgosTags.TagNumber.desc()) \
        .all()
    session.close()
    return tags


def tag_info(tag_num):
    session = create_session()
    tag_instance = session.query(ArgosTags).filter(ArgosTags.TagNumber == tag_num).first()
    session.close()
    return tag_instance


def list_tags() -> list:
    session = create_session()
    tags = session.query(ArgosTags) \
        .order_by(ArgosTags.TagNumber.asc()) \
        .all()
    session.close()
    return tags