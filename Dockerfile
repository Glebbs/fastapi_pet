#
FROM python:3.10

#
WORKDIR /src
#

#
COPY ./requirements.txt /.

#
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

#
COPY ./src/ /src/

#
CMD ['alembic', 'upgrade', 'head', '&', "python" ,"-m" ,"app.main"]

EXPOSE 80