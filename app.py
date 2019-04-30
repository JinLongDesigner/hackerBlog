import os
import sys
import time

from flask import (Flask, abort, flash, redirect, render_template, request,
                   url_for)

from exist import db
from models import Articles, project, Lab

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')
# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

@app.route('/')
@app.route('/home')
def homeView():
    articles = Articles.query.all()
    return render_template("home.html",articles=articles)

@app.route('/article/<string:article_id>')
def articleView(article_id):
    article = Articles.query.get(article_id)
    return render_template("article.html",article=article)

@app.route('/story')
def storyView():
    return render_template("story.html")

@app.route('/project')
def projectView():
    projects = []
    projects.append(project('dirmap'))
    projects.append(project('hackerblog'))
    return render_template("project.html",projects=projects)

@app.route('/lab')
def labView():
    labs = []
    labs.append(Lab('rmre','文本去重复工具'))
    labs.append(Lab('xsspayload','xss常用payload'))
    labs.append(Lab('xsshex','xss编码工具'))
    labs.append(Lab('base64','base64编解码工具'))
    labs.append(Lab('ujscanner','扫描器web UI'))
    return render_template("lab.html",labs=labs)

@app.route('/ujssec')
def ujssecView():
    return render_template("ujssec.html")

@app.route('/friend')
def friendView():
    return render_template("friend.html")

@app.route('/admin')
def adminArticlesView():
    test = Articles.query.all()
    return render_template("adminArticles.html",articles=test)

@app.route('/admin/add',methods=['GET','POST'])
def addArticleView():
    if request.method == 'POST':
        title = request.values.get("title")
        content = request.values.get("content")
        article = Articles(article_title=title,article_content=content)
        db.session.add(article)
        db.session.commit()
        flash('Add article succeed!')
        return redirect(url_for('adminArticlesView'))
    return render_template('adminAddArticle.html')

@app.route('/admin/edit/<string:article_id>',methods=['GET','POST'])
def editArticleView(article_id):
    article = Articles.query.get(article_id)
    if request.method == 'POST':
        article.article_title = request.values.get("title")
        article.article_content = request.values.get("content")
        db.session.commit()
        flash('Updated article succeed!')
        return redirect(url_for('adminArticlesView'))
    return render_template("adminEditArticle.html",article=article)

@app.route('/admin/del/<string:article_id>')
def deleteArticleView(article_id):
    article = Articles.query.get(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('Delete article succeed!')
    return redirect(url_for('adminArticlesView'))

@app.route('/login')
def login():
    return render_template('adminLogin.html')

#扫描器web ui
@app.route('/ujscanner')
def ujscanner():
    return render_template('ujscanner.html')

#小彩蛋
@app.route('/AreYouAHacker/<string:msg>')
def hackerMsg(msg):
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ip = request.remote_addr
    with open('msg.txt','a+',encoding='utf-8') as msg_file:
        msg_file.write('msg:{} ip:{} time:{}\n'.format(msg,ip,nowtime))
    return render_template('succeed.html',msg=msg)

#小工具
@app.route('/rmre')
def rmre():
    return render_template('rmre.html')

@app.route('/xsspayload')
def xsspayload():
    return render_template('xsspayload.html')

@app.route('/xsshex')
def xsshex():
    return render_template('xsshex.html')

@app.route('/base64')
def base64():
    return render_template('base64.html')

if __name__ == '__main__':
    app.run()
