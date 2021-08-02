from collections import namedtuple, Counter
from dateutil.parser import parse
from itertools import islice

def date(value):
    '''
    This function is used to format the column with date in it.
    It will take a string in the form 10/5/2016 and return datetime.date(2016, 10, 5)
    '''
    return parse(value).date()       


def gen_ticket(file):
    '''
    This is a generator that yields one line from the file on each iteration
    Because we want lazy operation, the row is formatted just before yielding and
    not for all rows immediately when it is called
    '''
    with open(file, encoding='utf8', errors='ignore') as f:
        # the first line is the header; this is used to
        # create the names for elements in the namedtuple
        header = next(f).strip().split(',')
        header = [x.replace(" ", "") for x in header]
        # data type for each column in the file
        data_type = [int, str, str, str, date, int, str, str, str]
        Ticket = namedtuple('Ticket', header )
        for line in f:
            line = line.strip().split(',')
            data = (type(field) for type, field in zip(data_type, line))
            yield Ticket(*data)


tickets = gen_ticket('nyc_parking_tickets_extract.csv')


for i in islice(tickets, 0,5):
    print(f'{i}\n')


def ticket_count_by_car():
    '''
    This will sum the violations by car model
    It will iterate over all rows in the generator
    '''

    # We initialize a counter to keep count of all the models
    ticket_cnt = Counter()

    for ticket in tickets:
        ticket_cnt.update([ticket.VehicleMake])

    # The most_common method sorts in descending order
    for key, value in ticket_cnt.most_common():
        yield (key, value)

car_cnt = ticket_count_by_car()

for i in islice(car_cnt, 0,5):
    print(i)
