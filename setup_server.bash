#! ../bin/bash

mv ./server/notedrop_nginx.conf /etc/nginx/sites-enabled
mv ./server/start_notedrop ../bin
mv ./server/notedrop_supervisor.conf /etc/supervisor/conf.d
