echo "Performing dump"

ssh focus@'kontor.focussecurity.no' '
    cd /var/webapps/focus24/focusbackup
    bin/django dumpdata -a > ~/dumpdata.json
'
echo "Downloading data"

scp focus@kontor.focussecurity.no:~/dumpdata.json .

echo "Perform load"
source venv/bin/activate
python manage.py syncdb --migrate --noinput
python manage.py flush --noinput
python manage.py loadprod dumpdata.json

echo "Done!"