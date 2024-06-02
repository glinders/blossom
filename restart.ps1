# restart application
#
# WARNING -- deletes all data -- WARNING
#
#

echo ''
echo 'All Django data including database will be removed'
echo ''
$confirmation = Read-Host 'Do you want to continue'
if ($confirmation -ne 'y') {
    echo ''
    echo 'Aborting...'
    exit(0)
}

del db.sqlite3

del ccf\migrations\00*.*

del users\migrations\00*.*

python manage.py makemigrations

python manage.py migrate

# provide superuser name, email and password
$env:DJANGO_SUPERUSER_PASSWORD = 'admin'
python manage.py createsuperuser --username admin --email "admin@admin.com" --noinput




