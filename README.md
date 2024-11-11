# 基于Flask的Web应用开发

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