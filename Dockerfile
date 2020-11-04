FROM python:3
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD Dashboard.py /
ADD cdph-race-ethnicity.csv /
ADD latimes-state-totals.csv /
CMD ["bokeh", "serve" ,"--show", "Dashboard.py" ]