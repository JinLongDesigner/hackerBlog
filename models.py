import time
from exist import db

class project(object):
    def __init__(self,name):
        self.name = name

class Articles(db.Model):
    __tablename__ = 'articles'
    article_id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(100), nullable=False)
    article_content = db.Column(db.Text, nullable=False)
    article_date = db.Column(db.Text, default=time.strftime('%Y-%m-%d', time.localtime(time.time())))
