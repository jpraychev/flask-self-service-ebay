# How to start app in daemon mode using gunicorn

1. Start the service
```
/home/jraychev/ebay-bg/venv/bin/python3 /home/jraychev/ebay-bg/venv/bin/gunicorn --chdir /home/jraychev/ebay-bg/flask-self-service-ebay/src/ -b 192.46.239.37:5000 app:app --daemon --log-file logs/debug.log --log-level DEBUG --access-logfile logs/access.log
```