FROM python:3-alpine

COPY dist/output-producer-resource-*.tar.gz .
RUN pip install output-producer-resource-*.tar.gz
RUN mkdir -p /opt/resource
RUN for script in check in out; do ln -s $(which $script) /opt/resource/; done
