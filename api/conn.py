import pymongo

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

class dbcon(object):
    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        # app.config.setdefault('DATABASE_URI', 'mongodb://localhost:27017/')
        # app.config.setdefault('DBNAME', 'feedtest')		
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
		uri = self.app.config['DATABASE_URI']
		print "******"
		print uri
		return pymongo.MongoClient(uri)
#		sqlite3.connect(self.app.config['SQLITE3_DATABASE'])

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'mongo_db'):
            ctx.mongo_db.close()

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'mongo_db'):
                ctx.mongo_db = self.connect()
            return ctx.mongo_db[self.app.config['DBNAME']]