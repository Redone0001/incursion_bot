FROM python:3
ADD main.py eve_incursion_data.py incursion.py requirements.txt /
RUN pip install -r requirements.txt
CMD ["python3", "./main.py"]