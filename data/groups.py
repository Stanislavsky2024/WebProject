import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from data.users import User
from data import db_session
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer

user_to_group = sqlalchemy.Table(
    'user_to_group',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('groups', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('groups.id'))
)

group_to_group_work = sqlalchemy.Table(
    'group_to_group_work',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('group_works', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('group_works.id')),
    sqlalchemy.Column('groups', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('groups.id'))
)


class Group(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    members = sqlalchemy.Column(sqlalchemy.String, default='')
    link = sqlalchemy.Column(sqlalchemy.String)
    announcement_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('announcements.id'))
    announcement = orm.relationship('Announcement')
    group_works = orm.relationship('Group_work', secondary='group_to_group_work', backref='groups')

    def add_member(self, user_id):
        if str(user_id) in self.members.split(';') or user_id == self.user_id:
            return
        if self.members == '':
            self.members = str(user_id)
        else:
            self.members += ';' + str(user_id)

    def check_member(self, user_id):
        if str(user_id) in self.members.split(';') or user_id == self.user_id:
            return True
        return False

    def remove_member(self, user_id):
        if str(user_id) in self.members.split(';'):
            result = self.members.split(';')
            result.remove(str(user_id))
            if result:
                self.members = ';'.join(result)
            else:
                self.members = ''

    def get_creator(self):
        db_sess = db_session.create_session()
        user = db_sess.get(User, self.user_id)
        return {'name': user.name, 'surname': user.surname, 'picture': user.profile_pics, 'id': user.id}

    def get_members(self):
        db_sess = db_session.create_session()
        members = []
        if self.members != '':
            for id in self.members.split(';'):
                try:
                    user = db_sess.get(User, id)
                    members.append({'name': user.name, 'surname': user.surname, 'picture': user.profile_pics})
                except TypeError:
                    members.append({'name': '???', 'surname': '???', 'picture': '/static/profile_pics/default.png'})
        return members

    def create_token(self):
        db_sess = db_session.create_session()
        serializer = URLSafeTimedSerializer('secret')
        token = serializer.dumps({'group_id': db_sess.query(Group).filter(Group.name == self.name,
                                                                          Group.user_id == self.user_id).first().id})
        self.link = token

    @staticmethod
    def verify_token(token: str):
        serializer = URLSafeTimedSerializer('secret')
        try:
            group_id = serializer.loads(token)['group_id']
        except TypeError:
            return None
        db_sess = db_session.create_session()
        return db_sess.query(Group).filter(group_id == Group.id).first().id
