from logs import logging
import os

logging.info('Setting up infrastructure')

os.system('apt update && apt install -y wget vim htop curl nano cron')
os.system('echo "deb http://cz.archive.ubuntu.com/ubuntu jammy main" >> /etc/apt/sources.list')
os.system('apt update')
os.system('apt install libc6')
os.system('apt install -y g++-11')


logging.info('Infrastructure ready')