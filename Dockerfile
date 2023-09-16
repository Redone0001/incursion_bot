FROM python:3
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD main.py eve_incursion_data.py incursion.py /
CMD ["python3", "./main.py"]