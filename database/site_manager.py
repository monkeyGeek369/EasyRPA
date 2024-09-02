from database.db_session import db_session
from database.models import Site
import datetime
from easyrpa.tools import request_tool 

@db_session
def add_site(site_name, site_description,session=None):
    new_site = Site(
        site_name=site_name,
        site_description=site_description,
        created_id=request_tool.get_current_header().user_id,
        created_time=datetime.now(),
        trace_id = request_tool.get_current_header().trace_id,
        is_active=True
    )
    session.add(new_site)
    session.commit()
    return new_site.id

@db_session
def update_site(site_id, site_name=None, site_description=None, is_active=None,session=None):
    site = session.query(Site).filter_by(id=site_id).first()
    if site:
        if site_name:
            site.site_name = site_name
        if site_description:
            site.site_description = site_description
        if is_active is not None:
            site.is_active = is_active
        site.modify_id = request_tool.get_current_header().user_id
        site.modify_time = datetime.now()
        site.trace_id = request_tool.get_current_header().trace_id
        session.commit()
        return site
    else:
        return None

@db_session
def delete_site(site_id,session=None):
    site = session.query(Site).filter_by(id=site_id).first()
    if site:
        session.delete(site)
        session.commit()
        return True
    else:
        return False

@db_session
def get_site(site_id,session=None):
    return session.query(Site).filter_by(id=site_id).first()

@db_session
def get_sites(session=None):
    return session.query(Site).all()
