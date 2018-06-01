#!/usr/bin/env bash

set -o errexit  # 只要有命令失败，就退出sh。 bash 默认错误，执行下一句命令。
set -o pipefail  # 当管道子命令有一条失败，整个管道命令失败。bash 默认只要最后一个子命令成功，即成功。
set -o nounset  # 遇到未定义的环境变量，抛出错误。bash 默认忽略。


python manage.py collectstatic --noinput --settings=config.settings.production
# python manage.py rebuild_index --settings=config.settings.production -y
python manage.py makemigrations --settings=config.settings.production
python manage.py migrate --settings=config.settings.production
python manage.py importpost --settings=config.settings.production


/usr/local/bin/gunicorn -c compose/production/gunicorn.conf config.wsgi
