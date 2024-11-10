from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import Site
from sqlalchemy import desc, and_

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
        session.refresh(new_site)
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
            session.refresh(site)
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
    
    @db_session
    def select_page_list(session,do:Site,page: int,page_size: int,sorts: dict) -> list[Site]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(Site, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(Site, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(Site, key).desc())

        # 执行查询
        query = session.query(Site).filter(
            Site.id == do.id if do.id is not None else True,
            Site.site_name.contains(do.site_name) if do.site_name is not None else True,
            Site.site_description.contains(do.site_description) if do.site_description is not None else True,
            Site.created_id == do.created_id if do.created_id is not None else True,
            Site.modify_id == do.modify_id if do.modify_id is not None else True,
            Site.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:Site) -> int:
        query = session.query(Site).filter(
            Site.id == do.id if do.id is not None else True,
            Site.site_name.contains(do.site_name) if do.site_name is not None else True,
            Site.site_description.contains(do.site_description) if do.site_description is not None else True,
            Site.created_id == do.created_id if do.created_id is not None else True,
            Site.modify_id == do.modify_id if do.modify_id is not None else True,
            Site.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
