import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Group_work(SqlAlchemyBase):
    __tablename__ = 'group_works'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    users_results = sqlalchemy.Column(sqlalchemy.String)
    max_result = sqlalchemy.Column(sqlalchemy.Integer)
    tasks = orm.relationship('Work_task', secondary='work_task_to_group_work', backref='group_works')

    def add_result(self, user_id, result):
        if self.users_results:
            self.users_results += ';' + user_id + '-' + result
        else:
            self.users_results = user_id + '-' + result

    def get_user_result(self, user_id):
        if self.users_results:
            users_results = self.users_results.split(';')
            for user_result in users_results:
                results = user_result.split('-')
                if results[0] == str(user_id):
                    return results[1]
        return None
    
    def remove_user_result(self, user_id):
        if self.users_results:
            back_res = []
            users_results = self.users_results.split(';')
            for user_result in users_results:
                results = user_result.split('-')
                if results[0] == str(user_id):
                    continue
                else:
                    back_res.append('-'.join(results))
            self.users_results = ';'.join(back_res)
