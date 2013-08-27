rssapp
======

Simple RSS reader using python, Mongodb and AngularJS

To Install:
===========

1. Clone the repository
2. It has following folders,
	a. api - contains server-side REST api in Python
	b. ui - UI for Reader
	
3. in 'api' folder, 
	a. create python virtual environement using virtualenv 
	b. install dependancies using "pip install -r requirements.txt"
	c. modify dev.cfg and set Proxy (if needed) and database connection settings 
	d. modify rssapp.py to set the http port if needed
	e. REST api is currently made available at "http://<ip>:<port>/api" 
	
4. in 'ui' folder,
	a. UI project uses yeoman 
	b. run "npm install & bower install" to install dependancies 
	c. modify gruntfile.js to change http port, if needed. (under "connect -> options")
	
	
5. nginx setup (Optional) 
	a. setup nginx reverse proxy to forward requests to UI and api. for e.g.
		server { # simple reverse-proxy for rssreader
			listen  9000;
			server_name  localhost;
			location / {
				proxy_pass      http://localhost:4000;
					}
			location /api {
				 proxy_pass      http://localhost:3000;
				 include        /etc/nginx/proxy.conf;
					}
			  }
6. To run the application (from 'api' folder), "honcho start"