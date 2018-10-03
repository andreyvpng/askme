# Ask me

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/47fcd26304534930a2940ab39524d82c)](https://app.codacy.com/app/andreyvpng/askme?utm_source=github.com&utm_medium=referral&utm_content=andreyvpng/askme&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.org/andreyvpng/askme.svg?branch=master)](https://travis-ci.org/andreyvpng/askme)

The web application for people who likes to ask questions and get answers from others.

![Screenshot](screenshot.png)

Add .env. For developping I'm using this:

    DJANGO_DB_NAME=askme
    DJANGO_DB_USER=askme
    DJANGO_DB_PASSWORD=askme
    DJANGO_DB_HOST=db
    DJANGO_DB_PORT=5432
    DJANGO_SETTINGS_MODULE=config.dev_settings

For build and run, use:

    docker-compose build && docker-compose up
