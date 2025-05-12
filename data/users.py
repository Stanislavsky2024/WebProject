import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.String, 
                                     default=datetime.datetime.now)
    profile_pics = sqlalchemy.Column(sqlalchemy.String, default='/static/profile_pics/default.png')
    groups = orm.relationship("Group", secondary="user_to_group", backref="users")
    groups_participant = sqlalchemy.Column(sqlalchemy.String, default='')
    is_teacher = sqlalchemy.Column(sqlalchemy.Boolean)
    solved_tasks_ids = sqlalchemy.Column(sqlalchemy.String, default='')
    solved_variants = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def add_group_participant(self, group_id):
        if str(group_id) in self.groups_participant.split(';'):
            return
        for group in self.groups:
            if int(group_id) == group.user_id:
                return
        if self.groups_participant == '':
            self.groups_participant = str(group_id)
        else:
            self.groups_participant += ';' + str(group_id)
    
    def get_group_participant(self):
        if self.groups_participant == '':
            return None
        else:
            return self.groups_participant.split(';')
    
    def remove_group_participant(self, group_id):
        if str(group_id) not in self.groups_participant:
            return
        result = self.groups_participant.split(';')
        result.remove(str(group_id))
        if result:
            self.groups_participant = ';'.join(result)
        else:
            self.groups_participant = ''
    
    def add_solved_task(self, task_id):
        if str(task_id) in self.solved_tasks_ids.split(';'):
            return
        if self.solved_tasks_ids:
            self.solved_tasks_ids += ';' + str(task_id)
        else:
            self.solved_tasks_ids = str(task_id)
    
    def add_solved_variant(self):
        self.solved_variants += 1
