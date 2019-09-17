# scrapy_nhs docker file

# build: docker build -t scrapy_nhs .
FROM bionic-mongo-python

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY nhs/nhs /app/nhs/nhs
COPY nhs/scrapy.cfg /app/nhs
COPY docker_start_scrapy_nhs.sh /app
COPY nhs/requirements.txt /app

# RUN echo $(ls -1R .)
# RUN apt-get install -y vim

RUN mkdir -p /app/nhs_files
ENV FILES_STORE="/app/nhs_files"
ENV MONGO_URI='mongodb://mongo_db:27017/'

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["/app/docker_start_scrapy_nhs.sh"]
CMD ["mongo_db"]
