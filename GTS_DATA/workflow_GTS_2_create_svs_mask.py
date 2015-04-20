__author__ = 'kanaan' 'March_17_2015'

import os
import errno
import string
import shutil
import subprocess
import sys
import nipype.interfaces.fsl as fsl
import shutil
import subprocess

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
valid_chars = '-_.() %s%s' %(string.ascii_letters, string.digits)

#assert len(sys.argv)== 2
#subject_index=int(sys.argv[1])

'========================================================================================'

afsdir_a           = '/a/projects/nmr093a/'
afsdir_b           = '/a/projects/nmr093b/'


workspace_a    = '/scr/sambesi2/workspace/project_MRSTissueClass/GTS/study_a'
workspace_b    = '/scr/sambesi2/workspace/project_MRSTissueClass/GTS/study_b'

test_pop       = ['HCTT']
population_a   = [ 'BM8X', 'GF3T', 'GH4T', 'GSNT', 'HCTT', 'HM1X', 'HR8T', 'LMIT', 'MJBT', 'PAHT',
                   'RB1T', 'RJBT', 'RJJT', 'RMNT', 'SDCT', 'SI5T', 'SJBT', 'STQT', 'TJ5T', 'TR4T',
                   'TSCT', 'TV1T', 'ZT5T']
                  # no retest ---- >'KDET', 'NP4T', 'WJ3T',

population_b   = [ 'BM8X', 'GF3T', 'GH4T', 'GSNT', 'HCTT', 'HM1X', 'HR8T', 'LMIT', 'MJBT', 'PAHT',
                   'RB1T', 'RJBT', 'RJJT', 'RMNT', 'SDCT', 'SI5T', 'SJBT', 'STQT', 'TJ5T', 'TR4T',
                   'TSCT', 'TV1T', 'ZT5T', ]

'========================================================================================'



