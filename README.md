rssapp
======

Simple RSS reader using python, Mongodb and AngularJS

To Install:
===========

1. Clone the repository
2. It has following folders,
	> api - contains server-side REST api in Python
	> ui - UI for Reader
	
3. in 'api' folder, 
	> create python virtual environement using virtualenv 
	> install dependancies using `pip install -r requirements.txt`
	> modify dev.cfg and set Proxy (if needed) and database connection settings 
	> modify rssapp.py to set the http port if needed
	> REST api is currently made available at "http://<ip>:<port>/api" 
	
4. in 'ui' folder,
	> UI project uses yeoman 
	> run `npm install & bower install` to install dependancies 
	> modify gruntfile.js to change http port, if needed. (under "connect -> options")
	
	
5. To run the application, 
         * In development mode, ui server can be run using grunt (from 'ui' folder) and parallely running REST api. To avoid issues with cross domain requests, 
	   following is sample reverse proxy settings to forward requests from UI to api using nginx. 
		```
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
		```
           To run the application (from 'api' folder), `honcho start`		       
         * Alternatively, ui folder can be linked `sudo ln -s ..` within api folder and application can be run as python app itself by issuing ```python rssapp.py``` from 'api' folder. 
           Batch jobs to update , archive feeds can be configured as cron jobs. 
           Sample cron job entries are (in 'api' folder),
           `*/15 * * * * <path to project>/api/scheduleit.sh`         
           `0 */12 * * * <path to project>/api/archiver.sh`

Check sample screenshots at https://github.com/sachinsu/rssapp/wiki/Screenshots
