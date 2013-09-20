#!/bin/bash
if [ -z "$OPENSHIFT_REPO_DIR" ];  then	
	source /home/ubuntu/projects/app/env/bin/activate 
	python /home/ubuntu/projects/app/scheduleit.py 
	deactivate	
else
	source ${OPENSHIFT_REPO_DIR}/env/bin/activate
	python ${OPENSHIFT_REPO_DIR}/scheduleit.py cron
	deactivate
fi
