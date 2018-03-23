# :ticket: My Little Ticket

[![Build Status](https://travis-ci.org/iksaif/my-little-ticket.svg?branch=master)](https://travis-ci.org/iksaif/my-little-ticket)
[![Coverage Status](https://coveralls.io/repos/github/iksaif/my-little-ticket/badge.svg)](https://coveralls.io/github/iksaif/my-little-ticket?branch=master)
[![Dependency Status](https://gemnasium.com/badges/github.com/iksaif/my-little-ticket.svg)](https://gemnasium.com/github.com/iksaif/my-little-ticket)

UI and API to show an aggregate status of your services.

[![My-Little-Ticket screenshot](doc/my-little-ticket.png)](doc/my-little-ticket.png)

*This is currently under active development and not ready for production.*


## Quickstart

```bash
virtualenv venv -p python3
source venv/bin/activate
cp examples/local_settings.py defcon/
pip install -e .
pip install -r requirements.txt
./manage.py migrate
./manage.py migrate --run-syncdb
./manage.py createsuperuser
./manage.py runserver
```

## Configuration

.. Work in progress ..

## Authentication

.. Work in progress ..

## API

.. Work in progress ..
