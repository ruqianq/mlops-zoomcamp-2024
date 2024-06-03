import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):
    service = 'fhv'
    year = 2019
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'

    # native date parsing 
    for i in range(12):
        
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]

        file_name = f"{service}/{service}_tripdata_{year}-{month}.csv.gz"
        # download it using requests via a pandas df
        request_url = url + file_name
        print(request_url)
        r = requests.get(request_url)
        open(f'{file_name}', 'wb').write(r.content)
        print(f"Local: {file_name}")


    return 
