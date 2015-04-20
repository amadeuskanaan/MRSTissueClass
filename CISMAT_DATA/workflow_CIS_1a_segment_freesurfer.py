__author__ = 'kanaan 25.02.2015'

import os
import sys
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.fsl as fsl
import nibabel as nb
import numpy as np

#assert len(sys.argv)== 2
#subject_index=int(sys.argv[1])

'========================================================================================'
gm_labels        = [3,8,42,17,18,53,54,11,12,13,26,50,51,52,58,9,10,47,48,49,16,28,60]
wm_labels        = [2,7,41,46]
csf_labels       = [4,5,14,15,24,31, 43,44,63, 72]
'========================================================================================'

'##################             ALL Young COMPLETE on March 5 2015     ##################'
test_pop       = ['BB2T040407.TRIO']
freesurfer_dir = '/scr/sambesi2/workspace/project_MRSTissueClass/CISMAT/FS_SUBJECTS'
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
'========================================================================================'
'========================================================================================'



def freesurfer_reconall(population, workspace_dir, freesurferdir):

	#subject = population[subject_index]
	count= 0
	for subject in population:
		count +=1
		print '========================================================================================'
		print '%s- Runnning FREESURFER reconall on subject %s' %(count, subject)

		subject_dir     = os.path.join(workspace_dir ,  subject[0:4])
		anatomical_dir  = os.path.join(subject_dir   , 'anatomical_original')
		anatomical_file = os.path.join(anatomical_dir, 'ANATOMICAL.nii')


		# check if the file exists
		if os.path.isfile(anatomical_file):
			print '..'
			if os.path.isfile(os.path.join(freesurfer_dir, subject[0:10], 'mri', 'aseg.mgz')):
				print 'Brain already segmented .......................... moving on'
				#print 'check data here ---> %s' %(os.path.join(freesurfer_dir, subject))
			else:
				#set freesurfer dir
				fs.FSCommand.set_default_subjects_dir(freesurferdir)
				seg_dir=freesurferdir+'/'+subject[0:10]+'/'
				print('saving outputs to ' + seg_dir)

				#run freesurfer segmentation

				reconall = fs.ReconAll()
				reconall.inputs.subject_id    = subject[0:10]
				reconall.inputs.directive     = 'all'
				reconall.inputs.T1_files      = anatomical_file
				reconall.inputs.subjects_dir  = freesurferdir
				reconall.run()
		else:
			print 'anatomical file for subject %s not found' %subject



		'============================================================================================'
		'                           Convert Freesurfer MGZs to Nifti'
		'============================================================================================'

		seg_dir     = os.path.join(freesurfer_dir, subject[0:10])
		t1_mgz      = os.path.join(seg_dir, 'mri', 'T1.mgz')    # T1 image in freesurfer orientation
		aseg_mgz    = os.path.join(seg_dir, 'mri', 'aseg.mgz')  # freesurfer segmentation file

		if os.path.isfile(os.path.join(workspace_dir, subject[0:4], 'segmentation_freesurfer', 'aseg.nii')):
			print 'MGZs already converted to NIFTI .................. moving on'
		else:
			print 'converting Freesurfer MGZ files to NIFTI......'

			try:
				os.makedirs(os.path.join(workspace_dir, subject[0:4], 'segmentation_freesurfer'))
			except OSError:
				out_fs_dir  = str(os.path.join(workspace_dir, subject[0:4], 'segmentation_freesurfer'))
			out_fs_dir  = str(os.path.join(workspace_dir, subject[0:4], 'segmentation_freesurfer'))

			#convert T1 to nifti
			anat2nii = fs.MRIConvert()
			anat2nii.inputs.in_file  = t1_mgz
			anat2nii.inputs.out_file = '%s/T1.nii' %out_fs_dir
			anat2nii.inputs.out_type = 'nii'
			anat2nii.run()
			#convert seg to nifti
			seg2nii = fs.MRIConvert()
			seg2nii.inputs.in_file  = aseg_mgz
			seg2nii.inputs.out_file = '%s/aseg.nii' %out_fs_dir
			seg2nii.inputs.out_type = 'nii'
			seg2nii.run()

		'============================================================================================'
		'                                     Registration                                           '
		'============================================================================================'

		out_fs_dir  = str(os.path.join(workspace_dir, subject[0:4], 'segmentation_freesurfer'))

		if os.path.isfile(os.path.join(out_fs_dir, 'freesurfer_aseg_2spm.nii.gz')):
			print 'Freesurfer to SPM affine already calculated....... moving on'
		else:
			print 'reorienting freesurfer files (T1 & aseg) to SPM space ..........'
			anat_spm       = os.path.join(workspace_dir, subject[0:4], 'anatomical_original', 'ANATOMICAL.nii')
			fs_t1_nii      = os.path.join(out_fs_dir, 'T1.nii')
			fs_aseg_nii    = os.path.join(out_fs_dir, 'aseg.nii')

			#register freesurfer T1  to SPM space
			anat_flirt = fsl.FLIRT()
			anat_flirt.inputs.in_file         = fs_t1_nii
			anat_flirt.inputs.reference       = anat_spm
			anat_flirt.inputs.output_type     = "NIFTI"
			anat_flirt.inputs.searchr_x       = [-180, 180]
			anat_flirt.inputs.searchr_y       = [-180, 180]
			anat_flirt.inputs.searchr_z       = [-180, 180]
			anat_flirt.inputs.cost_func       = 'mutualinfo'
			anat_flirt.inputs.out_file        = '%s/freesurfer_T1_2spm.nii' %out_fs_dir
			anat_flirt.inputs.out_matrix_file = '%s/freesurfer_T1_2spm_xfm.mat' %out_fs_dir
			anat_flirt.run()

			# Apply fs2spm xfm to aseg file
			fs2spm_xfm = '%s/freesurfer_T1_2spm_xfm.mat' %out_fs_dir

			aseg_applyxfm = fsl.ApplyXfm()
			aseg_applyxfm.inputs.in_file         = fs_aseg_nii
			aseg_applyxfm.inputs.reference       = anat_spm
			aseg_applyxfm.inputs.in_matrix_file  = fs2spm_xfm
			aseg_applyxfm.inputs.apply_xfm       = True
			aseg_applyxfm.inputs.out_file        = '%s/freesurfer_aseg_2spm.nii.gz' %out_fs_dir
			aseg_applyxfm.run()
		'============================================================================================'
		'                                     Create Tissue Masks                                    '
		'============================================================================================'
		out_fs_dir  = str(os.path.join(workspace_dir, subject[0:4], 'segmentation_freesurfer'))

		if os.path.isfile(os.path.join(out_fs_dir, 'freesurfer_GM_mask.nii.gz')):
			print 'Tissues already extracted as nifti files.......... moving on'

		else:
			print '...'
			print 'Extracting Tissue classes from Labels and saving as a nifti file'
			aseg 		= str(os.path.join(workspace_dir, subject[0:4], 'segmentation_freesurfer','freesurfer_aseg_2spm.nii.gz'))
			aseg_data   = nb.load(aseg).get_data()
			aseg_affine = nb.load(aseg).get_affine()

			wm_data      = np.zeros(aseg_data.shape)
			gm_data      = np.zeros(aseg_data.shape)
			csf_data     = np.zeros(aseg_data.shape)

			for data, labels in zip([wm_data, gm_data, csf_data], [wm_labels, gm_labels, csf_labels]):
				for label in labels:
					data[np.where(aseg_data==label)] =1
			wm_img   = nb.Nifti1Image(wm_data   , aseg_affine)
			gm_img   = nb.Nifti1Image(gm_data   , aseg_affine)
			csf_img  = nb.Nifti1Image(csf_data  , aseg_affine)

			nb.save(wm_img   , '%s/freesurfer_WM_mask.nii.gz'  %out_fs_dir)
			nb.save(gm_img   , '%s/freesurfer_GM_mask.nii.gz'  %out_fs_dir)
			nb.save(csf_img  , '%s/freesurfer_CSF_mask.nii.gz' %out_fs_dir)

'######################################################################################################################################'
'######################################################################################################################################'

if __name__ == "__main__":

	freesurfer_reconall(population_young_a, workspace_a, freesurfer_dir)  # run on 2015-03-10 at 13.35... complete
	freesurfer_reconall(population_young_b, workspace_b, freesurfer_dir)  # run on 2015-03-10 at 14.22... complete
	freesurfer_reconall(population_young_c, workspace_c, freesurfer_dir)  # run on 2015-03-10 at 13:13... complete
