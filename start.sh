if [ -f "./dev" ]; then
  python manage.py runserver 0.0.0.0:8001
else
  uwsgi --chdir=. --module=currentmap.wsgi:application --env DJANGO_SETTINGS_MODULE=currentmap.settings --master --pidfile=./project-master.pid --http 0.0.0.0:8001 --processes=2 --uid=1000 --gid=2000 --harakiri=20 --max-requests=100 --vacuum                      # clear environment on exit
fi