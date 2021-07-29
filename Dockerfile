FROM python:3.9

RUN pip install \
	boto3 \
	numpy \
	pandas \
	pyyaml \
	synapseclient \
	XlsxWriter

RUN git clone https://github.com/Sage-Bionetworks/sysbioDCCjsonschemas.git

WORKDIR sysbioDCCjsonschemas

CMD ["/bin/bash"]
