FROM python:3
COPY pip.install.txt .
RUN pip install -r pip.install.txt
WORKDIR workdir
COPY src ./src
COPY README.sh index.sh Makefile *.mk ./
