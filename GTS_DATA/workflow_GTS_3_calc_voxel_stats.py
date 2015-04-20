__author__ = 'kanaan' '18.03.2015'


import os
import numpy as np
import nibabel as nb
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.fsl as fsl
# import nipype.pipeline.engine as pe
# import nipype.interfaces.io as nio

'========================================================================================'
workspace_a    = '/scr/sambesi2/workspace/project_MRSTissueClass/GTS/study_a'
workspace_b    = '/scr/sambesi2/workspace/project_MRSTissueClass/GTS/study_b'

test_pop       = ['SI5']
population_a   = [ 'BM8X', 'GF3T', 'GH4T', 'GSNT', 'HCTT', 'HM1X', 'HR8T', 'LMIT', 'MJBT', 'PAHT',
                   'RB1T', 'RJBT', 'RJJT', 'RMNT', 'SDCT', 'SI5T', 'SJBT', 'STQT', 'TJ5T', 'TR4T',
                   'TSCT', 'TV1T', 'ZT5T']
                  # no retest ---- >'KDET', 'NP4T', 'WJ3T',

population_b   = [ 'BM8X', 'GF3T', 'GH4T', 'GSNT', 'HCTT', 'HM1X', 'HR8T', 'LMIT', 'MJBT', 'PAHT',
                   'RB1T', 'RJBT', 'RJJT', 'RMNT', 'SDCT', 'SI5T', 'SJBT', 'STQT', 'TJ5T', 'TR4T',
                   'TSCT', 'TV1T', 'ZT5T', ]

'========================================================================================'


