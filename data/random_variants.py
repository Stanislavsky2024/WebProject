import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Random_variant(SqlAlchemyBase):
    __tablename__ = 'random_variants'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    tasks = orm.relationship('Task', secondary='task_to_random_variants', backref='random_variants')
