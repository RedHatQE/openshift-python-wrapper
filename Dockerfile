FROM python

COPY . /openshift-pythpn-wrapper
WORKDIR /openshift-pythpn-wrapper
RUN pip install pip -U && pip install tox
CMD ["tox", "-e", "tests"]
