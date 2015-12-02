import requests
import requests_cache

requests_cache.install_cache('worldbank_api_cache') #TODO how long does this last
base_uri = 'http://api.worldbank.org/'

def generic_query(uri, params={}):
    '''
    handles paging and json
    although world bank is really cool no auth sweet
    
    would  be cool if this cached
    '''
    uri = base_uri + uri
    params['format'] = 'json'
    info = []
    page_number = 1
    while True:
        result = requests.get(uri, params=params)
        if result.status_code != 200:
            return None, 'non 200 response'
        request_data = result.json()
        page_info, data = request_data
        info = info + data
        page_number += 1
        params['page'] = page_number
        if page_info['page'] == page_info['pages']:
            break

    return info, None

def poverty_data():
    uri = 'countries/all/indicators/SI.POV.NOP2'
    data, error = generic_query(uri)
    return data, error

def query_country(country_code):
    data, error = poverty_data()
    for row in data:
        if row['country']['id'] == country_code:
            print(row)
    

def parse_poverty_data(raw_data):
    '''
    input------------------------
    array off these
     {'decimal': '0', 'value': None, 'indicator': {'id': 'SI.POV.NOP2', 'value': 'Number of poor at $3.10 a day (2011 PPP) (millions)'}, 'country': {'id': 'ZW', 'value': 'Zimbabwe'}, 'date': '1990'},

    output ---------------------
    dictionary of dictionaries with key being country id
    the sub dicts look like
    {'country_name':Zimbabwe, 'most_recent_date':1990, percent:10.1}

    if no data can be found percent will be None

    issues -----------------
    all kinds of problems can happen if this data format changes even symantically
    why both a value and a decimal field
    we need to scrub regions out or do something with them
    '''
    country_id_to_poverty_data = {}
    for row in raw_data:
        country_id = row['country']['id']
        if country_id not in country_id_to_poverty_data:
            country_id_to_poverty_data[country_id] = {'country_name': row['country']['value'],
                                                      'most_recent_date': None,
                                                      'percent': None}
        country_poverty_data = country_id_to_poverty_data[country_id]
        most_recent_data_date = country_poverty_data['most_recent_date']

        if row['value'] is None or row['date'] is None:
            continue

        if most_recent_data_date is None or int(row['date']) > int(most_recent_data_date):
            country_poverty_data['percent'] = row['value']
            country_poverty_data['most_recent_date'] = row['date']

    return country_id_to_poverty_data
        

def most_recent_poverty_data():
    data, error = poverty_data()
    if error is not None:
        return data, 'could not get data on poverty from world bank: ' + error
    
    data = parse_poverty_data(data)
    return data, None
        

if __name__ == '__main__':
    #print(most_recent_poverty_data())
    query_country('DZ')
