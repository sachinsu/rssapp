#!/bin/bash
if [ -z "$OPENSHIFT_REPO_DIR" ];  then	
	source ./env/bin/activate 
	python  archiver.py 
	deactivate	
else
	source ${OPENSHIFT_REPO_DIR}/env/bin/activate
	python ${OPENSHIFT_REPO_DIR}/archiver.py cron
	deactivate
fi
