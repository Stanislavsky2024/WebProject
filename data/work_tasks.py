import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


work_task_to_group_work = sqlalchemy.Table(
    'work_task_to_group_work',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('work_tasks', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('work_tasks.id')),
    sqlalchemy.Column('group_works', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('group_works.id'))
)


class Work_task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'work_tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    text1 = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)
    text2 = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)

    def get_dict(self):
        return {'text1': self.text1, 'image': self.image, 'text2': self.text2, 'answer': self.answer}
