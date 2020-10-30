# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Open Education Polito.
#
# fare is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

FROM nginx
ARG NGINX_CERT
ARG NGINX_KEY
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/* /etc/nginx/conf.d/
COPY $NGINX_KEY /etc/ssl/private/nginx_key.key
COPY $NGINX_CERT /etc/ssl/certs/nginx_cert.crt
