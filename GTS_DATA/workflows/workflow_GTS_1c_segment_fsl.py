__author__ = 'kanaan' 'Feb_20_2015'

import os
import sys
import nipype.interfaces.fsl as fsl
import shutil
import subprocess

#assert len(sys.argv)== 2
#subject_index=int(sys.argv[1])

'========================================================================================'

afs_dir_a      =  '/xxx'
afs_dir_b      =  '/xxx'

workspace_a    = '/scr/xxx'
workspace_b    = '/scr/xxx'

population_a   = [ 'xxx']

population_b   = [ 'xxx', ]


'========================================================================================'

def segment_fslFAST(population, afs_dir, workspace_dir):
    count= 0
    #subject = population[subject_index]
    for subject in population:
        count +=1
        print '========================================================================================'
        print '%s- Runnning FSL FAST Segmentation on subject %s_%s' %(count, subject, workspace_dir[-1])
        print ''

        # define subject directory and anatomical file path
        afs_anatomical = os.path.join(afs_dir, 'probands', subject, 'NIFTI', 'MP2RAGE_BRAIN.nii')

        # define destination directory for fsl segmentation outputs
        try:
            os.makedirs(os.path.join(workspace_dir, subject, 'segmentation_fslFAST'))
        except OSError:
            out_dir  = str(os.path.join(workspace_dir, subject, 'segmentation_fslFAST'))
        out_dir  = str(os.path.join(workspace_dir, subject, 'segmentation_fslFAST'))

        '============================================================================================'
        '                       Converting dims of spectre deskulled mp2rage to spm space	     	 '
        '============================================================================================'

        # fslFAST needs a skullstripped brain.
        # BET fails with mp2rage
        # necessary that skullstripped mp2rage is in same orientation as spm mp2rage input
        # swap dims fails to conert to AIL.
        # solution, flip to radiological, swapdim to AIL, and then switch back to neurological.

        # flipping to radiological
        #print 'Forcing radiological..............................'
        shutil.copy(afs_anatomical, out_dir)
        local_anatomical = os.path.join(out_dir, 'MP2RAGE_BRAIN.nii')
        force_radiological = ['fslorient', '-forceradiological', '%s'%local_anatomical]
        subprocess.call(force_radiological)

        #swap dims
        if os.path.isfile(os.path.join(out_dir, 'MP2RAGE_BRAIN_swapdim.nii.gz')):
            print 'Dimensions already swapped .......................... moving on'
        else:
            print 'Swapping dimensions of freesurfer files to AIL....'

        swapdim_t1 = fsl.SwapDimensions()
        swapdim_t1.inputs.in_file     = local_anatomical
        swapdim_t1.inputs.new_dims    = ('AP', 'IS', 'LR')
        swapdim_t1.inputs.out_file    = '%s/MP2RAGE_BRAIN_swapdim.nii.gz' %out_dir
        swapdim_t1.inputs.output_type = 'NIFTI_GZ'
        swapdim_t1.run()

        #flipping to  neurological..............................'
        shutil.copy(afs_anatomical, out_dir)
        anatomical_swap2   = '%s/MP2RAGE_BRAIN_swapdim.nii.gz' %out_dir
        force_neurological = ['fslorient', '-forceneurological', '%s'%anatomical_swap2]
        subprocess.call(force_neurological)


        '============================================================================================'
        '                                     Registration                                           '
        '============================================================================================'

        if os.path.isfile(os.path.join(out_dir, 'MP2RAGE_BRAIN_2spm.nii')):
            print 'MP2RAGE_BRAIN to SPM affine already calculated....... moving on'
        else:
            print 'Running FSL2SPM affine registration..................'
            swapdim_t1     = os.path.join(out_dir, 'MP2RAGE_BRAIN_swapdim.nii.gz')
            freesurf_anat  = os.path.join(workspace_dir, subject, 'segmentation_freesurfer', 'freesurfer_T1_2spm.nii')

            #register freesurfer T1  to SPM space
            anat_flirt = fsl.FLIRT()
            anat_flirt.inputs.in_file         = swapdim_t1
            anat_flirt.inputs.reference       = freesurf_anat
            anat_flirt.inputs.output_type     = "NIFTI"
            anat_flirt.inputs.bins     		  = 256
            anat_flirt.inputs.cost            = 'mutualinfo'
            anat_flirt.inputs.interp 		  = 'nearestneighbour'
            anat_flirt.inputs.searchr_x       = [-90, 90]
            anat_flirt.inputs.searchr_y       = [-90, 90]
            anat_flirt.inputs.searchr_z       = [-90, 90]
            #anat_flirt.inputs.dof     		  = 6
            anat_flirt.inputs.out_file        = '%s/MP2RAGE_BRAIN_2spm.nii' %out_dir
            anat_flirt.inputs.out_matrix_file = '%s/MP2RAGE_BRAIN_2spm.mat' %out_dir
            anat_flirt.run()

        '============================================================================================'
        '                                     Segmentation                                           '
        '============================================================================================'
        # check if the file exists
        if os.path.isfile(os.path.join( os.path.join(workspace_dir, subject, 'segmentation_fslFAST', 'fslFAST_seg_2.nii.gz'))):
            print 'Brain already segmented......... moving on'

        else:

            # define destination directory for spm segmentation outputs
            try:
                os.makedirs(os.path.join(workspace_dir, subject, 'segmentation_fslFAST'))
            except OSError:
                out_dir  = str(os.path.join(workspace_dir, subject, 'segmentation_fslFAST'))
            out_dir  = str(os.path.join(workspace_dir, subject, 'segmentation_fslFAST'))

            # run FSL FAST  segmentation
            print '..... Running FSL FAST Segmentation '
            os.chdir(out_dir)
            seg                             = fsl.FAST()
            seg.inputs.in_files             = '%s/MP2RAGE_BRAIN_2spm.nii' %out_dir
            seg.inputs.out_basename         = 'fslFAST'
            seg.inputs.segments             = True
            seg.inputs.probability_maps     = True
            seg.run()

        print '========================================================================================'


'======================================================================================================================================'
'======================================================================================================================================'

if __name__ == "__main__":
    #segment_fslFAST(test_pop, afsdir_a, workspace_a)
    segment_fslFAST(population_a, afsdir_a, workspace_a)
    segment_fslFAST(population_b, afsdir_b, workspace_b)

