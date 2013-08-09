#!/usr/bin/python2.7
# http://flask.pocoo.org/docs/quickstart/
# http://flask.pocoo.org/docs/api/
from flask import Flask, request, json, jsonify, Response, abort, redirect, url_for,make_response,current_app
from api import User,Feed,Notification
from werkzeug.exceptions import default_exceptions, HTTPException
from functools import wraps,update_wrapper
import conn, logging, sys, os 
from datetime import timedelta 

# def crossdomain(origin=None, methods=None, headers=None,
                # max_age=21600, attach_to_all=True,
                # automatic_options=True):
	# if methods is not None:
		# methods = ', '.join(sorted(x.upper() for x in methods))
	# if headers is not None and not isinstance(headers, basestring):
		# headers = ', '.join(x.upper() for x in headers)
	# if not isinstance(origin, basestring):
		# origin = ', '.join(origin)
	# if isinstance(max_age, timedelta):
		# max_age = max_age.total_seconds()

	# def get_methods():
		# if methods is not None:
			# return methods

		# options_resp = current_app.make_default_options_response()
		# return options_resp.headers['allow']

	# def decorator(f):
		# def wrapped_function(*args, **kwargs):
			# print "in  decorator"
			# if automatic_options and request.method == 'OPTIONS':
				# resp = current_app.make_default_options_response()
			# else:
				# resp = make_response(f(*args, **kwargs))
			# if not attach_to_all and request.method != 'OPTIONS':
				# return resp

			# h = resp.headers

			# h['Access-Control-Allow-Origin'] = origin
			# h['Access-Control-Allow-Methods'] = get_methods()
			# h['Access-Control-Max-Age'] = str(max_age)
			# if headers is not None:
				# h['Access-Control-Allow-Headers'] = headers
			# return resp

		# f.provide_automatic_options = False
		# f.required_methods = ['OPTIONS']
		# return update_wrapper(wrapped_function, f)
	# return decorator


