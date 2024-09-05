from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import Site
from datetime import datetime
from easyrpa.tools import request_tool 

class SiteDbManager:
    @db_session
    def add_site(session,site_name, site_description):
        # 不可以创建已经存在的site_name
        if session.query(Site).filter(Site.site_name == site_name).first():
            raise ValueError("Site name already exists")
        new_site = Site(
            site_name=site_name,
            site_description=site_description
        )
        create_common_fields(new_site)
        session.add(new_site)
        session.commit()
        return new_site.id

    @db_session
    def update_site(session,site_id, site_name=None, site_description=None, is_active=None):
        site = session.query(Site).filter_by(id=site_id).first()
        # 名称不可以修改为出了自己之外的与其它site相同
        if site_name and session.query(Site).filter(Site.site_name == site_name).filter(Site.id != site_id).first():
            raise ValueError("Site name already exists")

        if site:
            if site_name:
                site.site_name = site_name
            if site_description:
                site.site_description = site_description
            if is_active is not None:
                site.is_active = is_active
            update_common_fields(site)
            session.commit()
            return site
        else:
            return None

    @db_session
    def delete_site(session,site_id):
        site = session.query(Site).filter_by(id=site_id).first()
        if site:
            session.delete(site)
            session.commit()
            return True
        else:
            return False

    @db_session
    def get_site(session,site_id):
        return session.query(Site).filter_by(id=site_id).first()

    @db_session
    def get_sites(session):
        return session.query(Site).all()
