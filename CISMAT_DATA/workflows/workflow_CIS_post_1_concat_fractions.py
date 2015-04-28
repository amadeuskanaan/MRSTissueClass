__author__ = 'kanaan' '2015_04_27'

import os
import pandas as pd



afs_dir        = '/xxx'
population_young_a = ['xxx']
workspace_a    = 'xxx'


def concat_fraction_outputs(population, workspace_dir):

    print 'creating dataframes for ACC/THA/STR voxel tissue proportions'

    list_spm = []
    list_fsl = []
    list_fsu = []


    for subject in population:

        #grab tissue proprtion data and dump into list
        spm = pd.read_csv(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_stats', 'voxel_statistics_spm.txt'), header = None)
        spm.insert(0, 'SUBJECT', subject[0:4])
        list_spm.append(spm)

        #grab tissue proprtion data and dump into list
        fsl = pd.read_csv(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_stats', 'voxel_statistics_fslfast.txt'), header = None)
        list_fsl.append(fsl)


        #grab tissue proprtion data and dump into list
        fsu = pd.read_csv(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_stats', 'voxel_statistics_freesurfer.txt'), header = None)
        list_fsu.append(fsu)


    #create concatenated dataframe for all tissue data in list

    df_spm = pd.concat(list_spm, ignore_index=True)
    df_spm.columns = ['SUBJECT', 'GM_SPM', 'WM_SPM','CSF_SPM']
    df_fsl = pd.concat(list_fsl, ignore_index=True)
    df_fsl.columns = ['GM_FSL', 'WM_SPM','CSF_FSL']
    df_fsu = pd.concat(list_fsu, ignore_index=True)
    df_fsu.columns =  ['GM_SURFER', 'WM_SURFER','CSF_SURFER']

    # combine all voxel tissue proportion data into one dataframe
    cols =  ['SUBJECT', 'GM_SPM'  , 'GM_FSL'   , 'GM_SURFER'  ,
                        'WM_SPM'  , 'WM_FSL'   , 'WM_SURFER'  ,
                        'CSF_SPM' , 'CSF_FSL'  , 'CSF_SURFER' ]

    frames = pd.concat([df_spm, df_fsl, df_fsu], axis = 1)
    #frames = frames[cols]

    frames.to_csv(os.path.join(workspace_dir, 'group_statistics', 'proportions_%s.csv'%workspace_dir[-1]))

    return frames


'######################################################################################################################################'
'######################################################################################################################################'

if __name__ == "__main__":
    concat_fraction_outputs(population_young_a, workspace_a)
    concat_fraction_outputs(population_young_b, workspace_b)
    concat_fraction_outputs(population_young_c, workspace_c)
