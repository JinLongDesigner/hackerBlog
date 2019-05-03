import time
import uuid
import json
from flask_login import UserMixin

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from exist import db
from ujscanner.lib.core.data import conf

class ScannerConfig(db.Model):
    __talbename__ = 'ScannerConfig'
    config_id = db.Column(db.Integer, primary_key=True)
    #Recursive scan options
    #[RecursiveScan]
    #recursive scan:Close:0;Open:1
    recursive_scan = db.Column(db.Text, default='0')
    recursive_status_code = db.Column(db.Text, default='[301,403]')
    #The directory does not scan
    #exclude_subdirs = ['/test1','/test2']
    exclude_subdirs = db.Column(db.Text, default='')

    #Processing scan mode
    #[ScanModeHandler]
    #Dict mode:Close :0;single dict:1;multiple dict:2
    dict_mode = db.Column(db.Text, default='1')
    #Single dictionary file path
    dict_mode_load_single_dict = db.Column(db.Text, default='dict_mode_dict.txt')
    #Multiple dictionary file path
    dict_mode_load_mult_dict = db.Column(db.Text, default='dictmult')
    #Blast mode:tips:Use "file_extension" options for suffixes
    blast_mode = db.Column(db.Text, default='0')
    #Minimum length of character set
    blast_mode_min = db.Column(db.Text, default='3')
    #Maximum length of character set
    blast_mode_max = db.Column(db.Text, default='3')
    #The default character set:a-z
    blast_mode_az = db.Column(db.Text, default='abcdefghijklmnopqrstuvwxyz')
    #The default character set:0-9
    blast_mode_num = db.Column(db.Text, default='0123456789')
    #Custom character set
    blast_mode_custom_charset = db.Column(db.Text, default='abc')
    #Custom continue to generate blast dictionary location
    blast_mode_resume_charset = db.Column(db.Text, default='')
    #Crawl mode:Close :0;Open:1
    crawl_mode = db.Column(db.Text, default='0')
    #Parse robots.txt file
    crawl_mode_parse_robots = db.Column(db.Text, default='0')
    #An xpath expression used by a crawler to parse an HTML document
    crawl_mode_parse_html = db.Column(db.Text, default='//*/@href | //*/@src | //form/@action')
    #Whether to turn on the dynamically generated payloads:close:0;open:1
    crawl_mode_dynamic_fuzz = db.Column(db.Text, default='1')
    #Fuzz mode:Close :0;single dict:1;multiple dict:2
    fuzz_mode = db.Column(db.Text, default='0')
    #Single dictionary file path.You can customize the dictionary path. The labels are just a flag for insert dict.
    fuzz_mode_load_single_dict = db.Column(db.Text, default='fuzz_mode_dir.txt')
    #Multiple dictionary file path
    fuzz_mode_load_mult_dict = db.Column(db.Text, default='fuzzmult')
    #Set the label of fuzz.e.g:{dir};{ext}
    #fuzz_mode_label = db.Column(db.Text, default='')
    fuzz_mode_label = db.Column(db.Text, default='{dir}')

    #Processing payloads
    #[PayloadHandler]

    #Processing requests
    #[RequestHandler]
    #Custom request header.e.g:test1=test1,test2=test2
    request_headers = db.Column(db.Text, default='')
    #Custom request user-agent
    request_header_ua = db.Column(db.Text, default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
    #Custom request cookie.e.g:cookie1=cookie1; cookie2=cookie2;
    request_header_cookie = db.Column(db.Text, default='')
    #Custom 401 certification
    request_header_401_auth = db.Column(db.Text, default='')
    #Custom request methods (get, head)
    request_method = db.Column(db.Text, default='get')
    #Custom per request timeout in x sec.
    request_timeout = db.Column(db.Text, default='3')
    #Custom per request delay random(0-x) secends.The parameter must be an integer.
    request_delay = db.Column(db.Text, default='0')
    #Custom all request limit,default 30 coroutines
    request_limit = db.Column(db.Text, default='30')
    #Custom request max retries
    request_max_retries = db.Column(db.Text, default='1')
    #Whether to open an HTTP persistent connection
    request_persistent_connect = db.Column(db.Text, default='0')
    #Whether to follow 302 redirection
    redirection_302 = db.Column(db.Text, default='False')
    #Payload add file extension
    file_extension = db.Column(db.Text, default='')

    #Processing responses
    #[ResponseHandler]
    #Sets the response status code to record
    response_status_code = db.Column(db.Text, default='[200]')
    #Whether to record content-type
    response_header_content_type = db.Column(db.Text, default='1')
    #Whether to record page size
    response_size = db.Column(db.Text, default='1')
    #Auto check 404 page
    auto_check_404_page = db.Column(db.Text, default='True')
    #Custom 503 page regex
    custom_503_page = db.Column(db.Text, default='page 503')
    #Custom regular match response content
    custom_response_page = db.Column(db.Text, default='([0-9]){3}([a-z]){3}test')
    #Skip files of size x bytes.you must be set "None",if don't want to skip any file.e.g:None;0b;1k;1m
    skip_size = db.Column(db.Text, default='None')

    #Processing proxy
    #[ProxyHandler]
    #proxy:e.g:{"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}
    #proxy_server = db.Column(db.Text, default='')
    proxy_server = db.Column(db.Text, default='None')

    #Debug option
    #[DebugMode]
    #Print payloads and exit the program
    debug = db.Column(db.Text, default='0')

    #update option
    #[CheckUpdate]
    #Get the latest code from github(Not yet available)
    update = db.Column(db.Text, default='0')
        
class Project(object):
    def __init__(self,name):
        self.name = name

class Lab(object):
    def __init__(self,name,introduce):
        self.name = name
        self.introduce = introduce
class Articles(db.Model):
    __tablename__ = 'Articles'
    article_id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(100), nullable=False)
    article_content = db.Column(db.Text, nullable=False)
    article_date = db.Column(db.Text, default=time.strftime('%Y-%m-%d', time.localtime(time.time())))

PROFILE_FILE = "admin.txt"
class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.password_hash = self.get_password_hash()
        self.id = self.get_id()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """save user name, id and password hash to json file"""
        self.password_hash = generate_password_hash(password)
        with open(PROFILE_FILE, 'w+') as f:
            try:
                profiles = json.load(f)
            except ValueError:
                profiles = {}
            profiles[self.username] = [self.password_hash,
                                       self.id]
            f.write(json.dumps(profiles))

    def verify_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_password_hash(self):
        """try to get password hash from file.

        :return password_hash: if the there is corresponding user in
                the file, return password hash.
                None: if there is no corresponding user, return None.
        """
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                user_info = user_profiles.get(self.username, None)
                if user_info is not None:
                    return user_info[0]
        except IOError:
            return None
        except ValueError:
            return None
        return None

    def get_id(self):
        """get user id from profile file, if not exist, it will
        generate a uuid for the user.
        """
        if self.username is not None:
            try:
                with open(PROFILE_FILE) as f:
                    user_profiles = json.load(f)
                    if self.username in user_profiles:
                        return user_profiles[self.username][1]
            except IOError:
                pass
            except ValueError:
                pass
        return str(uuid.uuid4())

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not user_id:
            return None
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                for user_name, profile in user_profiles.items():
                    if profile[1] == user_id:
                        return User(user_name)
        except:
            return None
        return None
