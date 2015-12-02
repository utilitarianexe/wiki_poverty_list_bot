def parse_header(line):
    '''
    input-----------------
    Series Name,Series Code,Country,Country Code,2012 [YR2012],2013 [YR2013],2014 [YR2014]
    output -------------
    ['2012','2013','2014']
    '''
    header_info = line.split(',')
    years_included = []
    for item in reversed(header_info):
        if item == 'Country Code':
            break
        year = item[:4]
        years_included.append(year)
    return list(reversed(years_included)) #needs to be iterated more than once


def most_recent_data(countries_data):
    '''
    takes output of parse_table_data
    turns it into the form outputed by parse_poverty_data
    might just want to totally throw this out
    '''
    country_id_to_poverty_data = {}
    for country_data in countries_data:
        country_id = country_data['code']
        country_name = country_data['name']
        if country_id in country_id_to_poverty_data:
            print('why are we getting repeats')
            continue
        
        year, rate = most_recent_year_percent(country_data)
        country_poverty_data = {'country_name': country_name,
                                'most_recent_date':year,
                                'percent': rate}
        country_id_to_poverty_data[country_id] = country_poverty_data

    return country_id_to_poverty_data


def most_recent_year_percent(country_data):
    year_data = country_data['years_to_rates']
    max_year, max_rate = None, None
    for year, rate in year_data.items():
        if max_rate is None or (int(year) > int(max_year) and rate is not None):
            max_year = year
            max_rate = rate

    return max_year, max_rate


def parse_table_data(csv_file):
    '''
    input----------------
    essentially a file will change to pass in later
    gives the percentage of people below the specified income for a year

    so these are csvs
    generally pure comma seperated but if comma in cell then quoted

    there is one header column

    columns look like
    description,weird thing, full name, countriy code, percentage for year,[next year],[next year]

    output --------------
    array of dicts
    where each dict corresponds to a line like
    {'code': 'MNG', 'years_to_rates': {'2014': None, '2013': None, '2012': '0.1109293905'}, 'name': 'Mongolia'}

    todo--------------
    use pandas maybe
    might be totally scrapped if worldbank api
    '''
    poverty_data = []
    for i, line in enumerate(csv_file):
        line = line[:-2] #remove trailing \r\n
        if i == 0: # I hate this hack for headers
            years_included = parse_header(line)
            continue
        if line == ',,,,,,':
            break

        line_data = line.split(',')
        #remove unneeded data
        line_data = line_data[2:]
        country_data = {}
        country_data['name'] = line_data[0]
        country_data['code'] = line_data[1]
        country_data['years_to_rates'] = {}
        for rate, year in zip(line_data[2:], years_included):
            if rate == '..':
                rate = None
            country_data['years_to_rates'][year] = rate
            
        poverty_data.append(country_data)

    return poverty_data


def download_table_data():
    '''
    currently manually gotten from
    http://databank.worldbank.org/data/reports.aspx?source=poverty-and-equity-database#
    
    needs to use an api or if that fails wget
    we may even be able to avoid parsing with a good api
    '''

    csv_file = open('/home/peter/Downloads/Data_Extract_From_Poverty_and_Equity_Database_Data.csv')
    return csv_file


def most_recent_poverty_data():
    csv_file = download_table_data()
    table_data = parse_table_data(csv_file)
    most_recent_table_data = most_recent_data(table_data)
    return most_recent_table_data
