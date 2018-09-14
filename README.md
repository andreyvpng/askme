# Ask me

A ask.fm clone development with django 2

Add .env. For developping I'm using this:

    DJANGO_DB_NAME=askme
    DJANGO_DB_USER=askme
    DJANGO_DB_PASSWORD=askme
    DJANGO_DB_HOST=db
    DJANGO_DB_PORT=5432
    DJANGO_SETTINGS_MODULE=config.dev_settings

For build and run, use:

    docker-compose build && docker-compose up
