import sqlalchemy
from .db_session import SqlAlchemyBase


class Answers_work(SqlAlchemyBase):
    __tablename__ = 'answers_works'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_answers = sqlalchemy.Column(sqlalchemy.String)
    correct_answers = sqlalchemy.Column(sqlalchemy.String)
    max_points = sqlalchemy.Column(sqlalchemy.Integer)
    is_correct = sqlalchemy.Column(sqlalchemy.String)

    def add_answers(self, user_answer: str, correct_answer: str):
        if self.user_answers:
            self.user_answers += ';' + user_answer
            self.correct_answers += ';' + correct_answer
        else:
            self.user_answers = user_answer
            self.correct_answers = correct_answer
        if user_answer.lower() == correct_answer.lower():
            if self.is_correct:
                self.is_correct += ';' + '1'
            else:
                self.is_correct = '1'
        else:
            if self.is_correct:
                self.is_correct += ';' + '0'
            else:
                self.is_correct = '0'
    
    def get_result(self):
        total_points = 0
        correct_answers = 0
        total_answers = 0
        is_correct = self.is_correct.split(';')
        user_answers = self.user_answers.split(';')
        for i in range(len(is_correct)):
            if is_correct[i] == '1':
                correct_answers += 1
                total_points += 1
            if user_answers[i] != '-':
                total_answers += 1
        return {'total_points': total_points, 'total_answers': total_answers, 'correct_answers': correct_answers}
    
    def get_answers(self):
        result = []
        user_answers = self.user_answers.split(';')
        correct_answers = self.correct_answers.split(';')
        is_correct = self.is_correct.split(';')
        for i in range(len(user_answers)):
            result.append({'user_answer': user_answers[i], 'correct_answer': correct_answers[i],
                           'is_correct': is_correct[i]})
        return result
