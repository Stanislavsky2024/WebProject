import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

task_to_variants = sqlalchemy.Table(
    'task_to_variants',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('tasks', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tasks.id')),
    sqlalchemy.Column('variants', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('variants.id'))
)

task_to_random_variants = sqlalchemy.Table(
    'task_to_random_variants',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('tasks', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tasks.id')),
    sqlalchemy.Column('random_variants', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('random_variants.id'))
)


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer)
    difficulty = sqlalchemy.Column(sqlalchemy.String)
    task_id = sqlalchemy.Column(sqlalchemy.Integer)
    type = sqlalchemy.Column(sqlalchemy.String)
    text1 = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)
    text2 = sqlalchemy.Column(sqlalchemy.String)
    solution = sqlalchemy.Column(sqlalchemy.String)
    answer = sqlalchemy.Column(sqlalchemy.String)

    def get_dict(self):
        return {'number': self.number, 'difficulty': self.difficulty, 'task_id': self.task_id,
                'type': self.type, 'text1': self.text1, 'image': self.image, 'text2': self.text2,
                'solution': self.solution, 'answer': self.answer}
