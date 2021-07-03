FROM trafex/php-nginx:latest

# Install composer from the official image
COPY --from=composer /usr/bin/composer /usr/bin/composer

# Run composer install to install the dependencies
RUN composer require "twig/twig:^3.0"

USER root

RUN set -ex \
  && apk --no-cache add \
    postgresql-dev

RUN apk add php8-pgsql php8-pdo_pgsql

USER nobody