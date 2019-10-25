import requests
import pandas as pd
import time
from io import BytesIO


def get_nyc_go_hotel_json(hotel_id):
    return requests.get(
        "https://api.nycgo.com/api/v2/hotels?hotelId={}&limit=1".format(
            hotel_id,
        )
    ).json()


def extract_response_data(data):
    return {
        'hotel_id': data['data'][0]['hotelId'],
        'longitude': data['data'][0]['hotelData']['location']['longitude'],
        'latitude': data['data'][0]['hotelData']['location']['latitude'],
        'num_rooms': data['data'][0]['hotelData']['numberOfRooms'],
        'city': data['data'][0]['hotelData']['city'],
        'zip_code': data['data'][0]['hotelData']['zip'],
        'hotel_type_id': data['data'][0]['hotelData']['hotelTypeId'],
        'city_id': data['data'][0]['hotelData']['cityId'],
        'address': data['data'][0]['hotelData']['address'],
        'hotel_class': data['data'][0]['hotelData']['class'],
        'name': data['data'][0]['hotelData']['name'],
        'district_id': data['data'][0]['hotelData']['districtId'],
        'url': data['data'][0]['hotelData']['url']
    }


def get_nyc_go_hotels_data(
        hotel_id_list,
        output_csv,
):
    hotel_data = {}

    for hotel_id in hotel_id_list:
        hotel_data[hotel_id] = extract_response_data(
            get_nyc_go_hotel_json(hotel_id)
        )
        time.sleep(1)

    pd.DataFrame(hotel_data).T.to_csv(output_csv, index=False)


def google_sheet_to_dataframe(url):
    r = requests.get(url)
    data = r.content
    return pd.read_csv(BytesIO(data))


def get_osm_data(
        query,
        radius_meters,
        latitude,
        longitude,
        output_csv,
):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    ({}(around:{},{},{});
    );
    out center;
    """.format(query, radius_meters, latitude, longitude)

    response = requests.get(
        overpass_url,
        params={'data': overpass_query}
    )

    data = response.json()

    df = pd.DataFrame(data['elements'])

    pd.concat(
        [
            df.drop(['tags'], axis=1),
            df['tags'].apply(pd.Series)
        ],
        axis=1,
    ).to_csv(output_csv, index=False)
