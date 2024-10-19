#!/bin/bash

# Gives a personalised greeting
# Adds configuration options for SQLite
# Creates run aliases
# Author: Bill Saunders

echo "Setting the greeting"
sed -i "s/USER_NAME/$GITPOD_GIT_USER_NAME/g" ${GITPOD_REPO_ROOT}/README.md
echo "Creating .sqliterc file"
echo ".headers on" > ~/.sqliterc
echo ".mode column" >> ~/.sqliterc
echo "Your workspace is ready to use. Happy coding!"

# Install PostgreSQL 13
echo "Installing PostgreSQL 13"
sudo apt-get update
sudo apt-get install -y postgresql-13

# Start PostgreSQL service
echo "Starting PostgreSQL service"
sudo service postgresql start

# Run Django migrations
echo "Running Django migrations"
python3 manage.py migrate
