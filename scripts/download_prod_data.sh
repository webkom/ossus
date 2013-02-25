echo "Performing dump"

ssh focus@'kontor.focussecurity.no' '
    cd /var/webapps/focus24/focusbackup
    bin/django dumpdata -a > ~/dumpdata.json
'
echo "Downloading data"

scp focus@kontor.focussecurity.no:~/dumpdata.json .

echo "Perform load"
bin/django flush --noinput
bin/django loadprod dumpdata.json

echo "Done!"