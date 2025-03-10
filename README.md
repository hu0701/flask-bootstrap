# 基于Flask的Web应用开发

> 项目来源：

### 一、应用介绍及Flask安装

### 二、使用模板

### 三、连接MySQL数据库

#### 1、引入模块

> window是安装MySQL5.7
>
> https://blog.csdn.net/sunshine7058/article/details/138474991

requirements.txt文件追加模板

```shell
mysqlclient==2.2.0
SQLAlchemy==2.0.23
Flask-SQLAlchemy==3.1.1
```

#### 2、配置数据库连接参数

>https://docs.sqlalchemy.org/en/20/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqldb

`routes/__init__.py`

```pyton
mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
```

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../assets',
            static_url_path='/assets')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:root@127.0.0.1/myblog_db'
db = SQLAlchemy(app)

from routes import user_routes
from routes import admin_routes
```

#### 3、定义数据库映射类

`models/article.py`

```python
from datetime import datetime
from routes import db
from sqlalchemy import Integer, String, BLOB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column


class Article(db.Model):
    """
    踩坑，
    1、nullable参数写错
    2、格式不对齐
    """
    __tablename__ = 'articles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    __content: Mapped[bytes] = mapped_column(BLOB, name="content", nullable=False)
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    update_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    @property
    def content(self):
        return self.__content.decode('utf-8')
```

#### 4、前端渲染

`index.html`

```html
{% extends 'base.html' %}

{% block title %}
博客主页
{% endblock %}
<--! 拼写错误：在 index.html 文件中，你在循环部分写成了 acticles，应该是 articles。这个拼写错误会导致循环内容无法正确显示。 -->
{% block content %}
<table border="1">
    <tr>
        <th>标题</th>
        <th>时间</th>
    </tr>
    {% for article in  articles %}
    <tr>
        <td><a href="/article/{{ article.id }}.html">{{ article.title }}</a></td>
        <td>{{ article.create_time }}123</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
```



#### 效果：

![image-20241111105855269](image/image-20241111105855269.png)

![image-20241111105913309](image/image-20241111105913309.png)

![image-20241111105924574](image/image-20241111105924574.png)



### 四、实现用户登录

#### 1、添加新的模块

`requirements.txt`文件追加模板

```txt
flask-WTF==1.2.1
flask-login==0.6.3
```

#### 2、定义用户表的映射

`modele/user.py`

```python
from flask_login import UserMixin

from routes import db, login_manager
from sqlalchemy import Integer, String, BLOB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column



@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    fullname: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    def check_password_correction(self, attempted_password):
        return self.password == attempted_password

```

#### 3、增加login_manager的初始化

`routes/__init__.py`

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../assets',
            static_url_path='/assets')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:root@127.0.0.1/myblog_db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'  #初始化配置

db = SQLAlchemy(app)
login_manager = LoginManager(app)					#初始化实例

from routes import user_routes
from routes import admin_routes
```

#### 4、为User类增加对login_manage的支持

`modele/user.py`

```python
from datetime import datetime

from flask_login import UserMixin

from routes import db, login_manager
from sqlalchemy import Integer, String, BLOB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column



@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    fullname: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    def check_password_correction(self, attempted_password):
        return self.password == attempted_password
```



#### 5、编写表单类

`forms/login_form.py`

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(label="用户名:", validators=[DataRequired()])
    password = PasswordField(label="密码:", validators=[DataRequired()])
    submit = SubmitField(label="登陆")
```



#### 6、编写表单页面

`templates/login.html`

```html
{% extends 'base.html' %}
{% block title %}
博客主页
{% endblock %}

{% block content %}
<div class="container-xl">
    <form method="POST" class="form-signin">
        {{ form.hidden_tag() }}
        <h1 class="h3 mb-3 font-weight-normal">博客管理员登录</h1>

        {{ form.username.label }}
        {{ form.username(class="form-control", placeholder="输入用户名") }}

        {{ form.password.label }}
        {{ form.password(class="form-control", placeholder="输入密码") }}

        <br>

        {{ form.submit(class="btn btn-lg btn-primary btn-block") }}
    </form>
</div>
{% endblock %}
```



#### 7、添加路由追踪

`routes/user_route.py`

```python
······
@app.route('/login.html', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        result = UserService().do_login(username=form.username.data, password=form.password.data)
        if result:
            flash(f'欢迎{form.username.data}回来',category='success')
            return redirect(url_for('home_page'))
        else:
            flash(f'用户名或密码错误!',category='error')

    return render_template('login.html', form=form)
```



#### 	8、完成UserService的登陆支持

`service/user_service`

```python
from sqlalchemy import Select
from models.user import User
from routes import db
from flask_login import login_user



class UserService:
    def do_login(self, username: str, password: str)-> bool:
        query = Select(User).where(User.username == username)
        attempted_user = db.session.scalar(query)
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=password
        ):
            login_user(attempted_user)
            return True
        return False
