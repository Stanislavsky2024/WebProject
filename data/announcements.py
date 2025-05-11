import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Announcement(SqlAlchemyBase):
    __tablename__ = 'announcements'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.String)
    group = orm.relationship('Group', back_populates='announcement')
