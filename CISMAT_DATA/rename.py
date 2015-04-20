__author__ = 'kanaan' '19.03.2015'
import os
import shutil
def reanme_and_dump(population, out_dir ):
    count= 0
    for subject in population:
        count +=1
        sub_dir = os.path.join(out_dir, subject)

        for file in os.listdir(sub_dir):
            shutil.move(file, file + '%s'%count)



