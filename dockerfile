FROM nikolaik/python-nodejs:latest

COPY ./data /code/data
COPY ./django_sensors /code/django_sensors
COPY ./vue-project /code/vue-project
COPY ./start.sh /code/start.sh

RUN python -m pip install django
RUN python -m pip install django-cors-headers

WORKDIR /code/vue-project
RUN chmod +x /code/vue-project/node_modules/.bin/vite
RUN npm install

WORKDIR /code
EXPOSE 8000
EXPOSE 5173

ENTRYPOINT ["bash", "/code/start.sh"]
