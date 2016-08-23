
apt-get update
apt-get -y install build-essential
apt-get -y install python-pip python-dev python-setuptools python-psycopg2
apt-get -y install nginx
apt-get -y install libtiff5-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

pip install --upgrade supervisor
pip install --upgrade virtualenv
