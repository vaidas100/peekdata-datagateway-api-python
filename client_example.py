from Peekdata.DataGatewayAPI import ApiServices
from Peekdata.DataGatewayAPI import RequestServices
from Peekdata.DataGatewayAPI.Model import *
import logging
import time

__author__ = 'Vaidotas Senkus'
__email__ = 'vaidas100@gmail.com'


# logging configuration
PRINT = 25
logging.basicConfig(
    level=PRINT,
    format=format('%(message)s'),
    handlers=[
        logging.FileHandler(filename='client_example.log', mode='w'),
        logging.StreamHandler(),
    ]
)

logging.log(PRINT, "Peekdata Data API Gateway examples:\n")

# initialize client
api = ApiServices.ApiClient("demo.peekdata.io", 8080, "http")

# check service
t1 = time.time()
health = api.healthCheck()
t2 = time.time()
if health:
    logging.log(PRINT, "Healthcheck ok ({time:.2f}ms).\n".format(
        time=(t2 - t1)*1000
    ))
else:
    input("Service is not available. Press <Enter> to continue...")
    exit(1)

# create request
request = RequestServices.getTwoDimensionsTwoMetricsFilterAndSorting()
logging.log(PRINT, "Request serialized to JSON:\n{sep}\n{json}\n{sep}\n".format(
    json=serialize_to_json(request),
    sep='-'*40,
))

# get select
t1 = time.time()
select = api.getSelect(request)
t2 = time.time()
logging.log(PRINT, "Got SELECT statement in ({time:.2f}ms):\n{sep}\n{select}\n{sep}\n".format(
    time=(t2 - t1)*1000,
    select=select,
    sep='-'*40,
))

# get data
t1 = time.time()
data = api.getData(request)
t2 = time.time()
logging.log(PRINT, "Got DATA ({time:.2f}ms):\n{sep}\n{data}\n{sep}\n".format(
    time=(t2 - t1) * 1000,
    data=data,
    sep='-' * 40,
))

# get file
t1 = time.time()
csv_filename = 'client_example_output.csv'
api.GetCSV(request, csv_filename)
t2 = time.time()
logging.log(PRINT, "DATA stored to file ({time:.2f}ms):\n{sep}\n{file}\n{sep}\n".format(
    time=(t2 - t1) * 1000,
    file=csv_filename,
    sep='-' * 40,
))

logging.log(PRINT, "END")


