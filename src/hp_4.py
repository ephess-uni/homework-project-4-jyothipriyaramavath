# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    
    nd = [datetime.strptime(olddate, "%Y-%m-%d").strftime('%d %b %Y') for olddate in old_dates]
    return nd

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    
    x = []
    
    strd = datetime.strptime(start, '%Y-%m-%d')
    
    for i in range(n):
        
        x.append(strd + timedelta(days=i))
        
    return x


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    vlslen = len(values)
    a = date_range(start_date, vlslen(values))
    g = list(zip(a, values))
    return g

def methods1(infile):
    
    fields = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    with open(infile, 'r') as f:
        removehdr = DictReader(f, fieldnames=fields)
        removehdr_rows = [row for row in removehdr]

        removehdr_rows.pop(0)
    
    return removehdr_rows

def fees_report1(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    
    nowformat = '%m/%d/%Y'
    textdata = methods1(infile)
    feesDIct = defaultdict(float)

    for eachline in textdata:
       
        patron = eachline['patron_id']
        due = datetime.strptime(eachline['date_due'], nowformat)
        returned = datetime.strptime(eachline['date_returned'], nowformat)

        ds = (returned - due).days

        feesDIct[patron]+= 0.25 * ds if ds > 0 else 0.0

    finalList = [
        {'patron_id': pntln, 'late_fees': f'{fsrtv:0.2f}'} for pntln, fsrtv in feesDIct.items()
    ]

    with open(outfile, 'w') as f:
        r = DictWriter(f, ['patron_id', 'late_fees'])
        r.writeheader()
        r.writerows(finalList)

def fees_report(infile, outfile):
    
    infileheaders = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    fees = defaultdict(float)
    
    with open(infile, 'r') as f:
        lines = DictReader(f, fieldnames=infileheaders)
        rows = [row for row in lines]

    rows.pop(0)
       
    for each_line in rows:
       
        patronID = each_line['patron_id']
        
        date_due = datetime.strptime(each_line['date_due'], "%m/%d/%Y")
        
        date_returned = datetime.strptime(each_line['date_returned'], "%m/%d/%Y")
        daysLate = (date_returned - date_due).days
        
        fees[patronID]+= 0.25 * daysLate if daysLate > 0 else 0.0
        
            
    finalIst = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in fees.items()
    ]
    with open(outfile, 'w') as f:
        
        writer = DictWriter(f,['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(finalIst)

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    #BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    #BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report('book_returns.csv', OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
