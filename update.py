import argparse
import hashlib
import os
import re
import sqlite3
import yaml

class Update:

    def __init__(self, user, dirloc, organism, technique, afactor, tissue=None, cline=None):
        self.user = user
        self.organism = organism
        self.technique = technique
        self.afactor = afactor
        self.tissue = tissue
        self.cline = cline
        self.dirloc = dirloc

    # define md5 hashing function
    def md5(self):
        hash_md5 = hashlib.md5()
        with open(self.file_location, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    # generate list of files, add to tables Bed and Identity
    def flist(self):

        # generate list of files
        file_list = os.listdir(self.dirloc)

        # connect to sqlite database
        conn = sqlite3.connect('data-dev.sqlite')

        # create 'cursor' object to add values into sqlite3 database
        c = conn.cursor()

        # iterate through the list of files and pertinent information to Bed
        for f in file_list:

            # if file name contains '.bed. at the end, analyze it
            if re.search('(\.bed$)', f):
        
                # identify all rows for table Bed
                file_location = os.path.abspath(self.dirloc + f)
                label = re.sub('(\.bed$)', '', f)
                date = os.path.getmtime(file_location)
                self.file_location = file_location
                md5val = self.md5()

                #TODO: handle situation where file is already present, i.e. md5 is not unique
                try:
                    # insert values into Bed table
                    c.execute('insert into Bed values (?, ?, ?, ?, ?)',
                              (self.file_location, label, date, self.user, md5val))
                    c.execute('insert into Identity values (?, ?, ?, ?, ?, ?)',
                              (self.organism, self.technique, self.afactor, self.tissue, self.cline, md5val))
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass
                
# create object
x = yaml.load(open('update.yaml'))
for block in x:
    print(block)
    u = Update(**block).flist()
