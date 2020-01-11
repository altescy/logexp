# This Dockerfile creates an environment suitable for downstream usage of logexp.
# It creates an environment that includes a pip installation of logexp.

FROM python:3.7

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /logexp

COPY setup.py setup.py
COPY logexp/ logexp/
COPY Makefile Makefile

RUN python setup.py install
RUN make clean

ENTRYPOINT ["logexp"]
