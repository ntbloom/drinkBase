### dependencies.md -- notes for how to build drinkbase on debian

# packages to install with apt-get
vim
tmux
git
python3-pip
python3-venv
postgresql
postgresql-client
postgresql-doc
postgresql-server-dev-all
curl
apache2
libapache2-mod-wsgi-py3
nginx
certbot
python-certbot-apache
python-certbot-nginx
## additional dev dependencies
locate
man-db


# things to do
- make ssh keys
- configure ssh/ssh_config
- copy ssh to github
- git clone configs and use bashrc/etc

# configure postgres
- login as postgres
- mkdir /usr/local/postgres, give ownership to postgres
- make symlink of pg_hba.conf to postgres directory
- initdb (located /usr/lib/postgresql...)
- start database server
- update pg_hba.conf to set authentication method to "trust"
- create role
  CREATE ROLE debian LOGIN CREATEDB;
  ALTER ROLE debian SET client_min_messages = WARNING;

# configure apache
- put drinkbase.conf in sites-available
```
sudo a2enmod headers
sudo a2dissite 000-default.conf
sudo a2ensite drinkbase.conf
sudo systemctl start apache2
```

# install nodejs
```
sudo su -
curl -sL https://deb.nodesource.com/setup_10.x | bash -
apt-get install -y nodejs
```

# nginx
sudo ln -sf ~/drinkbase/build /var/www
sudo ln -sf ~/drinkbase/deployment/nginx/default /etc/nginx/sites-available
sudo systemctl start nginx
