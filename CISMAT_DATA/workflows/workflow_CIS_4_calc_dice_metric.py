__author__ = 'kanaan' '2015_04_27'


import os
import numpy as np
import nibabel as nb
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.fsl as fsl
# import nipype.pipeline.engine as pe
# import nipype.interfaces.io as nio

populationA     = ['xxx']
populationB     = ['xxx']
populationC     = ['xxx']

workspace_a    = '/xxx/study_a'
workspace_b    = '/xxx/study_b'
workspace_c    = '/xxx/study_c'




def dice_metric(svs_1, svs_2):
    """
    Method to compute the Sorensen-Dice coefficient between two binary nifti images.
    """

    import nibabel as nb
    import numpy
    #read in data
    vox_1_data = nb.load(svs_1).get_data()
    vox_2_data = nb.load(svs_2).get_data()

    vox_1_bool= numpy.atleast_1d(vox_1_data.astype(numpy.bool))
    vox_2_bool= numpy.atleast_1d(vox_2_data.astype(numpy.bool))

    intersection = numpy.count_nonzero(vox_1_bool & vox_2_bool)

    vox_1_total = numpy.count_nonzero(vox_1_bool)
    vox_2_total = numpy.count_nonzero(vox_2_bool)

    try:
        dice = 2. * intersection / float(vox_1_total + vox_2_total)
    except ZeroDivisionError:
        dice = 0.0

    return dice




def calculate_overlap_cismat(population_a, population_b, population_c, workspace_a, workspace_b, workspace_c):

    #* Retest MRS voxels (STUDY_B) are registered to test MRS voxel (STUDY_A)
    #* The Sorenson Dice metric between the two voxels is calculated to quantif the agreement between the two visits.

    ## anat_b is first registered to anat_a;
    ## affine xfm is then applied to mrs_b
    ## affines of mrs_a and mrs_ are checked.


    for subject in population_a and population_b and population_c:
        print '###################################################################################'
        print '                 Running CISMAT MRS voxel registration for subject %s' %subject
        print '                 ---------------------------------------------------'
        print ''

        anat_a    = os.path.join(workspace_a, subject[0:4], 'anatomical_original', 'ANATOMICAL.nii')
        vox_dir_a = os.path.join(workspace_a, subject[0:4], 'svs_voxel_mask')
        voxel_a   = str([os.path.join(vox_dir_a, vox) for vox in os.listdir(vox_dir_a) if vox.endswith('nii')][0])

        anat_b    = os.path.join(workspace_b, subject[0:4], 'anatomical_original', 'ANATOMICAL.nii')
        vox_dir_b = os.path.join(workspace_b, subject[0:4], 'svs_voxel_mask')
        voxel_b   = str([os.path.join(vox_dir_b, vox) for vox in os.listdir(vox_dir_b) if vox.endswith('nii')][0])

        anat_c    = os.path.join(workspace_c, subject[0:4], 'anatomical_original', 'ANATOMICAL.nii')
        vox_dir_c = os.path.join(workspace_c, subject[0:4], 'svs_voxel_mask')
        voxel_c   = str([os.path.join(vox_dir_c, vox) for vox in os.listdir(vox_dir_c) if vox.endswith('nii')][0])

        print voxel_a
        #print voxel_b
        print voxel_c


        #create output dir
        try:
           os.makedirs(os.path.join(os.path.join(workspace_c, subject[0:4], 'dice')))
        except OSError:
            pass

        dice_dir_c = os.path.join(os.path.join(workspace_c, subject[0:4], 'dice'))


        print '========================================================================================'
        print '                              Running VOXEL C to B Registration                         '
        print '========================================================================================'

        if os.path.isfile(os.path.join(dice_dir_c, 'anat_c2b.nii.gz')):
            print 'Anatomical registration already completed...moving on'
        else:
            print 'Registering anat_c to anat_b'
            # Running registration anat_a to anat_b
            import nipype.interfaces.fsl as fsl
            flirt = fsl.FLIRT (bins =256, dof = 6,  cost_func='mutualinfo')
            flirt.inputs.in_file         = anat_c
            flirt.inputs.reference       = anat_b
            flirt.inputs.searchr_x       = [-90,90]
            flirt.inputs.searchr_y       = [-90,90]
            flirt.inputs.searchr_z       = [-90,90]
            flirt.inputs.out_file        = os.path.join(dice_dir_c, 'anat_c2b.nii.gz')
            flirt.inputs.out_matrix_file = os.path.join(dice_dir_c, 'anat_c2b.mat')
            flirt.run()

        # apply transform to voxel_c
        print 'Registering voxe_c to voxel_b'
        mat_c2b = os.path.join(dice_dir_c, 'anat_c2b.mat')
        from nipype.interfaces import fsl
        apply_xfm                        = fsl.ApplyXfm()
        apply_xfm.inputs.in_file         = voxel_c
        apply_xfm.inputs.in_matrix_file  = mat_c2b
        apply_xfm.inputs.out_file        = os.path.join(dice_dir_c, 'svs_c2b.nii.gz')
        apply_xfm.inputs.reference       = anat_c
        apply_xfm.inputs.apply_xfm       = True
        apply_xfm.run()

        voxel_c2b = os.path.join(dice_dir_c, 'svs_c2b.nii.gz')
        dice_file_c2b = os.path.join(dice_dir_c, 'dice_c2b.txt')

        # calculate dice
        print 'Calculating Dice Metric'
        dice_c2b   = dice_metric(voxel_c2b, voxel_b)
        dice_c2b_write = open(dice_file_c2b, 'w')
        dice_c2b_write.write('%s'%dice_c2b)
        dice_c2b_write.close()


'######################################################################################################################################'

if __name__ == "__main__":
    calculate_overlap_cismat(populationA, populationB, populationC, workspace_a, workspace_b, workspace_c)