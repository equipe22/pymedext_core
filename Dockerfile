FROM python:3.7.2-slim
# HEGP NECKER
#special variables to define in order to process
#and generate the provenance of the script

MAINTAINER william.digan@aphp.fr
ENV containerName='pymedext-ehr'
ENV inputData=folder
ENV typeSearch="store data to OMOP"
ENV output="stdout"
ENV command="python3 /home/src/omop_prod_norm_graph.py -i $input"
ENV whenConditions=""
ENV metaParameters=""
ENV lowerText="True"
ENV treatFolder="True"
ENV sources="{'romedi':'','rxnorm':'-s'}"

WORKDIR /home
RUN mkdir data
RUN apt-get update
RUN apt-get -y install g++ gcc git build-essential
RUN pip3 install --upgrade pip

RUN apt-get update && apt-get install -y --allow-unauthenticated procps
RUN apt-get install -y libpq-dev libffi-dev python3-dev libxml2 libxml2-dev libxslt-dev python-dev
RUN apt-get install -y python3-lxml
RUN pip3 install lxml
RUN pip3 install git+https://github.com/equipe22/pymedext_core.git@v0.0.1
WORKDIR /home/data


CMD ["python3", "/home/src/omop_prod_norm_graph.py ","--inputFolder","$input"]