#http://flask.pocoo.org/snippets/8/
def check_auth(email, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    # app.logger.info("in check auth {} , {}".format(email,password))
    user = User()
    ret = user.login(db.connection,email,password)
    #app.logger.info(ret.haserrors)
    #app.logger.info(ret.result)
    return ret.result

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
		auth = request.authorization
		# app.logger.info("inside requires_auth")
		# app.logger.info(auth.username)
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		kwargs['email'] = auth.username
		return f(*args, **kwargs)
    return decorated	

#http://flask.pocoo.org/snippets/45/
def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

#http://flask.pocoo.org/snippets/83/
def make_rest_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_rest_error(ex):
	# app.logger.info("in make rest error")
	# app.logger.info(str(ex))
	if request_wants_json():
		response = jsonify(message=str(ex))
	else:
		response = Response('<message>{}</message>'.format(str(ex)))
        
	response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_rest_error

    return app

# todo: support for returning XML (currently its shortcut)
def buildresponse(notobj,opts):
	if request_wants_json():
		response = jsonify(success=not notobj.haserrors,
						errors = notobj.errors,
						result= notobj.result)
	else:
		response = Response("<response><success>{}</success><result>{}</result><error>{}</error></response>".format(not notobj.haserrors, 
					notobj.result,'</error><error>'.join(notobj.errors)),mimetype="text/xml")

	if opts.get('location') is not None:
		response.headers['Location'] = opts['location']
		
	if opts.get('http_status') is not None:
		response.status_code = opts['http_status']
	else:
		if notobj.haserrors:
			response.status_code = 409
			
	return response

app = make_rest_app(__name__)
defpath = '/api'
app.secret_key = "sfdusyfsyf37487347hijehfjshfksf983843"
db = conn.dbcon(app) 

# define routes
# https://en.wikipedia.org/wiki/Representational_state_transfer
# Flask+REST, http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
#  / - in case client is browser, it should render web page (index.html) which will show JS based UI
# /register - POST - new user registration
@app.route(defpath + '/register', methods=['POST'])
# @crossdomain(origin='*',headers=['Accept'])
def register():
	# app.logger.info("inside register")
	# app.logger.info(request.json)
	if not request.json or not 'email' in request.json:
		nobj = Notification()
		nobj.setdata(True,"Wrong Email or password !!",None)
		return buildresponse(nobj,{'http_status':400})
	else:
		user = User()
		# app.logger.info("after user--form")
		# app.logger.debug(request.form)
		# app.logger.info("in register, calling save {},{},{}".format(request.form['email'],request.form['name'],request.form['pwd']) )
	#	app.logger(request.form["email"])
		nobj = user.login(db.connection,request.json['email'],request.json['pwd'])
		if nobj.result is None:
			nobj = user.save(db.connection,request.json['email'],request.json['name'],request.json['pwd'])
		
		if not nobj.haserrors and nobj.result is not None:
			nobj.result={}
			resobj = user.getfeedtree(db.connection,request.json['email'])
			if not resobj.haserrors: 
				nobj.result["feedlist"] = resobj.result
				resobj = user.getcategorylist(db.connection,request.json['email'])
				if not resobj.haserrors:
					nobj.result["categories"] = resobj.result
					
		# app.logger.info("returning response")
		return buildresponse(nobj,{'http_status':201})
	
# /login - POST 
# /logout - GET 

# /category - Get - get list of categories for logged in user
@app.route(defpath + '/category', methods=['GET'])
@requires_auth
def getcatlist(**kwargs):
	user = User()
	nobj = user.getcategorylist(db.connection,kwargs['email'])
	return buildresponse(nobj,{'http_status':200})


# /category - POST - add new category
# todo: for POST, return 201 status code and  location header http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api?hn#ssl
@app.route(defpath + '/category', methods=['POST'])
@requires_auth
def addcategory(**kwargs):
	user = User()
	nobj = user.addcategory(db.connection,kwargs['email'],request.json['category'])
	return buildresponse(nobj,{'http_status':201})


#todo: add GET endpoint for category to return subscription details under a category

# /category - PUT - change  category
@app.route(defpath + '/category', methods=['PUT'])
@requires_auth
def changecategory(**kwargs):
	user = User()
	nobj = user.changecategory(db.connection,kwargs['email'],request.json['url'],request.json['category'])
	if not nobj.haserrors:
		nobj = user.getfeedtree(db.connection,kwargs['email'])
	return buildresponse(nobj,{'http_status':200})
	
# /category - DELETE - remove category
@app.route(defpath + '/category', methods=['DELETE'])
@requires_auth
def removecategory(**kwargs):
	user = User()
	nobj = user.removecategory(db.connection,kwargs['email'],request.form['category'])
	return buildresponse(nobj,{'http_status':200})
	
# /feed - GET - get feed details
@app.route(defpath + '/feed', methods=['GET'])
@requires_auth
def feeddetails(**kwargs):
	# app.logger.info(kwargs['email'])
	# app.logger.info(request.args.get('feedurl'))	
	user = User()
	nobj = user.getfeeddata(db.connection,kwargs['email'],request.args.get('feedurl'))
	return buildresponse(nobj,{'http_status':200})

	
# /feed - PUT - change category for subscription
@app.route(defpath + '/feed', methods=['PUT'])
@requires_auth
def changefeedcategory(**kwargs):
	user = User()
	nobj = user.changefeedcategory(db.connection,kwargs['email'],request.form['feedurl'],request.form['category'])
	return buildresponse(nobj,{'http_status':200})
		
# /feed - POST - add new  subscription 
@app.route(defpath + '/feed', methods=['POST'])
@requires_auth
def addfeed(**kwargs):
	# app.logger.info(kwargs['email'])
	# app.logger.info(request.json['feedurl'])	
	# app.logger.info(request.json['category'])		
	# app.logger.info(app.config['HTTP_PROXY'])
	user = User()
	nobj = user.addfeed(db.connection,kwargs['email'],request.json['feedurl'],request.json['category'],
	{'http_proxy':app.config['HTTP_PROXY']})
	if not nobj.haserrors and nobj.result is not None:
		nobj.result={}
		resobj = user.getfeedtree(db.connection,kwargs['email'])
		if not resobj.haserrors: 
			nobj.result["feedlist"] = resobj.result
			resobj = user.getcategorylist(db.connection,kwargs['email'])
			if not resobj.haserrors:
				nobj.result["categories"] = resobj.result
	
	return buildresponse(nobj,{'http_status':201})
	
# /feed - DELETE - remove subscription
@app.route(defpath + '/feed', methods=['DELETE'])
@requires_auth
def removefeed(**kwargs):
	user = User()
	nobj = user.removefeed(db.connection,kwargs['email'],request.args.get('feedurl'))
	return buildresponse(nobj,{'http_status':204})

@app.route(defpath + '/feeditem',methods=['PUT'])
@requires_auth
def updateitem(**kwargs):
	if not request.json or not 'id' in request.json:
		nobj = Notification()
		nobj.setdata(True,"ID Not found!!",None)
		return buildresponse(nobj,{'http_status':400})
	else:
		user = User()
		nobj = user.updatefeeditem(db.connection,kwargs['email'],request.json['id'],request.json['isread'],request.json['isstarred'])
		return buildresponse(nobj,{'http_status':200})
	
# /feeds - GET - Send subscription list
@app.route(defpath + '/feedlist', methods=['GET'])
# @crossdomain(origin='*',automatic_options=False,headers=['Accept','Authorization'])
@requires_auth
def feedlist(**kwargs):
	# app.logger.info(kwargs['email'])
	user = User()
	nobj = user.getfeedtree(db.connection,kwargs['email'])
	# app.logger.info(nobj)	
	return buildresponse(nobj,{'http_status':200})

@app.route(defpath + '/feeds', methods=['GET'])
# @crossdomain(origin='*',automatic_options=False,headers=['Accept','Authorization'])
@requires_auth
def allfeeds(**kwargs):
	# app.logger.info(kwargs['email'])
	user = User()
	nobj = user.getfeeddata(db.connection,kwargs['email'],None)
	# app.logger.info(nobj)	
	return buildresponse(nobj,{'http_status':200})

@app.route(defpath + '/feed/refresh', methods=['GET'])
# @crossdomain(origin='*',automatic_options=False,headers=['Accept','Authorization'])
@requires_auth
def refreshfeed(**kwargs):
	# app.logger.info(kwargs['email'])
	feed = Feed()
	nobj = feed.updatefeed(db.connection,request.args.get('feedurl'),
	{'http_proxy':app.config['HTTP_PROXY']})
	
	if not nobj.haserrors:
		user = User()
		nobj = user.getfeeddata(db.connection,kwargs['email'],request.args.get('feedurl'))
		# app.logger.info(nobj)	
		
	return buildresponse(nobj,{'http_status':200})	
	
@app.route(defpath + '/')
def index():
    return "root route"
    
# @app.route('/create', methods=['POST'])
# def create():
    # """Create user"""
    # user = request.form['name']
    # email = request.form['email']
    
    # try:
        # db.session.add(User(user, email))
        # db.session.commit()
        # d={'name': user, 'email': email}
    # except:
        # d={'error':'user exists'}
    
    # return jsonify(d)
    
# @app.route('/hello/<name>')
# def hello(name):
    # """Greet user"""
    # try:
        # user = User.query.filter_by(username=name).first()
        # d = {
            # 'id': user.id,
            # 'user': user.username,
            # 'email': user.email
        # }
    # except:
        # d={'error': 'user does not exist'}
    
    # return jsonify(d)
    
# @app.route('/delete/<name>', methods=['DELETE', 'POST'])
# def delete(name):
    
    # if request.method == 'POST':
        # resp = {'status': 'Using POST'}
    # else:
        # resp = {'status': 'Using DELETE'}
    
    # searchword = request.args.get('key', '')
    
    # """Delete user"""
    # #~db.session.delete(User).filter_by(username=name)
    # #~db.session.commit()
    # return jsonify(resp)
    
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
    
    # if request.method == 'POST':
        # f = request.files['file']
        # f.save('/tmp/newfile')
    
    # return jsonify({'status':'uploaded'})
    
# @app.route('/redirect', methods=['GET'])
# def redirect_to():
    # redirect(url_for('index'))

# 400 Bad Request
    # The request cannot be fulfilled due to bad syntax.[2]
# 401 Unauthorized
    # Similar to 403 Forbidden, but specifically for use when authentication is required and has failed or has not yet been provided.[2] The response must include a WWW-Authenticate header field containing a challenge applicable to the requested resource. See Basic access authentication and Digest access authentication.
# 402 Payment Required
    # Reserved for future use.[2] The original intention was that this code might be used as part of some form of digital cash or micropayment scheme, but that has not happened, and this code is not usually used. As an example of its use, however, Apple's defunct MobileMe service generated a 402 error if the MobileMe account was delinquent.[citation needed] In addition, YouTube uses this status if a particular IP address has made excessive requests, and requires the person to enter a CAPTCHA.
# 403 Forbidden
    # The request was a valid request, but the server is refusing to respond to it.[2] Unlike a 401 Unauthorized response, authenticating will make no difference.[2] On servers where authentication is required, this commonly means that the provided credentials were successfully authenticated but that the credentials still do not grant the client permission to access the resource (e.g. a recognized user attempting to access restricted content).
# 404 Not Found
    # The requested resource could not be found but may be available again in the future.[2] Subsequent requests by the client are permissible.
# 405 Method Not Allowed
    # A request was made of a resource using a request method not supported by that resource;[2] for example, using GET on a form which requires data to be presented via POST, or using PUT on a read-only resource.
# 406 Not Acceptable
    # The requested resource is only capable of generating content not acceptable according to the Accept headers sent in the request.[2]
# 407 Proxy Authentication Required
    # The client must first authenticate itself with the proxy.[2]
# 408 Request Timeout
    # The server timed out waiting for the request.[2] According to W3 HTTP specifications: "The client did not produce a request within the time that the server was prepared to wait. The client MAY repeat the request without modifications at any later time."
# 409 Conflict
    # Indicates that the request could not be processed because of conflict in the request, such as an edit conflict.[2]
# 410 Gone
    # Indicates that the resource requested is no longer available and will not be available again.[2] This should be used when a resource has been intentionally removed and the resource should be purged. Upon receiving a 410 status code, the client should not request the resource again in the future. Clients such as search engines should remove the resource from their indices. Most use cases do not require clients and search engines to purge the resource, and a "404 Not Found" may be used instead.
# 411 Length Required
    # The request did not specify the length of its content, which is required by the requested resource.[2]
# 412 Precondition Failed
    # The server does not meet one of the preconditions that the requester put on the request.[2]
# 413 Request Entity Too Large
    # The request is larger than the server is willing or able to process.[2]
# 414 Request-URI Too Long
    # The URI provided was too long for the server to process.[2]
# 415 Unsupported Media Type
    # The request entity has a media type which the server or resource does not support.[2] For example, the client uploads an image as image/svg+xml, but the server requires that images use a different format.
# 416 Requested Range Not Satisfiable
    # The client has asked for a portion of the file, but the server cannot supply that portion.[2] For example, if the client asked for a part of the file that lies beyond the end of the file.[2]
# 417 Expectation Failed
	

if __name__ == '__main__':
	# define app & config
	handler = logging.StreamHandler(sys.stdout)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	config = os.path.join(app.root_path, 'dev.cfg')
	app.config.from_pyfile(config)	
	app.run(host="0.0.0.0",port=3000,debug=True)