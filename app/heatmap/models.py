from itertools import permutations
import subprocess
from ..models import Bed, Colocalization
from pybedtools import BedTool
from .. import db


class Heatmap:

    def __init__(self, files, method):
        self.files = files
        self.method = method

    def determine_method(self):
        if method[0] == 'Jaccard':
            return jaccard_output(self)
        elif method[0] == 'Fisher Exact':
            return fisher_exact(self)
        elif method[0] == 'GAT Log-Fold':
            return gat_log_fold(self)
        elif method[0] == 'GAT Percent Overlay':
            return gat_percent_overlay(self)
        elif method[0] == 'Interval Stats':
            return interval_stats(self)
        # include flash statement for user to select method
        else:
            pass

    def jaccard_output(self):
        # go through all the file combinations via id values
        for permutation in permutations(self.files, 2):
            file_location1 = permutation[0]
            file_location2 = permutation[1]
            method = method[0]
            # split list of permutations
            if Colocalization.query.filter_by(file_location1=file_location1, file_location2=file_location2, method=method) == None:
                # create the bed files using Bedtools Jaccard
                u_inter = BedTool(file_location1).jaccard(
                    file_location2)['jaccard']
                # sqlite table
                data_value = Colocalization(file_location1=file_location1,
                                            file_location2=file_location2, method=method, value=u_inter)
                db.session.add(data_value)
                db.session.commit()

    def fisher_exact(self):
        pass

    def gat_log_fold(self):
        pass

    def gat_percent_overlay(self):
        pass

    def interval_stats(self):
        pass


def magic(numList):
    s = ''.join(map(str, numList))
    return int(s)
