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
                      'ME1T04Kan0628.TRIO', 'MH4T040407.TRIO', 'NC2T040405.TRIO', 'NT2T040407.TRIO', 'WM8T040420.TRIO','ZK1T040405.TRIO']
population_young_b = ['BB2T040628.TRIO', 'EK5T040706.TRIO', 'FM4T040712.TRIO',                    'HS5T040810.TRIO', 'KM4T040719.TRIO', # 'GA3T040629.TRIO' no rda
                      'ME1T040712.TRIO', 'MH4T040628.TRIO', 'NC2T040712.TRIO', 'NT2T040628.TRIO', 'WM8T040706.TRIO', 'ZK1T040628.TRIO']
population_young_c = ['BB2T040719.TRIO', 'EK5T040719.TRIO', 'FM4T040727.TRIO', 'GA3T040907.TRIO', 'HS5T040901.TRIO','ME1T040803.TRIO',
                                         'MH4T040719.TRIO', 'NC2T040810.TRIO', 'NT2T040712.TRIO', 'WM8T040719.TRIO', 'ZK1T040713.TRIO']



def calculate_voxel_statistics(population, workspace_dir):
        for subject in population:
            print '========================================================================================'
            print 'Calculating MRS voxel statistics for subject %s ' %subject[0:10]
            print ''

            freesurfer_dir     = os.path.join(workspace_dir, subject[0:4], 'segmentation_freesurfer')
            fslfast_dir        = os.path.join(workspace_dir, subject[0:4], 'segmentation_fslFAST')
            spm_dir            = os.path.join(workspace_dir, subject[0:4], 'segmentation_spm')

            svs_mask          = os.path.join(workspace_dir, subject[0:4], 'svs_voxel_mask', '%s_RDA_MASK.nii'%subject[0:10])


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
            '                     Calculating Tissue Proportions for Freesurfer and SPM '
            '============================================================================================'
            if not os.path.isfile(freesurfer_gm):
                print 'ValueError: freesurfer tissue masks not created, run workflow 1a and come back'
            elif not os.path.isfile(svs_mask):
                print 'IOError: [Errno 2] SVS mask Does not exist, run ''workflow_CIS_2_create_svs_mask.py'' and come back.'
            else:
                if os.path.isfile(os.path.join(workspace_dir, 'svs_voxel_stats', 'voxel_statistics_freesurfer.txt')):
                    print 'Voxel statistics already calculated for freeseurfer... moving on'
                else:
                    try:
                        os.makedirs(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_stats'))
                    except OSError:
                        stats_dir  = str(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_stats'))
                    stats_dir  = str(os.path.join(workspace_dir, subject[0:4], 'svs_voxel_stats'))

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
                    svs_data    = nb.load(svs_mask).get_data().squeeze()

                    #multiply SVS ROI with segmented data
                    vox_fs_gm  = svs_data * fs_gm_data
                    vox_fs_wm  = svs_data * fs_wm_data
                    vox_fs_cm  = svs_data * fs_cm_data
                    vox_fsl_gm = svs_data * fsl_gm_data
                    vox_fsl_wm = svs_data * fsl_wm_data
                    vox_fsl_cm = svs_data * fsl_cm_data
                    vox_spm_gm = svs_data * spm_gm_data
                    vox_spm_wm = svs_data * spm_wm_data
                    vox_spm_cm = svs_data * spm_cm_data

                    #extract stats from segmentation
                    vox_total_svs    = np.sum(svs_data)
                    vox_total_fs_gm  = np.sum(vox_fs_gm)
                    vox_total_fs_wm  = np.sum(vox_fs_wm)
                    vox_total_fs_cm  = np.sum(vox_fs_cm)
                    vox_total_fsl_gm = np.sum(vox_fsl_gm)
                    vox_total_fsl_wm = np.sum(vox_fsl_wm)
                    vox_total_fsl_cm = np.sum(vox_fsl_cm)
                    vox_total_spm_gm = np.sum(vox_spm_gm)
                    vox_total_spm_wm = np.sum(vox_spm_wm)
                    vox_total_spm_cm = np.sum(vox_spm_cm)

                    percent_svs           = float(vox_total_svs)/ float(vox_total_svs)
                    percent_freesurfer_gm = np.round(float(vox_total_fs_gm)/ float(vox_total_svs), 3)
                    percent_freesurfer_wm = np.round(float(vox_total_fs_wm)/ float(vox_total_svs), 3)
                    percent_freesurfer_cm = np.round(float(vox_total_fs_cm)/ float(vox_total_svs), 3)
                    percent_fslfast_gm    = np.round(float(vox_total_fsl_gm)/float(vox_total_svs), 3)
                    percent_fslfast_wm    = np.round(float(vox_total_fsl_wm)/float(vox_total_svs), 3)
                    percent_fslfast_cm    = np.round(float(vox_total_fsl_cm)/float(vox_total_svs), 3)
                    percent_spm_gm        = np.round(float(vox_total_spm_gm) / float(vox_total_svs), 3)
                    percent_spm_wm        = np.round(float(vox_total_spm_wm) / float(vox_total_svs), 3)
                    percent_spm_cm        = np.round(float(vox_total_spm_cm) / float(vox_total_svs), 3)
                    sum_fs   =  np.round(float(percent_freesurfer_gm + percent_freesurfer_wm + percent_freesurfer_cm), 1)
                    sum_fsl  =  np.round(float(percent_fslfast_gm + percent_fslfast_wm +  percent_fslfast_cm), 1)
                    sum_spm  =  np.round(float(percent_spm_gm + percent_spm_wm + percent_spm_cm), 1)
                    print ''
                    print 'Freesurfer Tissue Proportions     = %s%% GM, %s%% WM, %s%% CSF   = %s'  %(percent_freesurfer_gm,percent_freesurfer_wm, percent_freesurfer_cm, sum_fs)
                    print 'FSL FAST Tissue Proportions       = %s%% GM, %s%% WM, %s%% CSF = %s ' %(percent_fslfast_gm,percent_fslfast_wm, percent_fslfast_cm, sum_fsl)
                    print 'SPM NewSegment Tissue Proportions = %s%% GM, %s%% WM, %s%% CSF = %s'  %(percent_spm_gm,percent_spm_wm, percent_spm_cm, sum_spm)

                    spm_txt  = os.path.join(stats_dir, 'voxel_statistics_spm.txt')
                    fs_txt   = os.path.join(stats_dir, 'voxel_statistics_freesurfer.txt')
                    fsl_txt  = os.path.join(stats_dir, 'voxel_statistics_fslfast.txt')

                    write_spm = open(spm_txt, 'w')
                    write_spm.write('%s, %s, %s' %(percent_spm_gm,percent_spm_wm, percent_spm_cm))
                    write_spm.close()

                    write_fs = open(fs_txt, 'w')
                    write_fs.write('%s, %s, %s'%(percent_freesurfer_gm,percent_freesurfer_wm, percent_freesurfer_cm))
                    write_fs.close()

                    write_fsl = open(fsl_txt, 'w')
                    write_fsl.write('%s, %s, %s'%(percent_fslfast_gm,percent_fslfast_wm, percent_fslfast_cm))
                    write_fsl.close()

'######################################################################################################################################'
'######################################################################################################################################'

if __name__ == "__main__":
    calculate_voxel_statistics(population_young_a, workspace_a)
    calculate_voxel_statistics(population_young_b, workspace_b)
    calculate_voxel_statistics(population_young_c, workspace_c)