```

![image-20250303132546948](image/image-20250303132546948.png)![image-20250303132603663](image/image-20250303132603663.png)![image-20250303132616735](image/image-20250303132616735.png)

### 五、登陆错误处理和退出

#### 1、增加显示提示的页面组件

`templates/base.html`

```html
    {% with messages = get_flashed_messages(with_categories=true) %}
     {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        {% endfor %}
    {% endif %}
    {% endwith %}
```

#### 2、添加路由

`routes/user_routes.py`

```python
@app.route('/logout.html')
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))
```

#### 3、显示按钮

`templates/base.html`

```html
        ·····
		{% if current_user.is_authenticated %}
        <ul class="navbar-nav">
            <li class="nav-item">
               <a class="nav-link" href="#">发布新文章</a>
            </li>
            <li class="nav-item">
               <a class="nav-link" href="{{ url_for('logout_page') }}">退出</a>
            </li>
        </ul>
        {% else %}
		·····
```

![image-20250303143611232](image/image-20250303143611232.png)

![image-20250303143622166](image/image-20250303143622166.png)

![image-20250303143652923](image/image-20250303143652923.png)

![image-20250303143707673](image/image-20250303143707673.png)

### 六、发布文章

#### 1、定义表单类

`forms/article_form.py`

```html
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    title = StringField(label="标题:", validators=[DataRequired()])
    content = TextAreaField(label="内容:", validators=[DataRequired()])
    submit = SubmitField(label="保持")
```



#### 2、定义添加文章表单页面

`templates/editarticle.html`

```html
{% extends 'base.html' %}
{% block title %}
博客主页
{% endblock %}
{% block content %}
<style>
    .content_height{
        height: 550px;
    }
</style>
<div class="container-fluid px-4 py-4">
    <form method="POST" class="form-signin">
        {{ form.hidden_tag() }}
        <h1 class="h3 mb-3 font-weight-normal">添加新文章</h1>
        <br>
            {{ form.title.label() }}
            {{ form.title(class="form-control", placeholder="请输入文章标题") }}
            {{ form.content.label() }}
            {{ form.content(class="form-control content_height", placeholder="请输入文章内容") }}
        </br>
        {{ form.submit(class="btn btn-lg btn-block btn-primary")}}
    </form>
</div>
{% endblock %}
```



#### 3、实现添加文章的service方法

`service/article_service.py`

```python
class ArticleService:

·····

    def create_article(self, article: Article):
        db.session.add(article)
        db.session.commit()
        return article
```



#### 4、添加文章的路由处理

`routes/admin_routes.py`

```python
from flask import render_template, url_for, redirect,flash
from flask_login import login_required

from forms.article_form import ArticleForm
from models.article import Article
from routes import app
from services.article_service import ArticleService


@app.route('/createarticle.html', methods=['GET','POST'])
@login_required
def create_article_page():
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = Article()
        new_article.title = form.title.data
        new_article.content = form.content.data

        try:
            ArticleService().create_article(new_article)
            flash(message=f'发布文章完成', category='success')
            return redirect(url_for('home_page'))
        except Exception as error:
            flash(message=f'发布文章失败: {error}', category='danger')


    return render_template(template_name_or_list='editarticle.html', form=form)
```



### 七、美化主页与修改文章

#### 1、美化主页

`templates/index.html`

```html
{% extends 'base.html' %}

{% block title %}
博客主页
{% endblock %}
{% block content %}
<div class="container-xl">
    <--! 拼写错误：在 index.html 文件中，你在循环部分写成了 acticles，应该是 articles。这个拼写错误会导致循环内容无法正确显示。 -->
    {% for article in articles %}
    <div class="card mb-4" style="background-color: #ecf2f9">
        <div class="card-header">
            <ul class="nav">
                <li class="nav-itme me-auto">
                    <a class="btn fs-5 fw-bold" href="/article/{{ article.id }}.html" >{{ article.title }}</a>
                </li>
                {% if current_user.is_authenticated %}
                <li class="nav-item px-a">
                    <small class="text-body-secondary">
                        <a class="btn" href="/editartical/{{ article.id }}.html">编辑</a>
                    </small>
                </li>
                {% endif %}
            </ul>
        </div>
        <div class="card-body">
            <p class="card-text">
                <a class="btn fs-6" href="/article/{{ article.id }}.html">{{ article.content }}</a>
            </p>
            <ul class="nav-item sm-auto">
                <small class="text-body-secondary">发布时间：{{ article.create_time }}</small>
            </ul>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

