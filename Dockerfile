FROM python:3.6.3
ADD . /project
RUN pip install --upgrade pip
RUN pip install -r /project/requirements.txt
RUN chmod a+x /project/run.sh
WORKDIR /project
CMD ["sh","/project/run.sh"]