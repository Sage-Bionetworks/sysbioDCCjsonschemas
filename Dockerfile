FROM python:3.9

RUN pip install \
	boto3 \
	numpy \
	pandas \
	pyyaml \
	synapseclient \
	XlsxWriter

RUN mkdir sysbioDCCjsonschemas
COPY . sysbioDCCjsonschemas

WORKDIR sysbioDCCjsonschemas

CMD ["/bin/bash"]
