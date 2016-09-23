from itertools import combinations
import subprocess
from ..models import Jaccard, PBed
from pybedtools import BedTool
from .. import db


class Heatmap:

    def __init__(self, files):
        self.files = files

    def jaccard_output(self):
        # go through all the file combinations via id values
        for combination in combinations(self.files, 2):
            combined = magic(combination)
            # if the combined id from combination is not in Jaccard
            # database
            if Jaccard.query.get(combined) == None:
                # take combination and find individual files
                file_location1 = PBed.query.get(
                    combination[0]).file_location
                file_location2 = PBed.query.get(
                    combination[1]).file_location
                # create the bed files using Bedtools Jaccard
                u_intersect = BedTool(file_location1).jaccard(
                    file_location2)['jaccard']
                # sqlite table
                value = Jaccard(p_id=combined, u_inter=u_intersect)
                db.session.add(value)
                db.session.commit()


def magic(numList):
    s = ''.join(map(str, numList))
    return int(s)
