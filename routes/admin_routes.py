from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from common import utils
from common.profile import Profile
from forms.article_form import ArticleForm
from forms.image_upload_form import ImageUploadForm
from models.article import Article
from routes import app
from services.article_service import ArticleService
from services.image_service import ImageService


@app.route('/createarticle.html', methods=['GET', 'POST'])
@login_required
def create_article_page():
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = Article()
        new_article.title = form.title.data
        new_article.content = form.content.data

        try:
            article, error_msg = ArticleService().create_article(new_article)
            if error_msg:
                flash(message=f'发布文章错误:{error_msg}', category='danger')
            else:
                flash(message=f'发布文章完成', category='success')
                return redirect(url_for('home_page'))
        except Exception as error:
            flash(message=f'发布文章失败: {error}', category='danger')

    return render_template(template_name_or_list='editarticle.html', form=form, is_edit=False)


@app.route('/editarticle/<article_id>.html', methods=['GET', 'POST'])
@login_required
def edit_article_page(article_id: str):
    form = ArticleForm()
    if request.method == 'GET':
        try:
            article = ArticleService().get_article(int(article_id))
            if not article:
                flash(message=f'修改的文章不存在', category='danger')
                return redirect(url_for('home_page'))
            else:
                form.title.data = article.title
                form.content.data = article.content
        except Exception as ex:
            flash(massage=f'提取文件失败: {ex}', category='danger')
            return redirect(url_for('home_page'))

    if form.validate_on_submit():
        try:
            updated_article = Article()
            updated_article.id = int(article_id)
            updated_article.title = form.title.data
            updated_article.content = form.content.data

            article, error_msg = ArticleService().update_article(updated_article)
            if error_msg:
                flash(message=f'更新文章失败', category='danger')
            else:
                flash(message=f'更新文章成功', category='success')
                return redirect(url_for('home_page'))
            return redirect(url_for('home_page'))
        except Exception as error:
            flash(message=f'更新文章失败: {error}', category='danger')

    return render_template(template_name_or_list='editarticle.html', form=form, is_edit=True)


@app.route('/images.html', methods=['GET', 'POST'])
@login_required
def images_page():
    form = ImageUploadForm()

    if form.validate_on_submit():
        image_file = form.image_file.data

        images_path = Profile.get_images_path()
        image_filename = secure_filename(image_file.filename)
        image_fullpath = utils.get_save_filepaths(images_path, image_filename)

        image_file.save(image_fullpath)
        flash(message=f'上传图片成功: {image_fullpath}', category='success')

    image_filenames = ImageService().get_image_filename_list()

    return render_template(template_name_or_list='images.html', form=form, image_filenames=image_filenames)
