FROM python:3.12-alpine
ARG MODE=release
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV POETRY_HOME=/opt/poetry
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN cp /usr/share/zoneinfo/Europe/London /etc/localtime
RUN echo 'export LC_ALL=en_GB.UTF-8' >> /etc/profile.d/locale.sh && \
  sed -i 's|LANG=C.UTF-8|LANG=en_GB.UTF-8|' /etc/profile.d/locale.sh

COPY requirements/alpine /requirements/alpine

RUN apk update && grep -o "^[^#]*" /requirements/alpine/requirements.txt | xargs apk add

RUN locale
COPY pyproject.toml poetry.lock ./

RUN pip3 install --no-cache poetry
RUN poetry lock
RUN poetry install --no-root --only main
RUN pip3 install uwsgi

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY setup.py MANIFEST.in pytest.ini /workdir/

COPY uwsgi.ini /workdir/

COPY wallet_api/ /workdir/walle_api/

RUN pip3 install -e /workdir/ --break-system-packages
EXPOSE 8000
CMD "/entrypoint.sh"
