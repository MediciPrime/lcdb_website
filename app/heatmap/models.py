from itertools import permutations
import subprocess
from ..models import Bed, Colocalization
from pybedtools import BedTool
from .. import db


class Heatmap(object):

    def __init__(self, files, method):
        self.files = files
        self.method = method

    def determine_method(self):
        if self.method == 'Jaccard':
            return self.jaccard_output()
        elif self.method == 'Fisher Exact':
            return fisher_exact(self)
        elif self.method == 'GAT Log Fold':
            return gat_log_fold(self)
        elif self.method == 'GAT Percent Overlay':
            return gat_percent_overlay(self)
        elif self.method == 'Interval Stats':
            return interval_stats(self)
        # include flash statement for user to select a method
        else:
            print("something is not right")

    def jaccard_output(self):
        # go through all the file combinations via id values
        for permutation in permutations(self.files, 2):
            f_l1 = permutation[0]
            f_l2 = permutation[1]
            m = self.method
            # split list of permutations
            if Colocalization.query.filter_by(file_location1=f_l1, file_location2=f_l2, method=m).first() is None:
                # create the bed files using Bedtools Jaccard
                u_inter = BedTool(f_l1).jaccard(f_l2)['jaccard']
                # sqlite table
                data_value = Colocalization(file_location1=f_l1,
                                            file_location2=f_l2, method=m, value=u_inter)
                db.session.add(data_value)
                db.session.commit()
            else:
                data_value = Colocalization.query.filter_by(file_location1=f_l1,
                                            file_location2=f_l2, method=m).first()
                print(data_value)

    def fisher_exact(self):
        pass

    def gat_log_fold(self):
        pass

    def gat_percent_overlay(self):
        pass

    def interval_stats(self):
        pass
