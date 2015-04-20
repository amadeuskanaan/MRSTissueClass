__author__ = 'kanaan'


import os
import numpy as np
import nibabel as nb
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.fsl as fsl
# import nipype.pipeline.engine as pe
# import nipype.interfaces.io as nio

workspace_a    = '/scr/sambesi2/workspace/project_MRSTissueClass/CISMAT/study_a/'
population     = ['BB2T040407.TRIO']

workspace_a    = '/scr/sambesi2/workspace/project_MRSTissueClass/CISMAT/study_a'
workspace_b    = '/scr/sambesi2/workspace/project_MRSTissueClass/CISMAT/study_b'
workspace_c    = '/scr/sambesi2/workspace/project_MRSTissueClass/CISMAT/study_c'

population_young_a = ['BB2T040407.TRIO', 'EK5T040407.TRIO', 'FM4T040330.TRIO', 'GA3T040405.TRIO', 'KM4T040427.TRIO',                   # 'HS5T040712.TRIO',
                      'ME1T040628.TRIO', 'MH4T040407.TRIO', 'NC2T040405.TRIO', 'NT2T040407.TRIO', 'WM8T040420.TRIO','ZK1T040405.TRIO']
population_young_b = ['BB2T040628.TRIO', 'EK5T040706.TRIO', 'FM4T040712.TRIO',                    'HS5T040810.TRIO', 'KM4T040719.TRIO', # 'GA3T040629.TRIO' no rda
                      'ME1T040712.TRIO', 'MH4T040628.TRIO', 'NC2T040712.TRIO', 'NT2T040628.TRIO', 'WM8T040706.TRIO', 'ZK1T040628.TRIO']
population_young_c = ['BB2T040719.TRIO', 'EK5T040719.TRIO', 'FM4T040727.TRIO', 'GA3T040907.TRIO', 'HS5T040901.TRIO','ME1T040803.TRIO',
                                         'MH4T040719.TRIO', 'NC2T040810.TRIO', 'NT2T040712.TRIO', 'WM8T040719.TRIO', 'ZK1T040713.TRIO']


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



def calculate_overlap(population_a, population_b, workspace_a, workspace_b, voxel_name):

    #* Retest MRS voxels (STUDY_B) are registered to test MRS voxel (STUDY_A)
    #* The Sorenson Dice metric between the two voxels is calculated to quantif the agreement between the two visits.

    ## anat_b is first registered to anat_a;
    ## affine xfm is then applied to mrs_b
    ## affines of mrs_a and mrs_ are checked.


    for subject in population_a and population_b:
        print '###################################################################################'
        print '                 Running %s MRS voxel registration for subject %s' %(voxel_name, subject)
        print '                 ---------------------------------------------------'
        print ''

        anat_a   = os.path.join(workspace_a, subject, 'anatomical_original', 'ANATOMICAL.nii')
        voxel_a  = os.path.join(workspace_a, subject, 'svs_voxel_mask', '%sa_%s_RDA_MASK.nii'%(subject,voxel_name))

        anat_b   = os.path.join(workspace_b, subject, 'anatomical_original', 'ANATOMICAL.nii')
        voxel_b  = os.path.join(workspace_b, subject, 'svs_voxel_mask', '%sb_%s_RDA_MASK.nii'%(subject,voxel_name))

        try:
           os.makedirs(os.path.join(os.path.join(workspace_b, subject, 'dice')))
        except OSError:
            pass

        dice_dir = os.path.join(os.path.join(workspace_b, subject, 'dice'))

        if os.path.isfile(os.path.join(dice_dir, 'anat_b2a.nii.gz')):
            print 'Anatomical registration already completed...moving on'
        else:
            print 'Registering anat_b to anat_a'
            # Running registration anat_a to anat_b
            import nipype.interfaces.fsl as fsl
            flirt = fsl.FLIRT ( bins=640, cost_func= 'mutualinfo')
            flirt.inputs.in_file         = anat_b
            flirt.inputs.reference       = anat_a
            flirt.inputs.out_file        = os.path.join(dice_dir, 'anat_b2a.nii.gz')
            flirt.inputs.out_matrix_file = os.path.join(dice_dir, 'anat_b2a.mat')
            flirt.run()

        # apply transform to voxel_b
        print 'Registering voxe_b to voxel_a'
        mat = os.path.join(dice_dir, 'anat_b2a.mat')
        from nipype.interfaces import fsl
        apply_xfm                        = fsl.ApplyXfm()
        apply_xfm.inputs.in_file         = voxel_b
        apply_xfm.inputs.in_matrix_file  = mat
        apply_xfm.inputs.out_file        = os.path.join(dice_dir, '%s_b2a.nii.gz'%voxel_name)
        apply_xfm.inputs.reference       = anat_a
        apply_xfm.inputs.apply_xfm       = True
        apply_xfm.run()

        voxel_b2a = os.path.join(dice_dir, '%s_b2a.nii.gz'%voxel_name)
        dice_file = os.path.join(dice_dir, 'dice_%s.txt'%voxel_name)

        # calculate dice
        print 'Calculating Dice Metric'
        dice_val   = dice_metric(voxel_b2a, voxel_a)
        dice_write = open(dice_file, 'w')
        dice_write.write('%s'%dice_val)
        dice_write.close()

calculate_overlap(population_a, population_b, workspace_a, workspace_b, 'ACC')
calculate_overlap(population_a, population_b, workspace_a, workspace_b, 'THA')
calculate_overlap(population_a, population_b, workspace_a, workspace_b, 'STR')
