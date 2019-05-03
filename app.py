import os
import sys
import time
import queue

from flask import (Flask, abort, flash, redirect, render_template, request,
                   url_for)

from exist import db
from models import Articles, Project, Lab, ScannerConfig

from ujscanner.lib.controller.bruter import test
from ujscanner.lib.core.data import conf, paths

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
    projects.append(Project('dirmap'))
    projects.append(Project('hackerblog'))
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
@app.route('/ujscanner',methods=['GET','POST'])
def ujscanner():
    # 根目录
    paths.ROOT_PATH = os.getcwd()
    root_path = paths.ROOT_PATH
    # datapath
    paths.DATA_PATH = os.path.join(root_path, "data")
    paths.OUTPUT_PATH = os.path.join(root_path, "output")
    if not os.path.exists(paths.OUTPUT_PATH):
        os.mkdir(paths.OUTPUT_PATH)
    if not os.path.exists(paths.DATA_PATH):
        os.mkdir(paths.DATA_PATH)
    
    if request.method == 'POST':
        config_id = request.values.get("config")
        config = ScannerConfig.query.get(config_id)
        conf.recursive_scan = int(config.recursive_scan)
        conf.recursive_status_code = eval(config.recursive_status_code)
        conf.exclude_subdirs = config.exclude_subdirs
        conf.dict_mode = int(config.dict_mode)
        conf.dict_mode_load_single_dict = os.path.join(paths.DATA_PATH,config.dict_mode_load_single_dict)
        conf.dict_mode_load_mult_dict = os.path.join(paths.DATA_PATH,config.dict_mode_load_mult_dict)
        conf.blast_mode = int(config.blast_mode)
        conf.blast_mode_min = eval(config.blast_mode_min)
        conf.blast_mode_max = eval(config.blast_mode_max)
        conf.blast_mode_az = str(config.blast_mode_az)
        conf.blast_mode_num = str(config.blast_mode_num)
        conf.blast_mode_custom_charset = str(config.blast_mode_custom_charset)
        conf.blast_mode_resume_charset = str(config.blast_mode_resume_charset)
        conf.crawl_mode = int(config.crawl_mode)
        conf.crawl_mode_parse_robots = eval(config.crawl_mode_parse_robots)
        conf.crawl_mode_parse_html = str(config.crawl_mode_parse_html)
        conf.crawl_mode_dynamic_fuzz = eval(config.crawl_mode_dynamic_fuzz)
        conf.fuzz_mode = int(config.fuzz_mode)
        conf.fuzz_mode_load_single_dict = os.path.join(paths.DATA_PATH,config.fuzz_mode_load_single_dict)
        conf.fuzz_mode_load_mult_dict = os.path.join(paths.DATA_PATH,config.fuzz_mode_load_mult_dict)
        conf.fuzz_mode_label = eval(config.fuzz_mode_label)
        conf.request_headers = str(config.request_headers)
        conf.request_header_ua = str(config.request_header_ua)
        conf.request_header_cookie = str(config.request_header_cookie)
        conf.request_header_401_auth = str(config.request_header_401_auth)
        conf.request_method = str(config.request_method)
        conf.request_timeout = str(config.request_timeout)
        conf.request_delay = int(config.request_delay)
        conf.request_limit = int(config.request_limit)
        conf.request_max_retries = int(config.request_max_retries)
        conf.request_persistent_connect = int(config.request_persistent_connect)
        conf.redirection_302 = str(config.redirection_302)
        conf.file_extension = str(config.file_extension)
        conf.response_status_code = eval(config.response_status_code)
        conf.response_header_content_type = eval(config.response_header_content_type)
        conf.response_size = eval(config.response_size)
        conf.auto_check_404_page = eval(config.auto_check_404_page)
        conf.custom_503_page = str(config.custom_503_page)
        conf.custom_response_page = str(config.custom_response_page)
        conf.skip_size = str(config.skip_size)
        conf.proxy_server = str(config.proxy_server)
        conf.debug = int(config.debug)
        conf.update = int(config.update)
        #conf.target = request.values.get("singleTarget")
        conf.target = queue.Queue()
        target = 'http://testphp.vulnweb.com'
        conf.target.put(target)
        conf.target_nums = conf.target.qsize()
        test()

    return render_template('ujscanner.html')

