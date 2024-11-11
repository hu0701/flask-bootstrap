from models.article import Article
from routes import db
from sqlalchemy import Select


class ArticleService:

    def get_article(self, id):
        return db.session.get(Article, id)

    def get_articles(self):
        query = Select(Article)
        #return db.session.scalar(query).all()  踩坑 这里不能使用scalar
        return db.session.scalars(query).all()