def calculate_voxel_statistics(population, workspace_dir):
        count = 0
        for subject in population:
            count +=1
            print '========================================================================================'
            print '%s-Calculating MRS voxel statistics for subject %s_%s ' %(count, subject, workspace_dir[-1])
            print ''

            freesurfer_dir     = os.path.join(workspace_dir, subject, 'segmentation_freesurfer')
            fslfast_dir        = os.path.join(workspace_dir, subject, 'segmentation_fslFAST')
            spm_dir            = os.path.join(workspace_dir, subject, 'segmentation_spm')

            #grab svs masks for three voxels
            acc_mask          = os.path.join(workspace_dir, subject, 'svs_voxel_mask', '%s%s_ACC_RDA_MASK.nii'%(subject,workspace_dir[-1]))
            tha_mask          = os.path.join(workspace_dir, subject, 'svs_voxel_mask', '%s%s_THA_RDA_MASK.nii'%(subject,workspace_dir[-1]))
            str_mask          = os.path.join(workspace_dir, subject, 'svs_voxel_mask', '%s%s_STR_RDA_MASK.nii'%(subject,workspace_dir[-1]))

            #grab tissues segments for the three algorithsm
            freesurfer_gm = os.path.join(freesurfer_dir, 'freesurfer_GM_mask.nii.gz')
            freesurfer_wm = os.path.join(freesurfer_dir, 'freesurfer_WM_mask.nii.gz')
            freesurfer_cm = os.path.join(freesurfer_dir, 'freesurfer_CSF_mask.nii.gz')

            fslfast_gm    = os.path.join(fslfast_dir, 'fslFAST_seg_1.nii.gz')
            fslfast_wm    = os.path.join(fslfast_dir, 'fslFAST_seg_2.nii.gz')
            fslfast_cm    = os.path.join(fslfast_dir, 'fslFAST_seg_0.nii.gz')

            spm_gm        = os.path.join(spm_dir, 'TISSUE_CLASS_1_GM_BINARY05.nii.gz')
            spm_wm        = os.path.join(spm_dir, 'TISSUE_CLASS_2_WM_BINARY05.nii.gz')
            spm_cm        = os.path.join(spm_dir, 'TISSUE_CLASS_3_CSF_BINARY05.nii.gz')


            '============================================================================================'
            '                     Calculating Tissue Proportions for ACC                                 '
            '============================================================================================'
            if not os.path.isfile(freesurfer_gm):
                print 'ValueError: freesurfer tissue masks not created, run workflow 1a and come back'
            elif not os.path.isfile(acc_mask):
                print 'IOError: [Errno 2] SVS mask Does not exist, run ''workflow_CIS_2_create_svs_mask.py'' and come back.'
            else:
                if os.path.isfile(os.path.join(workspace_dir, subject, 'svs_voxel_stats', 'ACC_voxel_statistics_freesurfer.txt')):
                    print 'Voxel statistics already calculated for freeseurfer... moving on'
                else:
                    try:
                        os.makedirs(os.path.join(workspace_dir, subject, 'svs_voxel_stats'))
                    except OSError:
                        stats_dir  = str(os.path.join(workspace_dir, subject, 'svs_voxel_stats'))
                    stats_dir  = str(os.path.join(workspace_dir, subject, 'svs_voxel_stats'))

                    print 'files available.... calculating.......'

                    # load mask data
                    fs_gm_data  = nb.load(freesurfer_gm).get_data().squeeze()
                    fs_wm_data  = nb.load(freesurfer_wm).get_data().squeeze()
                    fs_cm_data  = nb.load(freesurfer_cm).get_data().squeeze()
                    fsl_gm_data = nb.load(fslfast_gm).get_data().squeeze()
                    fsl_wm_data = nb.load(fslfast_wm).get_data().squeeze()
                    fsl_cm_data = nb.load(fslfast_cm).get_data().squeeze()
                    spm_gm_data = nb.load(spm_gm).get_data().squeeze()
                    spm_wm_data = nb.load(spm_wm).get_data().squeeze()
                    spm_cm_data = nb.load(spm_cm).get_data().squeeze()

                    acc_data    = nb.load(acc_mask).get_data().squeeze()

                    ########################################################
                    #multiply SVS ROI with segmented data for ACC
                    acc_vox_fs_gm  = acc_data * fs_gm_data
                    acc_vox_fs_wm  = acc_data * fs_wm_data
                    acc_vox_fs_cm  = acc_data * fs_cm_data
                    acc_vox_fsl_gm = acc_data * fsl_gm_data
                    acc_vox_fsl_wm = acc_data * fsl_wm_data
                    acc_vox_fsl_cm = acc_data * fsl_cm_data
                    acc_vox_spm_gm = acc_data * spm_gm_data
                    acc_vox_spm_wm = acc_data * spm_wm_data
                    acc_vox_spm_cm = acc_data * spm_cm_data

                    #extract stats from segmentation for acc
                    acc_vox_total_svs    = np.sum(acc_data)
                    acc_vox_total_fs_gm  = np.sum(acc_vox_fs_gm)
                    acc_vox_total_fs_wm  = np.sum(acc_vox_fs_wm)
                    acc_vox_total_fs_cm  = np.sum(acc_vox_fs_cm)
                    acc_vox_total_fsl_gm = np.sum(acc_vox_fsl_gm)
                    acc_vox_total_fsl_wm = np.sum(acc_vox_fsl_wm)
                    acc_vox_total_fsl_cm = np.sum(acc_vox_fsl_cm)
                    acc_vox_total_spm_gm = np.sum(acc_vox_spm_gm)
                    acc_vox_total_spm_wm = np.sum(acc_vox_spm_wm)
                    acc_vox_total_spm_cm = np.sum(acc_vox_spm_cm)

                    percent_svs           = float(acc_vox_total_svs)/ float(acc_vox_total_svs)
                    acc_percent_freesurfer_gm = np.round(float(acc_vox_total_fs_gm)/ float(acc_vox_total_svs), 3)
                    acc_percent_freesurfer_wm = np.round(float(acc_vox_total_fs_wm)/ float(acc_vox_total_svs), 3)
                    acc_percent_freesurfer_cm = np.round(float(acc_vox_total_fs_cm)/ float(acc_vox_total_svs), 3)
                    acc_percent_fslfast_gm    = np.round(float(acc_vox_total_fsl_gm)/float(acc_vox_total_svs), 3)
                    acc_percent_fslfast_wm    = np.round(float(acc_vox_total_fsl_wm)/float(acc_vox_total_svs), 3)
                    acc_percent_fslfast_cm    = np.round(float(acc_vox_total_fsl_cm)/float(acc_vox_total_svs), 3)
                    acc_percent_spm_gm        = np.round(float(acc_vox_total_spm_gm) / float(acc_vox_total_svs), 3)
                    acc_percent_spm_wm        = np.round(float(acc_vox_total_spm_wm) / float(acc_vox_total_svs), 3)
                    acc_percent_spm_cm        = np.round(float(acc_vox_total_spm_cm) / float(acc_vox_total_svs), 3)
                    acc_sum_fs   =  np.round(float(acc_percent_freesurfer_gm + acc_percent_freesurfer_wm + acc_percent_freesurfer_cm), 1)
                    acc_sum_fsl  =  np.round(float(acc_percent_fslfast_gm + acc_percent_fslfast_wm +  acc_percent_fslfast_cm), 1)
                    acc_sum_spm  =  np.round(float(acc_percent_spm_gm + acc_percent_spm_wm + acc_percent_spm_cm), 1)
                    print ''
                    print 'ACC Freesurfer Tissue Proportions     = %s%% GM, %s%% WM, %s%% CSF   = %s'  %(acc_percent_freesurfer_gm,acc_percent_freesurfer_wm, acc_percent_freesurfer_cm, acc_sum_fs)
                    print 'ACC FSL FAST Tissue Proportions       = %s%% GM, %s%% WM, %s%% CSF = %s ' %(acc_percent_fslfast_gm,acc_percent_fslfast_wm, acc_percent_fslfast_cm, acc_sum_fsl)
                    print 'ACC SPM NewSegment Tissue Proportions = %s%% GM, %s%% WM, %s%% CSF = %s'  %(acc_percent_spm_gm,acc_percent_spm_wm, acc_percent_spm_cm, acc_sum_spm)

                    acc_spm_txt  = os.path.join(stats_dir, 'ACC_voxel_statistics_spm.txt')
                    acc_fs_txt   = os.path.join(stats_dir, 'ACC_voxel_statistics_freesurfer.txt')
                    acc_fsl_txt  = os.path.join(stats_dir, 'ACC_voxel_statistics_fslfast.txt')

                    acc_write_spm = open(acc_spm_txt, 'w')
                    acc_write_spm.write('%s, %s, %s' %(acc_percent_spm_gm,acc_percent_spm_wm, acc_percent_spm_cm))
                    acc_write_spm.close()

                    acc_write_fs = open(acc_fs_txt, 'w')
                    acc_write_fs.write('%s, %s, %s'%(acc_percent_freesurfer_gm,acc_percent_freesurfer_wm, acc_percent_freesurfer_cm))
                    acc_write_fs.close()

                    write_fsl = open(acc_fsl_txt, 'w')
                    write_fsl.write('%s, %s, %s'%(acc_percent_fslfast_gm,acc_percent_fslfast_wm, acc_percent_fslfast_cm))
                    write_fsl.close()

            '============================================================================================'
            '                     Calculating Tissue Proportions for THA                                 '
            '============================================================================================'
            if not os.path.isfile(freesurfer_gm):
                print 'ValueError: freesurfer tissue masks not created, run workflow 1a and come back'
            elif not os.path.isfile(tha_mask):
                print 'IOError: [Errno 2] SVS mask Does not exist, run ''workflow_CIS_2_create_svs_mask.py'' and come back.'
            else:
                if os.path.isfile(os.path.join(workspace_dir, subject, 'svs_voxel_stats', 'tha_voxel_statistics_freesurfer.txt')):
                    print 'Voxel statistics already calculated for freeseurfer... moving on'
                else:
                    try:
                        os.makedirs(os.path.join(workspace_dir, subject, 'svs_voxel_stats'))
                    except OSError:
                        stats_dir  = str(os.path.join(workspace_dir, subject, 'svs_voxel_stats'))
                    stats_dir  = str(os.path.join(workspace_dir, subject, 'svs_voxel_stats'))

                    print 'files available.... calculating.......'

                    # load mask data
                    fs_gm_data  = nb.load(freesurfer_gm).get_data().squeeze()
                    fs_wm_data  = nb.load(freesurfer_wm).get_data().squeeze()
                    fs_cm_data  = nb.load(freesurfer_cm).get_data().squeeze()
                    fsl_gm_data = nb.load(fslfast_gm).get_data().squeeze()
                    fsl_wm_data = nb.load(fslfast_wm).get_data().squeeze()
                    fsl_cm_data = nb.load(fslfast_cm).get_data().squeeze()
                    spm_gm_data = nb.load(spm_gm).get_data().squeeze()
                    spm_wm_data = nb.load(spm_wm).get_data().squeeze()
                    spm_cm_data = nb.load(spm_cm).get_data().squeeze()

                    tha_data    = nb.load(tha_mask).get_data().squeeze()

                    ########################################################
                    #multiply SVS ROI with segmented data for ACC
                    tha_vox_fs_gm  = tha_data * fs_gm_data
                    tha_vox_fs_wm  = tha_data * fs_wm_data
                    tha_vox_fs_cm  = tha_data * fs_cm_data
                    tha_vox_fsl_gm = tha_data * fsl_gm_data
                    tha_vox_fsl_wm = tha_data * fsl_wm_data
                    tha_vox_fsl_cm = tha_data * fsl_cm_data
                    tha_vox_spm_gm = tha_data * spm_gm_data
                    tha_vox_spm_wm = tha_data * spm_wm_data
                    tha_vox_spm_cm = tha_data * spm_cm_data



                    #extract stats from segmentation for acc
                    tha_vox_total_svs    = np.sum(tha_data)
                    tha_vox_total_fs_gm  = np.sum(tha_vox_fs_gm)
                    tha_vox_total_fs_wm  = np.sum(tha_vox_fs_wm)
                    tha_vox_total_fs_cm  = np.sum(tha_vox_fs_cm)
                    tha_vox_total_fsl_gm = np.sum(tha_vox_fsl_gm)
                    tha_vox_total_fsl_wm = np.sum(tha_vox_fsl_wm)
                    tha_vox_total_fsl_cm = np.sum(tha_vox_fsl_cm)
                    tha_vox_total_spm_gm = np.sum(tha_vox_spm_gm)
                    tha_vox_total_spm_wm = np.sum(tha_vox_spm_wm)
                    tha_vox_total_spm_cm = np.sum(tha_vox_spm_cm)


                    percent_svs           = float(tha_vox_total_svs)/ float(tha_vox_total_svs)
                    tha_percent_freesurfer_gm = np.round(float(tha_vox_total_fs_gm)/ float(tha_vox_total_svs), 3)
                    tha_percent_freesurfer_wm = np.round(float(tha_vox_total_fs_wm)/ float(tha_vox_total_svs), 3)
                    tha_percent_freesurfer_cm = np.round(float(tha_vox_total_fs_cm)/ float(tha_vox_total_svs), 3)
                    tha_percent_fslfast_gm    = np.round(float(tha_vox_total_fsl_gm)/float(tha_vox_total_svs), 3)
                    tha_percent_fslfast_wm    = np.round(float(tha_vox_total_fsl_wm)/float(tha_vox_total_svs), 3)
                    tha_percent_fslfast_cm    = np.round(float(tha_vox_total_fsl_cm)/float(tha_vox_total_svs), 3)
                    tha_percent_spm_gm        = np.round(float(tha_vox_total_spm_gm) / float(tha_vox_total_svs), 3)
                    tha_percent_spm_wm        = np.round(float(tha_vox_total_spm_wm) / float(tha_vox_total_svs), 3)
                    tha_percent_spm_cm        = np.round(float(tha_vox_total_spm_cm) / float(tha_vox_total_svs), 3)
                    tha_sum_fs   =  np.round(float(tha_percent_freesurfer_gm + tha_percent_freesurfer_wm + tha_percent_freesurfer_cm), 1)
                    tha_sum_fsl  =  np.round(float(tha_percent_fslfast_gm + tha_percent_fslfast_wm +  tha_percent_fslfast_cm), 1)
                    tha_sum_spm  =  np.round(float(tha_percent_spm_gm + tha_percent_spm_wm + tha_percent_spm_cm), 1)
                    print ''
                    print 'THA Freesurfer Tissue Proportions     = %s%% GM, %s%% WM, %s%% CSF   = %s'  %(tha_percent_freesurfer_gm,tha_percent_freesurfer_wm, tha_percent_freesurfer_cm, tha_sum_fs)
                    print 'THA FSL FAST Tissue Proportions       = %s%% GM, %s%% WM, %s%% CSF = %s ' %(tha_percent_fslfast_gm,tha_percent_fslfast_wm, tha_percent_fslfast_cm, tha_sum_fsl)
                    print 'THA SPM NewSegment Tissue Proportions = %s%% GM, %s%% WM, %s%% CSF = %s'  %(tha_percent_spm_gm,tha_percent_spm_wm, tha_percent_spm_cm, tha_sum_spm)
                    tha_spm_txt  = os.path.join(stats_dir, 'tha_voxel_statistics_spm.txt')
                    tha_fs_txt   = os.path.join(stats_dir, 'tha_voxel_statistics_freesurfer.txt')
                    tha_fsl_txt  = os.path.join(stats_dir, 'tha_voxel_statistics_fslfast.txt')

                    tha_write_spm = open(tha_spm_txt, 'w')
                    tha_write_spm.write('%s, %s, %s' %(tha_percent_spm_gm,tha_percent_spm_wm, tha_percent_spm_cm))
                    tha_write_spm.close()

                    tha_write_fs = open(tha_fs_txt, 'w')
                    tha_write_fs.write('%s, %s, %s'%(tha_percent_freesurfer_gm,tha_percent_freesurfer_wm, tha_percent_freesurfer_cm))
                    tha_write_fs.close()

                    write_fsl = open(tha_fsl_txt, 'w')
                    write_fsl.write('%s, %s, %s'%(tha_percent_fslfast_gm,tha_percent_fslfast_wm, tha_percent_fslfast_cm))
                    write_fsl.close()

            '============================================================================================'
            '                     Calculating Tissue Proportions for STR                                 '
            '============================================================================================'
            if not os.path.isfile(freesurfer_gm):
                print 'ValueError: freesurfer tissue masks not created, run workflow 1a and come back'
            elif not os.path.isfile(str_mask):
                print 'IOError: [Errno 2] SVS mask Does not exist, run ''workflow_CIS_2_create_svs_mask.py'' and come back.'
            else:
                if os.path.isfile(os.path.join(workspace_dir,  subject, 'svs_voxel_stats', 'str_voxel_statistics_freesurfer.txt')):
                    print 'Voxel statistics already calculated for freeseurfer... moving on'
                else:
                    try:
                        os.makedirs(os.path.join(workspace_dir, subject, 'svs_voxel_stats'))
                    except OSError:
                        stats_dir  = str(os.path.join(workspace_dir, subject, 'svs_voxel_stats'))
                    stats_dir  = str(os.path.join(workspace_dir, subject, 'svs_voxel_stats'))

                    print 'files available.... calculating.......'

                    # load mask data
                    fs_gm_data  = nb.load(freesurfer_gm).get_data().squeeze()
                    fs_wm_data  = nb.load(freesurfer_wm).get_data().squeeze()
                    fs_cm_data  = nb.load(freesurfer_cm).get_data().squeeze()
                    fsl_gm_data = nb.load(fslfast_gm).get_data().squeeze()
                    fsl_wm_data = nb.load(fslfast_wm).get_data().squeeze()
                    fsl_cm_data = nb.load(fslfast_cm).get_data().squeeze()
                    spm_gm_data = nb.load(spm_gm).get_data().squeeze()
                    spm_wm_data = nb.load(spm_wm).get_data().squeeze()
                    spm_cm_data = nb.load(spm_cm).get_data().squeeze()

                    str_data    = nb.load(str_mask).get_data().squeeze()

                    ########################################################
                    #multiply SVS ROI with segmented data for ACC
                    str_vox_fs_gm  = str_data * fs_gm_data
                    str_vox_fs_wm  = str_data * fs_wm_data
                    str_vox_fs_cm  = str_data * fs_cm_data
                    str_vox_fsl_gm = str_data * fsl_gm_data
                    str_vox_fsl_wm = str_data * fsl_wm_data
                    str_vox_fsl_cm = str_data * fsl_cm_data
                    str_vox_spm_gm = str_data * spm_gm_data
                    str_vox_spm_wm = str_data * spm_wm_data
                    str_vox_spm_cm = str_data * spm_cm_data

                    #extract stats from segmentation for acc
                    str_vox_total_svs    = np.sum(str_data)
                    str_vox_total_fs_gm  = np.sum(str_vox_fs_gm)
                    str_vox_total_fs_wm  = np.sum(str_vox_fs_wm)
                    str_vox_total_fs_cm  = np.sum(str_vox_fs_cm)
                    str_vox_total_fsl_gm = np.sum(str_vox_fsl_gm)
                    str_vox_total_fsl_wm = np.sum(str_vox_fsl_wm)
                    str_vox_total_fsl_cm = np.sum(str_vox_fsl_cm)
                    str_vox_total_spm_gm = np.sum(str_vox_spm_gm)
                    str_vox_total_spm_wm = np.sum(str_vox_spm_wm)
                    str_vox_total_spm_cm = np.sum(str_vox_spm_cm)

                    percent_svs           = float(str_vox_total_svs)/ float(str_vox_total_svs)
                    str_percent_freesurfer_gm = np.round(float(str_vox_total_fs_gm)/ float(str_vox_total_svs), 3)
                    str_percent_freesurfer_wm = np.round(float(str_vox_total_fs_wm)/ float(str_vox_total_svs), 3)
                    str_percent_freesurfer_cm = np.round(float(str_vox_total_fs_cm)/ float(str_vox_total_svs), 3)
                    str_percent_fslfast_gm    = np.round(float(str_vox_total_fsl_gm)/float(str_vox_total_svs), 3)
                    str_percent_fslfast_wm    = np.round(float(str_vox_total_fsl_wm)/float(str_vox_total_svs), 3)
                    str_percent_fslfast_cm    = np.round(float(str_vox_total_fsl_cm)/float(str_vox_total_svs), 3)
                    str_percent_spm_gm        = np.round(float(str_vox_total_spm_gm) / float(str_vox_total_svs), 3)
                    str_percent_spm_wm        = np.round(float(str_vox_total_spm_wm) / float(str_vox_total_svs), 3)
                    str_percent_spm_cm        = np.round(float(str_vox_total_spm_cm) / float(str_vox_total_svs), 3)
                    str_sum_fs   =  np.round(float(str_percent_freesurfer_gm + str_percent_freesurfer_wm + str_percent_freesurfer_cm), 1)
                    str_sum_fsl  =  np.round(float(str_percent_fslfast_gm + str_percent_fslfast_wm +  str_percent_fslfast_cm), 1)
                    str_sum_spm  =  np.round(float(str_percent_spm_gm + str_percent_spm_wm + str_percent_spm_cm), 1)
                    print ''
                    print 'STR Freesurfer Tissue Proportions     = %s%% GM, %s%% WM, %s%% CSF   = %s'  %(str_percent_freesurfer_gm,str_percent_freesurfer_wm, str_percent_freesurfer_cm, str_sum_fs)
                    print 'STR FSL FAST Tissue Proportions       = %s%% GM, %s%% WM, %s%% CSF = %s ' %(str_percent_fslfast_gm,str_percent_fslfast_wm, str_percent_fslfast_cm, str_sum_fsl)
                    print 'STR SPM NewSegment Tissue Proportions = %s%% GM, %s%% WM, %s%% CSF = %s'  %(str_percent_spm_gm,str_percent_spm_wm, str_percent_spm_cm, str_sum_spm)

                    str_spm_txt  = os.path.join(stats_dir, 'str_voxel_statistics_spm.txt')
                    str_fs_txt   = os.path.join(stats_dir, 'str_voxel_statistics_freesurfer.txt')
                    str_fsl_txt  = os.path.join(stats_dir, 'str_voxel_statistics_fslfast.txt')

                    str_write_spm = open(str_spm_txt, 'w')
                    str_write_spm.write('%s, %s, %s' %(str_percent_spm_gm,str_percent_spm_wm, str_percent_spm_cm))
                    str_write_spm.close()

                    str_write_fs = open(str_fs_txt, 'w')
                    str_write_fs.write('%s, %s, %s'%(str_percent_freesurfer_gm,str_percent_freesurfer_wm, str_percent_freesurfer_cm))
                    str_write_fs.close()

                    write_fsl = open(str_fsl_txt, 'w')
                    write_fsl.write('%s, %s, %s'%(str_percent_fslfast_gm,str_percent_fslfast_wm, str_percent_fslfast_cm))
                    write_fsl.close()

'######################################################################################################################################'
'######################################################################################################################################'

if __name__ == "__main__":
    #calculate_voxel_statistics(test_pop, workspace_a)
    calculate_voxel_statistics(population_a, workspace_a)
    calculate_voxel_statistics(population_b, workspace_b)