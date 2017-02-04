#!/usr/bin/env python

import argparse
import hashlib
import os
import re
import sqlite3
import yaml

class Update:

    def __init__(self, user, dirloc, organism, technique, afactor=None, wld=None,
                 dld=None, tissue=None, cline=None):
        self.user = user
        self.dirloc = dirloc
        self.organism = organism
        self.technique = technique
        self.afactor = afactor
        self.wld = wld
        self.dld = dld
        self.tissue = tissue
        self.cline = cline
        

    # define md5 hashing function
    def md5(self):
        hash_md5 = hashlib.md5()
        with open(self.file_location, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    # generate list of files, add to tables Bed and Identity
    def flist(self):

        # open and write to 'unknown' file
        unknown = open('unknown.txt', 'w')

        # generate list of files
        file_list = os.listdir(self.dirloc)

        # connect to sqlite database
        conn = sqlite3.connect('data-dev.sqlite')

        # create 'cursor' object to add values into sqlite3 database
        c = conn.cursor()

        # iterate through the list of files and pertinent information to Bed
        for f in file_list:

            file_ok = True
            
            # create a new word list
            word_list = []

            # if file name contains '.bed' at the end, analyze it
            if re.search('(\.bed$)', f):

                # remove '.bed' from label
                label = re.sub('(\.bed$)', '', f)

                # split remaining label into word list
                word_list = re.split('[-_]+', label)

                # take word_list and send it to the 'decide' method
                '''
                The 'decide' method iterates through each of the words in the
                file name, 'word_list', and updates the class 'self.' variables
                '''
                self.decide(word_list, label, unknown)

            if file_ok == True:
                # identify all rows for table Bed
                file_location = os.path.abspath(self.dirloc + f)
                label = re.sub('(\.bed$)', '', f)
                date = os.path.getmtime(file_location)
                self.file_location = file_location
                md5val = self.md5()

                #TODO: handle situation where file is already present, i.e. md5 is not unique
                try:
                    # insert values into Bed table
                    c.execute('insert into Beds values (?, ?, ?, ?, ?)',
                              (self.file_location, label, date, self.user, md5val))
                    c.execute('insert into Identities values (?, ?, ?, ?, ?, ?, ?, ?)',
                              (self.organism, self.technique, self.afactor, self.tissue, self.cline,
                               self.wld, self.dld, md5val))
                    # print('{}, {}, {}, {}, {}, {}, {}'.format(self.organism, self.technique, self.afactor,
                    #                                               self.tissue, self.cline, self.wld, self.dld))
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass

            else:
                 file_ok = True

        # close the file containing the unidentifiable file names
        unknown.close()

    # the 'decide' method will organize word_list to specific columns
    #TODO: send 'file_ok' to decide in order to establish true or false
    def decide(self, word_list, label, unknown):
        
        # determine the number of words identified
        w = 0

        # predefined dictionary
        d = {'afactor' : ['ctcf', 'cp190', 'egfp', 'h2a', 'h3ac', 'h4ac', 'h2ak5ac', 'h3', 'h3k27me1',
                          'h3k36me3', 'h3k4me1', 'h3k4me3'],
             'tissue' : ['embryo', 'heads', 'ovary', 'testes'],
             'cline' : ['kc', 'kc167', 'mbn2', 's2', 's3'],
             'wld' : ['homemade', 'clontech'],
             'dld' : ['macs2']}

        d_f = {'afactor' : ['CTCF', 'CP190', 'EGFP', 'H2A', 'H3ac', 'H4ac', 'H2AK5ac', 'H3',
                            'H3K27me1', 'H3K36me3', 'H3K4me1', 'H3K4me3'],
             'tissue' : ['Embryo', 'Heads', 'Ovary', 'Testes'],
             'cline' : ['KC167', 'KC167', 'MBN2', 'S2-DRSC', 'S3'],
             'wld' : ['Homemade', 'Clontech'],
             'dld' : ['MACS2']}
        
        # run through word_list
        for word in word_list:
            
            # iterate through key of dictionary 'd'
            for k in d:

                # check if word is in dictionary 'd'
                if word.lower() in d[k]:

                    w += 1

                    # start at the first value in d[k][v]
                    v = 0

                    '''
                    This process works by identifying the part of the dictionary containing the word.
                    If it exists then find which 'v' value it is in using the while loop.
                    Once identified, use the final dictionary 'd_f' to enter the correct punctuation.
                    '''
                    if k == 'afactor':

                        while v < len(d[k]):

                            if d[k][v] == word.lower():

                                self.afactor = d_f[k][v]
                                break

                            v += 1
                            
                    elif k == 'tissue':

                        while v < len(d[k]):

                            if d[k][v] == word.lower():

                                self.tissue = d_f[k][v]
                                break

                            v += 1

                    elif k == 'cline':

                        while v < len(d[k]):

                            if d[k][v] == word.lower():

                                self.cline = d_f[k][v]
                                break

                            v += 1

                    elif k == 'wld':

                        while v < len(d[k]):

                            if d[k][v] == word.lower():

                                self.wld = d_f[k][v]
                                break

                            v += 1

                    elif k == 'dld':

                        while v < len(d[k]):

                            if d[k][v] == word.lower():

                                self.dld = d_f[k][v]
                                break

                            v += 1

        # file name was not properly identified
        # prevent from addition to database and
        # add file name to 'unknown' file
        if w == 0:
                file_ok = False
                unknown.write(label + "\n")
                print(file_ok)

if __name__ == '__main__':
    # create object
    x = yaml.load(open('update.yaml'))
    for block in x:
        print(block)
        u = Update(**block).flist()
