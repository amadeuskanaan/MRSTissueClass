__author__ = 'kanaan' 'Feb_20_2015'

import os
import sys
import nipype.interfaces.fsl as fsl

#assert len(sys.argv)== 2
#subject_index=int(sys.argv[1])

'========================================================================================'

workspace_a    = '/scr/sambesi2/workspace/project_MRSTissueClass/CISMAT/study_a'
workspace_b    = '/scr/sambesi2/workspace/project_MRSTissueClass/CISMAT/study_b'
workspace_c    = '/scr/sambesi2/workspace/project_MRSTissueClass/CISMAT/study_c'

population_young_a = ['BB2T040407.TRIO', 'EK5T040407.TRIO', 'FM4T040330.TRIO', 'GA3T040405.TRIO', 'HS5T040712.TRIO','KM4T040427.TRIO',
                      'ME1T040628.TRIO', 'MH4T040407.TRIO', 'NC2T040405.TRIO', 'NT2T040407.TRIO', 'WM8T040420.TRIO','ZK1T040405.TRIO']

population_young_b = ['BB2T040628.TRIO', 'EK5T040706.TRIO', 'FM4T040712.TRIO', 'GA3T040629.TRIO', 'HS5T040810.TRIO', 'KM4T040719.TRIO',
                      'ME1T040712.TRIO', 'MH4T040628.TRIO', 'NC2T040712.TRIO', 'NT2T040628.TRIO', 'WM8T040706.TRIO', 'ZK1T040628.TRIO']

population_young_c = ['BB2T040719.TRIO', 'EK5T040719.TRIO', 'FM4T040727.TRIO', 'GA3T040907.TRIO', 'HS5T040901.TRIO','ME1T040803.TRIO',
                                         'MH4T040719.TRIO', 'NC2T040810.TRIO', 'NT2T040712.TRIO', 'WM8T040719.TRIO', 'ZK1T040713.TRIO']
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

