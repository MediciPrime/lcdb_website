from itertools import product
import subprocess
from ..models import RNAseq
from subprocess import call
from .. import db
import pandas


class Scatter(object):

    # given 'RNAseq Files' and 'Adjpval'
    def __init__(self, files, adjpval):
        self.files = files
        self.adjpval = adjpval

    # return a dictionary with 'baseMean', 'log2FC' and 'name'
    # initial thought is open and read the file to extract and return required parts
    def get_dictionary(self):
        rnadata = pandas.read_table(self.files[0])
        rnadata = rnadata[['baseMean', 'log2FoldChange', 'name']]
        rnadict = rnadata.to_dict('records')
        return rnadict
