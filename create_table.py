'''
dev things----------
update to use https://pypi.python.org/pypi/wbpy/2.0.1
we need tests
need to handle all error conditions
make sure all pylint is good
read all doc strings
code review
copy paste
redundant code
bad naming

manaul update work --------------
remove bangladesh citation
remove gambia citation
change description of chart
look at notes about wiki bots

like to have------------------
auto posting
updating the image
cia data
compain to world bank about incomplete data
auto fill in dates for access times
auto pulling
other tables
informing other editors
'''

import world_bank_api
import iso3166 # country code data
import datetime


def build_table_text(table_data):
    #December 4, 2015
    now = datetime.date.today()
    
    header = '''{{| class="wikitable sortable" style="margin-left:auto;margin-right:auto;text-align: right"
|-
! data-sort-type = text | Country
! data-sort-type = number | $1.90<ref name="wdipov">{{{{cite web | url =http://data.worldbank.org/indicator/SI.POV.2DAY | title =World Development Indicators | publisher =[[World Bank]] | date = {date1}  | accessdate = {date2} }}}}</ref>
! data-sort-type = number | Year
! data-sort-type = number | < $3.10<ref name="wdipov">{{{{cite web | url =http://data.worldbank.org/indicator/SI.POV.2DAY | title =World Development Indicators | publisher =[[World Bank]] | date = {date3} | accessdate = {date4} }}}}</ref>
! data-sort-type = number | Year
|-'''
    date_text = now.isoformat()
    header = header.format(date1=date_text, date2=date_text, date3=date_text, date4=date_text)
    footer = '|}'
    rows = build_table_rows(table_data)
    rows = rows[:-4] # remove final row seperator
    table_text = '{header}\n{rows}\n{footer}'.format(header=header, rows=rows, footer=footer)
    return table_text


def reference_overwrite(name, rate_190, year_190, rate_310, year_310):
    india_ref = '<ref>http://pubdocs.worldbank.org/pubdocs/publicdoc/2015/10/109701443800596288/PRN03-Oct2015-TwinGoals.pdf</ref>'
    overwrite_dict = {'India': {'level_190': {'year': '2012', 'rate':'12.4', 'ref': india_ref},
                                'level_310': None}}
    ref_190 = None
    ref_310 = None
    if name not in overwrite_dict:
        return rate_190, year_190, ref_190, rate_310, year_310, ref_310

    overwrite = overwrite_dict[name]
    if overwrite['level_190'] is not None:
        if int(overwrite['level_190']['year']) > int(year_190):
            year_190 = overwrite['level_190']['year']
            rate_190 = overwrite['level_190']['rate']
            ref_190 = overwrite['level_190']['ref']

    if overwrite['level_310'] is not None:
        if int(overwrite['level_310']['year']) > int(year_310):
            year_310 = overwrite['level_310']['year']
            rate_310 = overwrite['level_310']['rate']
            ref_310 = overwrite['level_310']['ref']

            
    return rate_190, year_190, ref_190, rate_310, year_310, ref_310


def remap_country(name):
    '''
    Many countries returned by the world bank api do match the wikipedia flag template names
    this funcion manually remaps them
    '''
    flag_name_by_world_bank_name = {
        'Virgin Islands (U.S.)': 'United States Virgin Islands',
        'Egypt, Arab Rep.': 'Egypt',
        'Hong Kong SAR, China': 'Hong Kong',
        'Korea, Dem. Rep.': 'North Korea',
        'Lao PDR': 'Laos',
        'Macao SAR, China': 'Macao',
        'St. Martin (French part)': 'Collectivity of Saint Martin',
        'Venezuela, RB': 'Venezuela',
        'Yemen, Rep.': 'Yemen',}
    return flag_name_by_world_bank_name.get(name, name)


def build_table_rows(table_data):
    '''
    ---input
    see output of world_bank_api.most_recent_poverty_data
    ---output
    |-
    | style="text-align:left;"| {{flag|Albania}} || 0.5 || 3.00 || 2012 || 31.5 || 2012
    |-
    | style="text-align:left;"| {{flag|Algeria}} || 6.79 || 23.61 || 1995 || 63 || 1995
    |-
    flag problemsdd
    Virgin Islands (U.S.) -> United States Virgin Islands
    Egypt, Arab Rep. -> Egypt
    Hong Kong SAR, China -> Hong Kong
     Korea, Dem. Rep. -> North Korea
    Lao PDR -> Laos
    Macao SAR, China -> Macao
    St. Martin (French part) -> Collectivity of Saint Martin
    Venezuela, RB -> Venezuela
    Yemen, Rep. -> Yemen
    '''
    row_texts = []
    number_valid = 0
    countries_with_bad_data_190 = set()
    countries_with_bad_data_310 = set()
    countries_good = set()
    for country_data in table_data:
        country_id = country_data['country_code']
        name = country_data['country_name']
        name = remap_country(name)
        try:
            iso3166.countries.get(country_id)
        except KeyError:
            message = 'non country code {} name {} skipping these are usually regional data'
            message = message.format(country_id, name)
            print(message)
            continue

        year_310 = country_data['poverty_rates']['3.10']['most_recent_date']
        rate_310 = country_data['poverty_rates']['3.10']['percent']
        year_190 = country_data['poverty_rates']['1.90']['most_recent_date']
        rate_190 = country_data['poverty_rates']['1.90']['percent']

        if year_310 is None or rate_310 is None or rate_310 == '0':
            countries_with_bad_data_310.add(name)
            year_310 = '{{N/A}}'
            rate_310 = '{{N/A}}'

        if year_190 is None or rate_190 is None or rate_190 == '0':
            countries_with_bad_data_190.add(name)
            year_190 = '{{N/A}}'
            rate_190 = '{{N/A}}'

        rate_190, year_190, ref_190, rate_310, year_310, ref_310 = reference_overwrite(name, rate_190, year_190, rate_310, year_310)
        row_text = build_row_text(name, rate_190, year_190, rate_310, year_310,
                                  extra_reference_190=ref_190,
                                  extra_reference_310=ref_310)
        number_valid += 1
        countries_good.add(name)
        row_texts.append(row_text)

    rows_text = ''.join(row_texts)
    #print(countries_with_bad_data_190.symmetric_difference(countries_with_bad_data_310))
    # print(old_countries.difference(countries_good))
    # print(len(old_countries))
    # print(len(countries_good))
    return rows_text


def build_row_text(name, rate_190, year_190, rate_310, year_310,
                   extra_reference_190='',
                   extra_reference_310=''):
    if extra_reference_190 is None:
        extra_reference_190 = ''
    if extra_reference_310 is None:
        extra_reference_310 = ''
    # not using standard  python string formating because of conflicts with markup
    row_break = '|-\n'
    text_190 = rate_190 + extra_reference_190 + ' || ' + year_190
    text_310 = rate_310 + extra_reference_310 + ' || ' + year_310
    rate_year_info_text = text_190 + ' || ' + text_310
    country_text = '| style="text-align:left;"| {{flag|' + name + '}} ||'
    row_text = country_text + rate_year_info_text + '\n'
    row_text = row_text + row_break
    return row_text


def post_table(wiki_table):
    '''
    current outputs to file might be cool to write direct to page
    '''
    output_file = open('output_markup', 'w')
    output_file.write(wiki_table)
    output_file.close()
    print('markup written to output_markup')


def build_table():
    poverty_data, error = world_bank_api.most_recent_poverty_data()
    if error is not None:
        print(error)
        return
    wiki_table = build_table_text(poverty_data)
    post_table(wiki_table)


if __name__ == '__main__':
    build_table()
