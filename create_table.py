'''
dev things----------
we need tests
we need python tools(autocomplete, sytax checker, pep8, debugger)
read all doc strings
code review
copy paste

problems at current feature set -------------
how do we decide what years to consider
how do we quotes around names
how do we fix

required features--------------
auto posting
auto pulling
other tables
updating the image
informing other editors
'''

def get_table_data():
    csv_file = download_table_data()
    table_data = parse_table_data(csv_file)
    return table_data

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
    not quite sure how the output should look
    v1 is going to be array or dicts
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


def most_recent_data(country_data):
    year_data = country_data['years_to_rates']
    max_year, max_rate = None, None
    for year, rate in year_data.items():
        if max_rate is None or (int(year) > int(max_year) and rate is not None):
            max_year = year
            max_rate = rate

    return max_year, max_rate


def build_wiki_table(table_data):
    '''
    ---input
    see outpute of parse_table_data
    ---output
    |-
    | style="text-align:left;"| {{flag|Albania}} || 0.5 || 3.00 || 2012 || 31.5 || 2012
    |-
    | style="text-align:left;"| {{flag|Algeria}} || 6.79 || 23.61 || 1995 || 63 || 1995
    |-
    --todo
    what happens if we are missing a 
    '''
    table_text = ''
    row_texts = []
    for country_data in table_data:
        row_break = '|-\n'
        name = country_data['name']
        year, rate = most_recent_data(country_data)
        if year is None or rate is None:
            rate = 'bla' #TODO
            year = 'bla' #TODO
            continue

        # simplified take a look at doc string for whats currently on page
        # not using standard  python string formating because of conflicts with markup
        row_text = '| style="text-align:left;"| {{flag|' + name + '}} ||' + rate + ' || ' + year + '\n'
        row_text = row_text + row_break
        row_texts.append(row_text)
    
    table_text = ''.join(row_texts)
    return table_text


def post_table(wiki_table):
    # api if possible otherwise got to hack it or maybe just print the full edit for now
    print('not implemented you need to paste the folowing yourself')
    print(wiki_table)
    pass


def build_table():
    table_data = get_table_data()
    wiki_table = build_wiki_table(table_data)
    post_table(wiki_table)


if __name__ == '__main__':
    build_table()
