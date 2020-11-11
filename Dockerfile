# set base image (host OS)
FROM python:3.9

ARG db_account_user
ARG db_account_pass

ENV db_account_user ${db_account_user}
ENV db_account_pass ${db_account_pass}

# set the working directory in the container
WORKDIR /code

# install dependencies
RUN apt-get update && apt-get install -y libaio1 wget unzip

WORKDIR /opt/oracle
RUN wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip && \
    unzip instantclient-basiclite-linuxx64.zip && rm -f instantclient-basiclite-linuxx64.zip && \
    cd /opt/oracle/instantclient* && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci && \
    echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && ldconfig

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /code

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python", "./main.py" ]