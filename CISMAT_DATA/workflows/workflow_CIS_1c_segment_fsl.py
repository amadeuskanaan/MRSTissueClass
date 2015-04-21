__author__ = 'kanaan' 'Feb_20_2015'

import os
import sys
import nipype.interfaces.fsl as fsl

#assert len(sys.argv)== 2
#subject_index=int(sys.argv[1])

'========================================================================================'

afs_dir        = '/xxx'
population_young_a = ['xxx']
workspace_a    = 'xxx'
'========================================================================================'

def segment_fslFAST(population, workspace_dir):
    count= 0
    #subject = population[subject_index]
    for subject in population:
        count +=1
        print '========================================================================================'
        print '%s- Runnning FSL FAST Segmentation on subject %s_%s' %(count, subject[0:10], workspace_dir[-1])
        print ''

        # define subject directory and anatomical file path
        subject_dir     = os.path.join(workspace_dir ,  subject[0:4])
        anatomical_dir  = os.path.join(subject_dir   , 'anatomical_original')
        anatomical_file = os.path.join(anatomical_dir, 'ANATOMICAL.nii')



        # check if the file exists
        if os.path.isfile(os.path.join( os.path.join(workspace_dir, subject[0:4], 'segmentation_fslFAST', 'fslFAST_seg_2.nii.gz'))):
            print 'Brain already segmented......... moving on'

        else:

            # define destination directory for spm segmentation outputs
            try:
                os.makedirs(os.path.join(workspace_dir, subject[0:4], 'segmentation_fslFAST'))
            except OSError:
                out_dir  = str(os.path.join(workspace_dir, subject[0:4], 'segmentation_fslFAST'))
            out_dir  = str(os.path.join(workspace_dir, subject[0:4], 'segmentation_fslFAST'))

            # running bet
            print '..... Running Brain Extraction'
            os.chdir(out_dir)
            btr                 = fsl.BET()
            btr.inputs.in_file  = anatomical_file
            btr.inputs.frac     = 0.7
            btr.run()

            # run FSL FAST  segmentation
            print '..... Running FSL FAST Segmentation '
            os.chdir(out_dir)
            seg                             = fsl.FAST()
            seg.inputs.in_files             = os.path.join(out_dir, 'ANATOMICAL_brain.nii.gz')
            seg.inputs.out_basename         = 'fslFAST'
            seg.inputs.segments             = True
            seg.inputs.probability_maps     = True
            seg.run()

            print '========================================================================================'


'======================================================================================================================================'
'======================================================================================================================================'

if __name__ == "__main__":
    #segment_fslFAST(test_popo, workspace_a)
    segment_fslFAST(population_young_a, workspace_a) # COMPLETE via condor_submit on 11-03-2015   ... av run time per brain = 12minutes
    segment_fslFAST(population_young_b, workspace_b) # COMPLETE via shell 16-03-2015
    segment_fslFAST(population_young_c, workspace_c) # COMPLETE via condor_submit on 11-03-2015

