import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Variant(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'variants'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    difficulty = sqlalchemy.Column(sqlalchemy.String)
    tasks = orm.relationship('Task', secondary='task_to_variants', backref='variants')
