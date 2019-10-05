# scrapy_nhs docker file

# build: docker build -t scrapy_nhs .
FROM bionic-mongo-python

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY nhs/nhs /app/nhs/nhs
COPY nhs/scrapy.cfg /app/nhs
COPY docker_start_scrapy_nhs.sh /app
COPY docker_send_test_files.sh /app
COPY nhs/requirements.txt /app
RUN mkdir -p  /app/nhs/tests
COPY nhs/tests/test_kafka_pipeline.py /app/nhs/tests
COPY nhs/tests/utiltest.py /app/nhs/tests
COPY nhs/tests/__init__.py /app/nhs/tests
RUN mkdir -p /app/nhs_test_files/full
COPY nhs/tests/resources/xls/9781fb726a6213cc8e52c5d5c2b6aa9ad77a11f0.xlsx /app/nhs_test_files/full
RUN echo $(ls -1R .)
# RUN apt-get install -y vim

RUN mkdir -p /app/nhs_files
ENV KAFKA_HOST='kafka'
ENV FILES_STORE="/app/nhs_files"
# obsolete: now using kafka
ENV MONGO_URI='mongodb://mongo_db:27017/'

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["/app/docker_start_scrapy_nhs.sh"]
CMD ["mongo_db"]
