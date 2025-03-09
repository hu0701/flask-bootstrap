from models.article import Article
from routes import db
from sqlalchemy import Select, func, and_


class ArticleService:

    def get_article(self, id):
        return db.session.get(Article, id)

    def get_articles(self):
        query = Select(Article)
        #return db.session.scalar(query).all()  踩坑 这里不能使用scalar
        return db.session.scalars(query).all()

    def create_article(self, article: Article):
        query = Select(Article).where(Article.title == article.title)
        # db.session.scalar和 db.session.execute。这里使用execute 有问题，无法判断是否查询到数据 所以使用scalar
        exit_article = db.session.scalar(query)
        if exit_article:
            return article, '同标题的文章已存在'

        db.session.add(article)
        db.session.commit()
        return article, None

    def update_article(self, article: Article):
        exit_article = db.session.get(Article, article.id)
        if not exit_article:
            return article, '文章不存在'
        # TODO: 检查同标题文章是否存在
        # if exit_article.title != article.title: # 如果标题被修改了
        #     query = Select(Article).where(Article.title == article.title)
        #     exit_article = db.session.scalar(query)
        #     if exit_article:
        #         return article, '更新同标题的文章已存在'
        # else:
        #     exit_article.title = article.title
        #     exit_article.content = article.content
        #     exit_article.update_time = func.now()

        # TODO: 检查同标题文章是否存在
        qury = Select(Article).where(and_(Article.title == article.title, Article.id != article.id))
        same_title_article = db.session.scalar(qury)
        if same_title_article :
            return article, '更新同标题的文章已存在'

        exit_article.title = article.title
        exit_article.content = article.content
        exit_article.update_time = func.now()

        db.session.commit()
        return article , None

    def delete_article(self, article_id: int):
        article = db.session.get(Article, article_id)
        if article:
            db.session.delete(article)
            db.session.commit()
            return article, None
        else:
            return False, '文章不存在'