__author__ = 'kanaan' 'Feb_20_2015'

import os
import errno
import string
import shutil
import subprocess



rda_dir        = '/XXX'

afs_dir        = '/xxx'
population_young_a = ['xxx']
workspace_a    = 'xxx'


def create_svs_mask_CISMAT_data(population, workspace_dir, rda_dir):
    for subject in population:
        print '========================================================================================'
        print 'Reconstructing SVS voxel for subject %s_%s' %(subject[0:4], subject[4:10])
        print '.'
        subject_dir     = str(os.path.join(workspace_dir, subject[0:4]))


        if os.path.isfile(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_mask', '%s_RDA_MASK.nii'%subject[0:10])):
            print 'MRS mask already created....... moving on'
        else:
            print '..... Creating SVS mask from RDA Direction Cosines'

            # create destination directory for RDA file
            try:
                os.makedirs(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_mask'))
            except OSError:
                out_svs_dir  = str(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_mask'))
            out_svs_dir  = str(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_mask'))

            #copy rda file into workspace dir
            shutil.copy(str(os.path.join(rda_dir      , '%s.rda'%subject[0:10])),
                        str(os.path.join(out_svs_dir  , '%s.rda'%subject[0:10])))

            #matlab related defenitions.... check RDA2NII.m file

            T1Path          = str(os.path.join(subject_dir, 'anatomical_original' + '/'))
            T1Image         = 'ANATOMICAL.nii'
            SVS_path        = str(os.path.join(out_svs_dir + '/'))
            SVS_file        = '%s.rda'%subject[0:10]

            print '..... Starting Matlab no splash and runnning reconstruction'

            #run matlab code to create registered mask from rda file
            matlab_command = ['matlab'     ,
                              '-nodesktop' ,
                              '-nosplash'  ,
                              '-nojvm'     ,
                              '-r "RDA_TO_NIFTI(\'%s\', \'%s\', \'%s\', \'%s\') ; quit;"' %(T1Path, T1Image, SVS_path, SVS_file)]

            subprocess.call(matlab_command)


            # some folder cleanup and renaming
            anatomical_dir = str(os.path.join(subject_dir, 'anatomical_original'))
            for file in os.listdir(anatomical_dir):
                if 'rda' in file:
                    shutil.move(str(os.path.join(anatomical_dir, file)),
                                str(os.path.join(out_svs_dir, '%s_RDA_MASK.nii'%subject[0:10])))
                if 'coord' in file:
                    shutil.move(str(os.path.join(anatomical_dir, file)),
                                str(os.path.join(out_svs_dir, file)))

            if os.path.isfile(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_mask', '%s_RDA_MASK.nii'%subject[0:10])):
                print '..... SVS mask succesfully created'
                print 'check %s' %(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_mask'))

            print '========================================================================================'

if __name__ == "__main__":
    create_svs_mask_CISMAT_data(population_young_a, workspace_a, rda_dir)
    create_svs_mask_CISMAT_data(population_young_b, workspace_b, rda_dir)
    create_svs_mask_CISMAT_data(population_young_c, workspace_c, rda_dir)


