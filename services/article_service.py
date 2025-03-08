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

    def create_article(self, article: Article):
        db.session.add(article)
        db.session.commit()
        return article

    # def delete_article(self, id):
    #     article = db.session.get(Article, id)
    #     db.session.delete(article)
    #     db.session.commit()
    #     return article
    #
    # def update_article(self, id, article):
    #     article = db.session.get(Article, id)
    #     article.title = article.title
    #     article.content = article.content
    #     db.session.commit()
    #     return article