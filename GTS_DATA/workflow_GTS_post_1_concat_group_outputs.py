__author__ = 'kanaan' 'April 09 2015'

import os
import pandas as pd
import string

#'========================================================================================'
workspace_a    = '/scr/sambesi2/workspace/project_MRSTissueClass/GTS/study_a'
workspace_b    = '/scr/sambesi2/workspace/project_MRSTissueClass/GTS/study_b'

test_pop       = ['SI5T']
population_a   = [ 'BM8X', 'GF3T', 'GH4T', 'GSNT', 'HCTT', 'HM1X', 'HR8T', 'LMIT', 'MJBT', 'PAHT',
                   'RB1T', 'RJBT', 'RJJT', 'RMNT', 'SDCT', 'SI5T', 'SJBT', 'STQT', 'TJ5T', 'TR4T',
                   'TSCT', 'TV1T', 'ZT5T']
                  # no retest ---- >'KDET', 'NP4T', 'WJ3T',

population_b   = [ 'BM8X', 'GF3T', 'GH4T', 'GSNT', 'HCTT', 'HM1X', 'HR8T', 'LMIT', 'MJBT', 'PAHT',
                   'RB1T', 'RJBT', 'RJJT', 'RMNT', 'SDCT', 'SI5T', 'SJBT', 'STQT', 'TJ5T', 'TR4T',
                   'TSCT', 'TV1T', 'ZT5T', ]

#'========================================================================================'


def concat_lcmodel_outputs(population, workspace_dir, voxel_name):
    print '========================================================================================'
    print '                                  %s_%s'%(voxel_name, workspace_dir[-1])
    print ''
    print ' 1-Concatenating %s_%s LCMODEL outputs into a single dataframe' %(voxel_name, workspace_dir[-1])

    # get metabolite data for each subject and append to a list
    count =0
    csv_list = []
    for subject in population:
        count +=1
        #print '%s-Grabbing metabolite data for subject %s_%s'%(count,subject, workspace_dir[-1])

        csv   = os.path.join(workspace_dir, subject, 'lcmodel', voxel_name, 'spreadsheet.csv')
        if os.path.isfile(csv):
            reader = pd.read_csv(csv)
            reader.insert(0, 'Subject', subject)
            csv_list.append(reader)

    # creat a dataframe and place reliable metabolite data for every subject
    df = pd.concat(csv_list, ignore_index = True)
    reliable = df.loc[:,['Subject'   ,
                         ' Cre',      ' Cre %SD',
                         ' GPC+PCh',  ' GPC+PCh %SD',
                         ' NAA+NAAG', ' NAA+NAAG %SD',
                         ' mI',       ' mI %SD',
                         ' Glu',      ' Glu %SD',
                         ' Gln',      ' Gln %SD',
                         ' Glu+Gln',  ' Glu+Gln %SD']]

    # sort subjects alphabetically and rest index....
    reliable.sort(columns='Subject', inplace=True)
    reliable.reset_index(drop = True, inplace=True)

    # create output dir
    try:
        os.makedirs(os.path.join(workspace_dir, 'group_statistics'))
    except OSError:
       results_dir =  str(os.path.join(workspace_dir, 'group_statistics'))
    results_dir =  str(os.path.join(workspace_dir, 'group_statistics'))


    # save reliable dataframe as a csv in output folder
    print ''
    print '.....Saving relibale metabolite concentrations in a dataframe'

    reliable.to_csv(os.path.join(results_dir, 'quantitation_%s_%s_lcmodel.csv'%(voxel_name, workspace_dir[-1])))


    print ''
    print ' 2-Concatenating %s_%s Tissue proportions into a single dataframe'%(voxel_name, workspace_dir[-1])

    list_spm = []
    list_fsl = []
    list_fsu = []



    print '.....creating dataframes for ACC/THA/STR voxel tissue proportions'

    for subject in population:

        #small fix for data grabbing
        if voxel_name is 'THA':
            voxel = 'tha'
        elif voxel_name is 'STR':
            voxel = 'str'
        elif voxel_name is 'ACC':
            voxel = 'ACC'
        # grab tissue proportion data for all subjects and dump into list

        spm = pd.read_csv(os.path.join(workspace_dir, subject, 'svs_voxel_stats', '%s_voxel_statistics_spm.txt'%voxel), header = None)
        spm.insert(0, 'SUBJECT', subject)
        list_spm.append(spm)

        fsl = pd.read_csv(os.path.join(workspace_dir, subject, 'svs_voxel_stats', '%s_voxel_statistics_fslfast.txt'%voxel), header = None)
        list_fsl.append(fsl)

        fsu = pd.read_csv(os.path.join(workspace_dir, subject, 'svs_voxel_stats', '%s_voxel_statistics_freesurfer.txt'%voxel), header = None)
        list_fsu.append(fsu)

    # create concatenated datafram for all tissue data in list
    df_spm = pd.concat(list_spm, ignore_index=True)
    df_spm.columns = ['SUBJECT', 'GM_SPM_%s'%voxel_name,'WM_SPM_%s'%voxel_name,'CSF_SPM_%s'%voxel_name]
    df_fsl = pd.concat(list_fsl, ignore_index=True)
    df_fsl.columns = ['GM_FSL_%s'%voxel_name,'WM_FSL_%s'%voxel_name,'CSF_FSL_%s'%voxel_name]
    df_fsu = pd.concat(list_fsu, ignore_index=True)
    df_fsu.columns = ['GM_SURFER_%s'%voxel_name,'WM_SURFER_%s'%voxel_name,'CSF_SURFER_%s'%voxel_name]


    # combine all voxel tissue proportion data into one dataframe
    cols =  ['SUBJECT', 'GM_SPM_%s' %voxel_name , 'GM_FSL_%s' %voxel_name  , 'GM_SURFER_%s' %voxel_name  ,
                        'WM_SPM_%s' %voxel_name , 'WM_FSL_%s' %voxel_name  , 'WM_SURFER_%s' %voxel_name  ,
                        'CSF_SPM_%s'%voxel_name , 'CSF_FSL_%s'%voxel_name  , 'CSF_SURFER_%s'%voxel_name ]

    frames = pd.concat([df_spm, df_fsl, df_fsu], axis = 1)
    frames = frames[cols]

    frames.to_csv(os.path.join(workspace_dir, 'group_statistics', 'proportions_%s_%s.csv'%(voxel_name, workspace_dir[-1])))
    return frames


if __name__ == "__main__":
    concat_lcmodel_outputs(population_a, workspace_a, 'ACC')
    concat_lcmodel_outputs(population_a, workspace_a, 'THA')
    concat_lcmodel_outputs(population_a, workspace_a, 'STR')

    concat_lcmodel_outputs(population_b, workspace_b, 'ACC')
    concat_lcmodel_outputs(population_b, workspace_b, 'THA')
    concat_lcmodel_outputs(population_b, workspace_b, 'STR')