#添加扫描配置接口
@app.route('/ujscanner/addScannerConfig',methods=['GET','POST'])
def addScannerConfig():
    if request.method == 'POST':
        recursive_scan = request.values.get("recursive_scan")
        recursive_status_code = request.values.get("recursive_status_code")
        exclude_subdirs = request.values.get("exclude_subdirs")
        dict_mode = request.values.get("dict_mode")
        dict_mode_load_single_dict = request.values.get("dict_mode_load_single_dict")
        dict_mode_load_mult_dict = request.values.get("dict_mode_load_mult_dict")
        blast_mode = request.values.get("blast_mode")
        blast_mode_min = request.values.get("blast_mode_min")
        blast_mode_max = request.values.get("blast_mode_max")
        blast_mode_az = request.values.get("blast_mode_az")
        blast_mode_num = request.values.get("blast_mode_num")
        blast_mode_custom_charset = request.values.get("blast_mode_custom_charset")
        blast_mode_resume_charset = request.values.get("blast_mode_resume_charset")
        crawl_mode = request.values.get("crawl_mode")
        crawl_mode_parse_robots = request.values.get("crawl_mode_parse_robots")
        crawl_mode_parse_html = request.values.get("crawl_mode_parse_html")
        crawl_mode_dynamic_fuzz = request.values.get("crawl_mode_dynamic_fuzz")
        fuzz_mode = request.values.get("fuzz_mode")
        fuzz_mode_load_single_dict = request.values.get("fuzz_mode_load_single_dict")
        fuzz_mode_load_mult_dict = request.values.get("fuzz_mode_load_mult_dict")
        fuzz_mode_label = request.values.get("fuzz_mode_label")
        request_headers = request.values.get("request_headers")
        request_header_ua = request.values.get("request_header_ua")
        request_header_cookie = request.values.get("request_header_cookie")
        request_header_401_auth = request.values.get("request_header_401_auth")
        request_method = request.values.get("request_method")
        request_timeout = request.values.get("request_timeout")
        request_delay = request.values.get("request_delay")
        request_limit = request.values.get("request_limit")
        request_max_retries = request.values.get("request_max_retries")
        request_persistent_connect = request.values.get("request_persistent_connect")
        redirection_302 = request.values.get("redirection_302")
        file_extension = request.values.get("file_extension")
        response_status_code = request.values.get("response_status_code")
        response_header_content_type = request.values.get("response_header_content_type")
        response_size = request.values.get("response_size")
        auto_check_404_page = request.values.get("auto_check_404_page")
        custom_503_page = request.values.get("custom_503_page")
        custom_response_page = request.values.get("custom_response_page")
        skip_size = request.values.get("skip_size")
        proxy_server = request.values.get("proxy_server")
        debug = request.values.get("debug")
        update = request.values.get("update")
        config = ScannerConfig(recursive_scan=recursive_scan,recursive_status_code=recursive_status_code,exclude_subdirs=exclude_subdirs,dict_mode=dict_mode,dict_mode_load_single_dict=dict_mode_load_single_dict,dict_mode_load_mult_dict=dict_mode_load_mult_dict,blast_mode=blast_mode,blast_mode_min=blast_mode_min,blast_mode_max=blast_mode_max,blast_mode_az=blast_mode_az,blast_mode_num=blast_mode_num,blast_mode_custom_charset=blast_mode_custom_charset,blast_mode_resume_charset=blast_mode_resume_charset,crawl_mode=crawl_mode,crawl_mode_parse_robots=crawl_mode_parse_robots,crawl_mode_parse_html=crawl_mode_parse_html,crawl_mode_dynamic_fuzz=crawl_mode_dynamic_fuzz,fuzz_mode=fuzz_mode,fuzz_mode_load_single_dict=fuzz_mode_load_single_dict,fuzz_mode_load_mult_dict=fuzz_mode_load_mult_dict,fuzz_mode_label=fuzz_mode_label,request_headers=request_headers,request_header_ua=request_header_ua,request_header_cookie=request_header_cookie,request_header_401_auth=request_header_401_auth,request_method=request_method,request_timeout=request_timeout,request_delay=request_delay,request_limit=request_limit,request_max_retries=request_max_retries,request_persistent_connect=request_persistent_connect,redirection_302=redirection_302,file_extension=file_extension,response_status_code=response_status_code,response_header_content_type=response_header_content_type,response_size=response_size,auto_check_404_page=auto_check_404_page,custom_503_page=custom_503_page,custom_response_page=custom_response_page,skip_size=skip_size,proxy_server=proxy_server,debug=debug,update=update)
        db.session.add(config)
        db.session.commit()
    return render_template('addScannerConfig.html')

#更新进度接口
@app.route('/ujscanner/updateProgress')
def updateProgress():
    pass

#查询进度接口
@app.route('/ujscanner/getProgress')
def getProgress():
    pass

#添加扫描结果接口
@app.route('/ujscanner/addResult')
def addResult():
    pass

#查询结果查询接口
@app.route('/ujscanner/getResult')
def getResult():
    pass

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
