FROM python:3.7-alpine
LABEL Author=guowei.he@appcoachs.com

VOLUME ["/www"]

RUN apk add --no-cache libpng freetype libstdc++ python py-pip
RUN apk add --no-cache --virtual .build-deps \
	    gcc \
	    build-base \
	    python-dev \
	    libpng-dev \
	    musl-dev \
	    freetype-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h \
	&& pip install numpy \
	&& pip install matplotlib \
    && pip install Flask \
	&& pip install python-dotenv \
	&& pip install flask-sqlalchemy \
	&& pip install pymysql \
    && pip install flask_mail \
	&& apk del .build-deps

WORKDIR /www

EXPOSE 5000

ENV FLASK_APP=hello.py
ENV FLASK_ENV=development

CMD ["flask", "run","--host=0.0.0.0"]