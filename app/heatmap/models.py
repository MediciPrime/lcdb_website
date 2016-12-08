from itertools import product
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
        # empty list
        nodeList = []
        linkList = []
        source = 0
        target = 0
        # split list of permutations
        for jvalue in product(self.files, repeat=2):
            f_l1 = jvalue[0]
            f_l2 = jvalue[1]
            md5_1 = Bed.query.filter_by(file_location=f_l1).first().md5
            md5_2 = Bed.query.filter_by(file_location=f_l2).first().md5
            m = self.method
            # fill colocalization table with jaccard values
            # determine if sqlite has jaccard value for query, if not then add
            if Colocalization.query.filter_by(md5_1=md5_1, md5_2=md5_2, method=m).first() is None:
                # create the bed files using Bedtools Jaccard
                u_inter = BedTool(f_l1).jaccard(f_l2)['jaccard']
                # use md5 values for each file
                # create sqlite table value then add and submit
                data_value = Colocalization(method=m, value=u_inter, md5_1=md5_1, md5_2=md5_2)
                db.session.add(data_value)
                db.session.commit()

            # create the json object in correct order, linked to heatmap.js
            # 0,0 0,1 1,1; 0,0 0,1 0,2 1,0 1,1 1,2 2,0 2,1 2,2; and so on...
            if source == 0 and target == 0:
                f_lab = Bed.query.filter_by(file_location=f_l1).first().label
                nodeList.append({'name': f_lab, 'yoclust': 1})
                jcard = Colocalization.query.filter_by(
                    md5_1=md5_1, md5_2=md5_2, method='Jaccard').first().value
                linkList.append({'source': source, 'target': target, 'jaccard': jcard})
                target += 1
            elif f_lab == Bed.query.filter_by(file_location=f_l1).first().label and source == 0:
                jcard = Colocalization.query.filter_by(md5_1=md5_1, md5_2=md5_2, method='Jaccard').first().value
                linkList.append({'source': source, 'target': target, 'jaccard': jcard})
                target += 1
            elif f_lab == Bed.query.filter_by(file_location=f_l1).first().label:
                jcard = Colocalization.query.filter_by(
                    md5_1=md5_1, md5_2=md5_2, method='Jaccard').first().value
                target += 1
                linkList.append({'source': source, 'target': target, 'jaccard': jcard})
            else:
                target = 0
                source += 1
                f_lab = Bed.query.filter_by(file_location=f_l1).first().label
                nodeList.append({'name': f_lab, 'yoclust': 1})
                jcard = Colocalization.query.filter_by(
                    md5_1=md5_1, md5_2=md5_2, method='Jaccard').first().value
                linkList.append({'source': source, 'target': target, 'jaccard': jcard})

        return nodeList, linkList
    

    def fisher_exact(self):
        pass

    def gat_log_fold(self):
        pass

    def gat_percent_overlay(self):
        pass

    # create this metric next
    def interval_stats(self):
        pass
