#!/bin/bash
set -e
LOGFILE=/opt/web/focus24.no/focusbackup/guni.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=8
USER=focus
GROUP=focus
ADDRESS=127.0.0.1:8005
cd /opt/web/focus24.no/focusbackup
source /opt/web/focus24.no/focusbackup/venv/bin/activate
test -d $LOGDIR || mkdir -p $LOGDI
#export NEW_RELIC_CONFIG_FILE=newrelic.ini
exec gunicorn focusbackup.wsgi:application -w $NUM_WORKERS --bind=$ADDRESS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE 2>>$LOGFILE