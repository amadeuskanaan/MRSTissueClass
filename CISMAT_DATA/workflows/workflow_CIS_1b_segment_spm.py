__author__ = 'kanaan' 'Feb_20_2015'

import os
import nipype.interfaces.spm as spm
import shutil
import nipype.interfaces.fsl as fsl


afs_dir        = '/xxx'
population_young_a = ['xxx']
workspace_a    = 'xxx'



def segment_spm(population, workspace_dir):
    count= 0
    for subject in population:
        count +=1
        print '========================================================================================'
        print '%s- Runnning SPM12 NewSegment on subject %s' %(count, subject[0:10])
        print ''

        # define subject directory and anatomical file path
        subject_dir     = os.path.join(workspace_dir ,  subject[0:4])
        anatomical_dir  = os.path.join(subject_dir   , 'anatomical_original')
        anatomical_file = os.path.join(anatomical_dir, 'ANATOMICAL.nii')

        # check if the file exists
        if os.path.isfile(os.path.join( os.path.join(workspace_dir, subject[0:4], 'segmentation_spm', 'TISSUE_CLASS_1_GM.nii'))):
            print 'Brain already segmented......... moving on '

        else:
            print '..... Segmenting Brain with SPM12-NewSegment'

            # define destination directory for spm segmentation outputs
            try:
                os.makedirs(os.path.join(workspace_dir, subject[0:4], 'segmentation_spm'))
            except OSError:
                out_spm_dir  = str(os.path.join(workspace_dir, subject[0:4], 'segmentation_spm'))
            out_spm_dir  = str(os.path.join(workspace_dir, subject[0:4], 'segmentation_spm'))
            out_spm_dir  = str(os.path.join(workspace_dir, subject[0:4], 'segmentation_spm'))

            # run SPM segmentation
            print '..... Starting matlab no splash to run segmentation'
            seg                      = spm.NewSegment()
            seg.inputs.channel_files = anatomical_file
            seg.inputs.channel_info  = (0.0001, 60, (True, True))
            seg.out_dir              = out_spm_dir
            seg.run()


            # rename output files
            print '..... Renaming outputs and dumping into SPM segmenation dir'

            for file in os.listdir(anatomical_dir):
                if 'c1' in file:
                    shutil.move(str(os.path.join(anatomical_dir, file)),
                                str(os.path.join(out_spm_dir, 'TISSUE_CLASS_1_GM.nii')))
                elif 'c2' in file:
                    shutil.move(str(os.path.join(anatomical_dir, file)),
                                str(os.path.join(out_spm_dir, 'TISSUE_CLASS_2_WM.nii')))
                elif 'c3' in file:
                    shutil.move(str(os.path.join(anatomical_dir, file)),
                                str(os.path.join(out_spm_dir, 'TISSUE_CLASS_3_CSF.nii')))
                elif 'c4' in file:
                    shutil.move(str(os.path.join(anatomical_dir, file)),
                                str(os.path.join(out_spm_dir, '___Skull.nii')))
                elif 'c5' in file:
                    shutil.move(str(os.path.join(anatomical_dir, file)),
                                str(os.path.join(out_spm_dir, '___SoftTissue.nii')))
                elif 'BiasField' in file:
                    shutil.move(str(os.path.join(anatomical_dir, file)),
                                str(os.path.join(out_spm_dir, '___BiasFieldMap.nii')))
                elif 'mANATOMICAL' in file:
                    shutil.move(str(os.path.join(anatomical_dir, file)),
                                str(os.path.join(out_spm_dir, '___mFile.nii')))
                elif 'ANATOMICAL_seg8' in file:
                    shutil.move(str(os.path.join(anatomical_dir, file)),
                                str(os.path.join(out_spm_dir, '___seg8.mat')))


        # threshold and biniarize spm tissue masks
        out_spm_dir  = str(os.path.join(workspace_dir, subject[0:4], 'segmentation_spm'))
        gm_mask  = str(os.path.join(out_spm_dir, 'TISSUE_CLASS_1_GM.nii'))
        wm_mask  = str(os.path.join(out_spm_dir, 'TISSUE_CLASS_2_WM.nii'))
        csf_mask = str(os.path.join(out_spm_dir, 'TISSUE_CLASS_3_CSF.nii'))

        if os.path.isfile(os.path.join( os.path.join(workspace_dir, subject[0:4], 'segmentation_spm', 'TISSUE_CLASS_1_GM_BINARY05.nii.gz'))):
            print 'Tissues already binned.......... moving on '
        else:
            print '..... Thresholding and binazing tissue probablity maps '


            '###########################################'
            '##################  GM  ###################'
            thr_hbin_GM1                          = fsl.Threshold()
            thr_hbin_GM1.inputs.in_file           = gm_mask
            thr_hbin_GM1.inputs.thresh            =   0.5
            thr_hbin_GM1.inputs.args              = '-bin'
            thr_hbin_GM1.inputs.ignore_exception  = True
            thr_hbin_GM1.inputs.out_file          = str(os.path.join(out_spm_dir, 'TISSUE_CLASS_1_GM_BINARY05.nii.gz'))
            thr_hbin_GM1.run()

            thr_hbin_GM2                          = fsl.Threshold()
            thr_hbin_GM2.inputs.in_file           = gm_mask
            thr_hbin_GM2.inputs.thresh            = 0.7
            thr_hbin_GM2.inputs.args              = '-bin'
            thr_hbin_GM2.inputs.ignore_exception  = True
            thr_hbin_GM2.inputs.out_file          = str(os.path.join(out_spm_dir, 'TISSUE_CLASS_1_GM_BINARY07.nii.gz'))
            thr_hbin_GM2.run()

            '###########################################'
            '##################  WM  ###################'

            thr_hbin_WM1                          = fsl.Threshold()
            thr_hbin_WM1.inputs.in_file           = wm_mask
            thr_hbin_WM1.inputs.thresh            = 0.5
            thr_hbin_WM1.inputs.args              = '-bin'
            thr_hbin_WM1.inputs.ignore_exception  = True
            thr_hbin_WM1.inputs.out_file          = str(os.path.join(out_spm_dir, 'TISSUE_CLASS_2_WM_BINARY05.nii.gz'))
            thr_hbin_WM1.run()


            thr_hbin_WM2                          = fsl.Threshold()
            thr_hbin_WM2.inputs.in_file           = wm_mask
            thr_hbin_WM2.inputs.thresh            = 0.9
            thr_hbin_WM2.inputs.args              = '-bin'
            thr_hbin_WM2.inputs.ignore_exception  = True
            thr_hbin_WM2.inputs.out_file          = str(os.path.join(out_spm_dir, 'TISSUE_CLASS_2_WM_BINARY09.nii.gz'))
            thr_hbin_WM2.run()

            '###########################################'
            '##################  CSF  ###################'

            thr_hbin_CSF1                         = fsl.Threshold()
            thr_hbin_CSF1.inputs.in_file          = csf_mask
            thr_hbin_CSF1.inputs.thresh           = 0.5
            thr_hbin_CSF1.inputs.args             = '-bin'
            thr_hbin_CSF1.inputs.ignore_exception = True
            thr_hbin_CSF1.inputs.out_file         = str(os.path.join(out_spm_dir, 'TISSUE_CLASS_3_CSF_BINARY05.nii.gz'))
            thr_hbin_CSF1.run()

            thr_hbin_CSF2                         = fsl.Threshold()
            thr_hbin_CSF2.inputs.in_file          = csf_mask
            thr_hbin_CSF2.inputs.thresh           = 0.9
            thr_hbin_CSF2.inputs.args             = '-bin'
            thr_hbin_CSF2.inputs.ignore_exception = True
            thr_hbin_CSF2.inputs.out_file         = str(os.path.join(out_spm_dir, 'TISSUE_CLASS_3_CSF_BINARY09.nii.gz'))
            thr_hbin_CSF2.run()

            print '========================================================================================'


'======================================================================================================================================'
'======================================================================================================================================'

#if __name__ == "__main__":
    #segment_spm(test_popo, workspace_a)
    #segment_spm(population_young_a, workspace_a)  # complete 11.03.2015
    #segment_spm(population_young_b, workspace_b)  # complete 11.03.2015
    #segment_spm(population_young_c, workspace_c)  # complete 11.03.2015
