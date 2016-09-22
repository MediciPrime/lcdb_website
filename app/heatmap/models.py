from itertools import combinations
import subprocess
from ..models import Jaccard, PBed
from pybedtools import BedTool


class Heatmap:

    def __init__(self, files):
        self.files = files

    def jaccard_output(self):
        # go through all the file combinations via id values
        for combination in combinations(self.files, 2):
            # if the combined id from combination is not in Jaccard database
            if Jaccard.query.get(combination) == None:
                file_int = [int(char) for char in str(combination)]
                file_location1 = PBed.query.filter_by(id=file_int[0])
                file_location2 = PBed.query.filter_by(id=file_int[1])
                # create the bed files using Bedtools Jaccard
                u_intersect = BedTool(file_location1).jaccard(
                    file_location2)['jaccard']
                # sqlite table
                value = Jaccard(p_id=combination, u_inter=u_intersect)
                db.session.add(value)
                db.session.commit()

            # otherwise add the results from the bed file to the heatmap
            else:
                print(Jaccard.query.get(combination))
                # return Jaccard.query.get(combination)
