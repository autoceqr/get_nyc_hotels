# Get NYC Hotels Data
Repo for extracting NYC hotel data from NYC Go


```
from nyc_hotel_data import get_nyc_go_hotels_data
from datetime import datetime

hotel_id_list = [ ...list of hotel ids... ] 

dt_string = datetime.now().strftime("%Y-%d-%m_%H-%M-%S")

get_nyc_go_hotels_data(
    hotel_id_list, 
    'data/nyc_go_hotels_{}.csv'.format(dt_string)
)
```