![image-20250308230024505](image/image-20250308230024505.png)



#### 2、编辑文章功能

##### 文章发布错误美化

`route/admin_route.py`

```python
@app.route('/createarticle.html', methods=['GET','POST'])
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
                flash(message=f'发布文章错误', category='danger')
            else:
                flash(message=f'发布文章完成', category='success')
                return redirect(url_for('home_page'))
        except Exception as error:
            flash(message=f'发布文章失败: {error}', category='danger')


    return render_template(template_name_or_list='editarticle.html', form=form)
```

![image-20250309005028652](image/image-20250309005028652.png)



##### 文章编辑

`route/admin_route.py`

```python
····
# 发布文章
@app.route('/createarticle.html', methods=['GET','POST'])
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

    return render_template(template_name_or_list='editarticle.html', form=form)



# 更新文章
@app.route('/editarticle/<article_id>.html', methods=['GET','POST'])
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
            flash(message=f'发布文章失败: {error}', category='danger')


    return render_template(template_name_or_list='editarticle.html', form=form)
```

`route/admin_service.py`

````python
····
	# 发布文章对数据库进行比对
    def create_article(self, article: Article):
        query = Select(Article).where(Article.title == article.title)
        # db.session.scalar和 db.session.execute。这里使用execute 有问题，无法判断是否查询到数据 所以使用scalar
        exit_article = db.session.scalar(query)
        if exit_article:
            return article, '同标题的文章已存在'

        db.session.add(article)
        db.session.commit()
        return article, None

    # 更新文章
    def update_article(self, article: Article):
        exit_article = db.session.get(Article, article.id)
        if not exit_article:
            return article, '文章不存在'
        # TODO: 检查同标题文章是否存在
        qury = Select(Article).where(and_(Article.title == article.title, Article.id != article.id))
        same_title_article = db.session.scalar(qury)
        if same_title_article :
            return article, '更新同标题的文章已存在'

        exit_article.title = article.title
        exit_article.content = article.content
        exit_article.update_time = func.now()
````

![image-20250309021643838](image/image-20250309021643838.png)



##### 动态修改编译页面的文章

`route/admin_route.py`

```python
····
# 发布文章
@app.route('/createarticle.html', methods=['GET','POST'])
@login_required
def create_article_page():
·····
	# 通过传递 is_edit参数判断编辑/更新
    return render_template(template_name_or_list='editarticle.html', form=form, is_edit=False)



# 更新文章
@app.route('/editarticle/<article_id>.html', methods=['GET','POST'])
@login_required
def edit_article_page(article_id: str):
····
	# 通过传递 is_edit参数判断编辑/更新
    return render_template(template_name_or_list='editarticle.html', form=form, is_edit=True)
```



`templates/editarticle.html`

```html
{% extends 'base.html' %}
{% block title %}
    博客主页-
    {% if is_edit %}
        编辑文章
    {% else %}
        添加新文章
    {% endif %}
{% endblock %}
{% block content %}
<style>
    .content_height{
        height: 550px;
    }
</style>
<div class="container-fluid px-4 py-4">
    <form method="POST" class="form-signin">
        {{ form.hidden_tag() }}
        <h1 class="h3 mb-3 font-weight-normal">
            {% if is_edit %}
                编辑文章
            {% else %}
                添加新文章
            {% endif %}
            </h1>
            <br>
            {{ form.title.label() }}
            {{ form.title(class="form-control", placeholder="请输入文章标题") }}
            {{ form.content.label() }}
            {{ form.content(class="form-control content_height", placeholder="请输入文章内容") }}
        </br>
        {{ form.submit(class="btn btn-lg btn-block btn-primary")}}
    </form>
</div>
{% endblock %}
```

![image-20250309023016769](image/image-20250309023016769.png)



![image-20250309023016769](image/image-20250309023055656.png)





### 八、删除文章

#### 1、增加删除功能按钮

`templates/index.html`

```html
            ·····
				{% if current_user.is_authenticated %}
            ·····
                <li  class="nav-item px-1">
                    <small class="text-body-secondary">
                        <a class="btn" data-bs-toggle="modal" data-bs-target="#Mdal-DeleteConfirm-{{ article.id }}">删除</a>
                    </small>
                </li>
                {% endif %}
```



#### 2、定义删除文章表单类

新增`forms/delete_article_form.py`

```python
from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField
from wtforms.validators import DataRequired


class DeleteArticleForm(FlaskForm):
    article_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField(label='删除')
```



#### 3、增加确认删除对话框

新增`templates/includes/article_modals.html`

