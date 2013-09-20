#!/bin/bash
if [ -z "$OPENSHIFT_REPO_DIR" ];  then	
	source /home/ubuntu/projects/app/api/env/bin/activate && python /home/ubuntu/projects/app/api/archiver.py cron > /dev/null
else
	source ${OPENSHIFT_REPO_DIR}/env/bin/activate &&  python ${OPENSHIFT_REPO_DIR}/archiver.py cron
fi
