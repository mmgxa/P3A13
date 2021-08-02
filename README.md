# Session 13 Readme file.


## Link to Colab file

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mmgxa/P3A13/blob/main/session13.ipynb)

## Objective
The objective of this assignment is to implement a lazy iterator that will return a named tuple of the data in each row with proper formatting for data.

The second objective is to calculate the number of violations by car make.


## Question 1

We create a function that properly formats the date entry in a particlular row.

```python
def date(value):
    '''
    This function is used to format the column with date in it.
    It will take a string in the form 10/5/2016 and return datetime.date(2016, 10, 5)
    '''
    return parse(value).date()
```

Then, we create the generator function that yields one ticket at-a-time.

```python
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
```

The code can be executed as follows:

```python
tickets = gen_ticket('nyc_parking_tickets_extract.csv')

for i in islice(tickets, 0,5):
    print(f'{i}\n')
```

Here, we used the `islice` function to return a subset (5 here) of the results.

## Question 2

We create a function that has a Counter initialized inside and it iterates over all the lines from the ticket gneerator. Also, it is sorted in descending order using the `most_common()` function.

```python
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
```

The code can be executed as follows:

```python
car_cnt = ticket_count_by_car()

for i in islice(car_cnt, 0,5):
    print(i)
```