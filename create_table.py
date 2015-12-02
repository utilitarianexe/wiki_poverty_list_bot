'''
update to use https://pypi.python.org/pypi/wbpy/2.0.1
dev things----------
need requirments file
we need tests
need to handle all error conditions
we need python tools(autocomplete, sytax checker, pep8, debugger)
read all doc strings
code review
copy paste
redundant code
bad naming

problems at current feature set -------------
how do we decide what years to consider
how do we quotes around names
how do we fix

required features--------------
get numbers for all income levels
why so few countries in data sets
remove non country entities or find some way to deal with them
deal with quotes

auto posting
auto pulling
other tables
updating the image
informing other editors
'''

import world_bank_csv
import world_bank_api
import iso3166 # country code data

def build_wiki_table(table_data):
    '''
    ---input
    see outpute of parse_poverty_data
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
    for country_id, country_data in table_data.items():
        row_break = '|-\n'
        name = country_data['country_name']
        year = country_data['most_recent_date']
        rate = country_data['percent']
        print(country_id, name)
        if year is None or rate is None:
            print('missing data for: ' + name)
            continue

        # TODO simplified take a look at doc string for whats currently on page
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


def build_table():
    #poverty_data = world_bank_csv.most_recent_poverty_data()
    poverty_data, error = world_bank_api.most_recent_poverty_data()
    if error is not None:
        print(error)
        return
    wiki_table = build_wiki_table(poverty_data)
    post_table(wiki_table)


if __name__ == '__main__':
    build_table()