def create_svs_mask_GTS_data(population, population_type, afs_dir, workspace_dir):
    count = 0
    for subject in population:
        count +=1
        print '========================================================================================'
        print '%s- CREATING SVS mask for subject %s_%s' %(count,subject, workspace_dir[-1])
        print '.'

        subject_afs         = os.path.join(afs_dir, population_type, subject, 'SVS')
        subject_workspace   = os.path.join(workspace_dir, subject)

        acc=[]
        tha=[]
        str=[]
        '========================================================================================'
        '                              Copying RDAs to local dirs                               '
        '========================================================================================'
        # locating and copying rda files from afs dir to local workspace
        for root, dirs, files, in os.walk(subject_afs, topdown= False):
            for name in files:
                if 'SUPP' in name:
                    if 'ACC' in name or 'acc' in name or 'Acc' in name:
                        acc.append(os.path.join(root, name))
                    elif 'TH' in name or 'th' in name or 'Tha' in name:
                        tha.append(os.path.join(root, name))
                    elif 'STR' in name or 'ST' in name or 'st' in name:
                        str.append(os.path.join(root, name))

        mkdir_p(os.path.join(workspace_dir, subject, 'svs_voxel_mask'))
        svs_dir = os.path.join(workspace_dir, subject, 'svs_voxel_mask')

        shutil.copy(acc[0], os.path.join(svs_dir, '%s%s_ACC_SUPPRESSED.rda' %(subject,workspace_dir[-1]) ))
        shutil.copy(tha[0], os.path.join(svs_dir, '%s%s_THA_SUPPRESSED.rda' %(subject,workspace_dir[-1]) ))
        shutil.copy(str[0], os.path.join(svs_dir, '%s%s_STR_SUPPRESSED.rda' %(subject,workspace_dir[-1]) ))


        #matlab related defenitions.... check RDA2NII.m file

        T1Path          = os.path.join(subject_workspace, 'anatomical_original' + '/')
        T1Image         = 'ANATOMICAL.nii'
        SVS_path        = os.path.join(subject_workspace, 'svs_voxel_mask' + '/')
        acc_file        = '%s%s_ACC_SUPPRESSED.rda' %(subject,workspace_dir[-1])
        tha_file        = '%s%s_THA_SUPPRESSED.rda' %(subject,workspace_dir[-1])
        str_file        = '%s%s_STR_SUPPRESSED.rda' %(subject,workspace_dir[-1])



        #run matlab code to create registered mask from rda file
        matlab_command_acc = ['matlab','-nodesktop' ,'-nosplash'  ,'-nojvm' ,'-r "RDA_TO_NIFTI(\'%s\', \'%s\', \'%s\', \'%s\') ; quit;"'
                              %(T1Path, T1Image, SVS_path, acc_file)]
        matlab_command_tha = ['matlab','-nodesktop' ,'-nosplash'  ,'-nojvm' ,'-r "RDA_TO_NIFTI(\'%s\', \'%s\', \'%s\', \'%s\') ; quit;"'
                              %(T1Path, T1Image, SVS_path, tha_file)]
        matlab_command_str = ['matlab','-nodesktop' ,'-nosplash'  ,'-nojvm' ,'-r "RDA_TO_NIFTI(\'%s\', \'%s\', \'%s\', \'%s\') ; quit;"'
                              %(T1Path, T1Image, SVS_path, str_file)]
        anatomical_dir     = os.path.join(subject_workspace, 'anatomical_original')

        '========================================================================================'
        '                                           ACC                                          '
        '========================================================================================'

        if not os.path.isfile(os.path.join(svs_dir, '%s%s_ACC_RDA_MASK.nii' %(subject,workspace_dir[-1]))):
            #run matlab command to create mask
            print 'Extracting geometry from rda and creating nifti mask for ACC'
            subprocess.call(matlab_command_acc)

            # some folder cleanup
            for file in os.listdir(anatomical_dir):
                if 'rda' in file and 'ACC' in file:
                    shutil.move(os.path.join(anatomical_dir, file),
                                os.path.join(svs_dir,  '%s%s_ACC_RDA_MASK.nii' %(subject,workspace_dir[-1])))
                elif 'coord' in file and 'acc' in file:
                    shutil.move(os.path.join(anatomical_dir, file),
                                os.path.join(svs_dir, '%s%s_ACC_RDA_coord.txt' %(subject,workspace_dir[-1])))
        else:
            print 'ACC SVS mask already created..... moving on'

        '========================================================================================'
        '                                           THA                                          '
        '========================================================================================'

        if not os.path.isfile(os.path.join(svs_dir, '%s%s_THA_RDA_MASK.nii' %(subject,workspace_dir[-1]))):
            #run matlab command to create mask
            print 'Extracting geometry from rda and creating nifti mask for THA'
            subprocess.call(matlab_command_tha)

            # cleanup
            for file in os.listdir(anatomical_dir):
                if 'rda' in file and 'THA' in file:
                    shutil.move(os.path.join(anatomical_dir, file),
                            os.path.join(svs_dir, '%s%s_THA_RDA_MASK.nii' %(subject,workspace_dir[-1])))
                elif 'coord' in file and 'th' in file:
                    shutil.move(os.path.join(anatomical_dir, file),
                                os.path.join(svs_dir, '%s%s_THA_RDA_coord.txt' %(subject,workspace_dir[-1])))
        else:
            print 'THA SVS mask already created..... moving on'
        '========================================================================================'
        '                                           STR                                          '
        '========================================================================================'

        if not os.path.isfile(os.path.join(svs_dir, '%s%s_STR_RDA_MASK.nii' %(subject,workspace_dir[-1]))):
            #run matlab command to create mask
            print 'Extracting geometry from rda and creating nifti mask for STR'
            subprocess.call(matlab_command_str)

            # cleanup
            for file in os.listdir(anatomical_dir):
                 if 'rda' in file and 'ST' in file:
                     shutil.move(os.path.join(anatomical_dir, file),
                                 os.path.join(svs_dir, '%s%s_STR_RDA_MASK.nii' %(subject,workspace_dir[-1])))
                 elif 'coord' in file and 'st' in file:
                    shutil.move(os.path.join(anatomical_dir, file),
                                os.path.join(svs_dir, '%s%s_STR_RDA_coord.txt' %(subject,workspace_dir[-1])))
        else:
            print 'STR SVS mask already created..... moving on'

        print '========================================================================================'

if __name__ == "__main__":
    #create_svs_mask_GTS_data(test_pop, 'probands', afsdir_a, workspace_a)
    create_svs_mask_GTS_data(population_a, 'probands', afsdir_a, workspace_a)
    create_svs_mask_GTS_data(population_b, 'probands', afsdir_b, workspace_b)

