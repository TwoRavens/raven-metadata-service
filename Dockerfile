FROM python:3.6.4
MAINTAINER TwoRavens http://2ra.vn/

LABEL organization="Two Ravens" \
      2ra.vn.version="0.0.1-alpha" \
      2ra.vn.release-date="2018-02-21" \
      description="Preprocessing for tabular data"

# -------------------------------------
# Install debugging tools
# -------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils\
    iputils-ping \
    telnet \
    vim

# -------------------------------------
# Set the workdir
# -------------------------------------
WORKDIR /var/apps/raven-metadata-service

# -------------------------------------
# Copy over the requirements and run them
# -------------------------------------
COPY ./requirements/ ./requirements
RUN pip3 install --no-cache-dir -r requirements/10_preprocess.txt

# -------------------------------------
# Copy over the rest of the repository
# -------------------------------------
COPY . .

# -------------------------------------
# Copy preprocess script
# -------------------------------------
COPY preprocess/scripts/preprocess_file.sh /usr/bin/preprocess_file.sh
RUN chmod u+x /usr/bin/preprocess_file.sh

# -------------------------------------
# Create a volume for sharing between containers
# -------------------------------------
VOLUME /ravens_volume


# -------------------------------------
# Run preprocess against the entry point input param
# -------------------------------------
ENTRYPOINT ["/usr/bin/preprocess_file.sh"]
#CMD []

#RUN cd preprocess  && \
#    python preprocess.py
