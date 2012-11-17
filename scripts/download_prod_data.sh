echo "Performing dump"

ssh focus@'kontor.focussecurity.no' '
    ssh 'focus'@'10.0.6.31' "
        cd /var/webapps/focus24/focusbackup
        bin/django dumpdata -a > dumpdata.json
    "
'
echo "Downloading data"

ssh focus@kontor.focussecurity.no '
    scp focus@10.0.6.31:'/var/webapps/focus24/focusbackup/dumpdata.json .'
'

scp focus@kontor.focussecurity.no:~/dumpdata.json .

echo "Perform load"
bin/django flush --noinput
bin/django loadprod dumpdata.json

echo "Done!"