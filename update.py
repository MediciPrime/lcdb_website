import argparse
import hashlib
import os
import re
import sqlite3

# define md5 hashing function
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# connect to sqlite database
conn = sqlite3.connect('data-dev.sqlite')

# create 'cursor' object to add values into sqlite3 database
c = conn.cursor()

# specify directory containing files
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', help='directory containing the bed files')
parser.add_argument('-u', '--user', help='assumed user of the files', default='public')

# set d to directory location
args = parser.parse_args()
d = args.directory
u = args.user

# set file_list to the list of files from 'd'
file_list = os.listdir(d)

# iterate through the list of files and pertinent information to Bed
for f in file_list:

    # if file name contains '.bed. at the end, analyze it
    if re.search('(\.bed$)', f):
    
        # identify all rows for table Bed
        file_location = os.path.abspath(f)
        label = re.sub('(\.bed$)', '', f)
        date = os.path.getmtime(f)
        user = u
        md5val = md5(f)

        #TODO: handle situation where file is already present, i.e. md5 is not unique
        try:
            # insert values into Bed table
            c.execute('insert into Bed values (?, ?, ?, ?, ?)',
                      (file_location, label, date, user, md5val))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