```html
<!-- 删除文章确认页 -->
<div class="modal fade" id="Modal-DeleteConfirm-{{ article.id }}" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
    <dev class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="deleteModalLabel">{{ article.title }}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form method="POST">
                {{ delete_article_form.csrf_token }}
                {{ delete_article_form.article_id(value=article.id) }}
                <div class="modal-body">
                    <h4 class="text-center">确定要删除"{{ article.title }}"吗？</h4>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                    <button type="button" class="btn btn-primary">确定</button>
                </div>
            </form>
        </div>
    </dev>
</div>
```



#### 4、引入确认删除对话框

`templates/index.html`

```html
<div class="container-xl">
        <!-- 拼写错误：在 index.html 文件中，你在循环部分写成了 acticles，应该是 articles。这个拼写错误会导致循环内容无法正确显示。 -->
    {% for article in articles %}
     <!-- 引入确认删除对话框 --> 
    {% if current_user.is_authenticated %}
        {% include 'includes/article_modals.html' %}
    {% endif %}
```



#### 5、在service类中添加删除文章的业务逻辑

`service/article_service.py`

```python
·······
	def delete_article(self, article_id: int):
        article = db.session.get(Article, article_id)
        if article:
            db.session.delete(article)
            db.session.commit()
            return article, None
        else:
            return False, '文章不存在'
```



#### 6、路由处理中添加删除逻辑

`routes/user_routes.py`

```python
@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def home_page():
    if current_user.is_authenticated:
        delete_article_form = DeleteArticleForm()
        if delete_article_form.validate_on_submit():
            if delete_article_form.validate_on_submit():
                result, error = ArticleService().delete_article(int(delete_article_form.article_id.data))
                if result:
                    flash(message=f'删除文章成功', category='success')
                    return redirect(url_for('home_page'))
                else:
                    flash(message=f'删除文章成功', category='danger')

        articles = ArticleService().get_articles()
        if current_user.is_authenticated:
            return render_template(template_name_or_list='index.html', articles=articles, delete_article_form=delete_article_form)
        return render_template(template_name_or_list='index.html', articles=articles)
```

![image-20250309234652420](image/image-20250309234652420.png)

![image-20250309234702325](image/image-20250309234702325.png)



### 九、引入Markdown来显示文章

#### 1、下载showdownjs

>https://github.com/showdownjs/showdown/tree/master/dist
>
>下载 `showdown.min.js` 和 `showdown.min.js.map` 文件夹；放置 `assets/plugins/showdownjs-2.0.0`



#### 2、引入showdownjs与自定义markdown的一些显示样式

`templates/base.html`

```html
 	·····
	<script src="/assets/plugins/showdownjs-2.0.0/showdown.min.js"></script>
    <style>
        pre {
            white-space: pre-wrap;          /* css-3 */
            white-space: -moz-pre-wrap;     /* Mozilla, since 1999 */
            white-space: pre-wrap;          /* Opera 4-6 */
            white-space: -o-pre-wrap;       /* Opera 7 */
            word-wrap: break-word;          /* Internet Explorer 5.5+ */
            background-color: #f8f8f8;
            border: 1px solid #dfdfdf;
            margin-top: 1.5em;
            margin-bottom: 1.5em;
            padding: 1.25rem 0.3125rem 0.0625rem;
        }

        pre code {
            background-color: transparent;
            border: 0;
            padding: 0;
        }
    </style>
	·····
```



#### 3、调试文章显示页面的内容支持markdown

`templates/article.html`

```html
{% extends 'base.html' %}

{% block title %}
博客 -{{ article.title }}
{% endblock %}

{% block content %}
<textarea id="article_content" style="display: none;">{{ article.content }}</textarea>
<div class="container-xl">
    <h4><p class="text-center" style="margin-top: 20px;">{{ article.title }}</p></h4>
    <p class="text-center" style="margin-top: 10px;">最后更新： {{ article.update_time }}</p>
    <p id="article_viewer"></p>
</div>
<script src="/assets/js/article.js"></script>"
{% endblock %}
```



#### 4、编写自己的js来使用markdown

`/assets/js/article.js`

```javascript
$(function (){
    var converter = new showdown.Converter();
    var article_html = converter.makeHtml($('#article_content').val())
    $('#article_content').html(article_html)
})
```

![image-20250310181911220](image/image-20250310181911220.png)

![image-20250310181922805](image/image-20250310181922805.png)



Git

```git
$ git status
On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   .idea/workspace.xml
        new file:   assets/js/article.js

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   .idea/misc.xml
        modified:   .idea/myblog.iml
        modified:   .idea/workspace.xml
        modified:   README.md
        modified:   assets/js/article.js
        modified:   templates/article.html
        modified:   templates/base.html

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        assets/plugins/showdownjs-2.0.0/
        image/image-20250310181911220.png
        image/image-20250310181922805.png

```

