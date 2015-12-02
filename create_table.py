'''
we need tests
we need python tools
we need to put this on git hub
read all comments
'''


def get_table_data():
    '''
    input file 
    so these seem to be common only seperated
    there is one header column
    this give the percentage of people below the specified income for a year
    columns look like
    description,full name, countriy code, percentage for year,[next year],[next year]

    output file looks like
    
    '''
    csv_file = download_table_data()
    for line in csv_file:
        pass


def download_table_data():
    '''
    currently manually gotten from
    http://databank.worldbank.org/data/reports.aspx?source=poverty-and-equity-database#
    
    needs to use an api or if that fails wget
    we may even be able to avoid parsing with a good api
    '''

    csv_file = open('~/Downloads/Data_Extract_From_Poverty_and_Equity_Database_Data.csv')
    return csv_file

def build_wiki_table():
    # should just return the text
    pass

def post_table(wiki_table):
    # api if possible otherwise got to hack it or maybe just print the full edit for now
    pass


def build_table():
    table_data = get_table_data()
    wiki_table = build_wiki_table()
    post_table(wiki_table)


if __name__ == '__main__':
    build_table()
