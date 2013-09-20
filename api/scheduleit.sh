#!/bin/bash
if [ -z "$OPENSHIFT_REPO_DIR" ];  then	
	source ./env/bin/activate 
	python scheduleit.py 
	deactivate	
else
	source ${OPENSHIFT_REPO_DIR}/env/bin/activate
	python ${OPENSHIFT_REPO_DIR}/scheduleit.py cron
	deactivate
fi
