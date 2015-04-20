__author__ = 'kanaan' 'March_11_2015'

import os
import nipype.interfaces.spm as spm
import shutil
import nipype.interfaces.fsl as fsl
import sys
import nipype.interfaces.freesurfer as fs
import nibabel as nb
import numpy as np

# assert len(sys.argv)== 2
# subject_index=int(sys.argv[1])

'========================================================================================'

workspace_a    = '/scr/sambesi2/workspace/project_MRSTissueClass/GTS/study_a'
workspace_b    = '/scr/sambesi2/workspace/project_MRSTissueClass/GTS/study_b'

freesurfer_a   = '/scr/sambesi2/workspace/FS_SUBJECTS/Tourette_a/'
freesurfer_b   = '/scr/sambesi2/workspace/FS_SUBJECTS/Tourette_b/'
pop_test       = ['BM8X']
population_a   = [ 'BM8X', 'GF3T', 'GH4T', 'GSNT', 'HCTT', 'HM1X', 'HR8T', 'LMIT', 'MJBT', 'PAHT',
                   'RB1T', 'RJBT', 'RJJT', 'RMNT', 'SDCT', 'SI5T', 'SJBT', 'STQT', 'TJ5T', 'TR4T',
                   'TSCT', 'TV1T', 'ZT5T']
                  # no retest ---- >'KDET', 'NP4T', 'WJ3T',

population_b   = [ 'BM8X', 'GF3T', 'GH4T', 'GSNT', 'HCTT', 'HM1X', 'HR8T', 'LMIT', 'MJBT', 'PAHT',
                   'RB1T', 'RJBT', 'RJJT', 'RMNT', 'SDCT', 'SI5T', 'SJBT', 'STQT', 'TJ5T', 'TR4T',
                   'TSCT', 'TV1T', 'ZT5T', ]
				  # TJ5T has a bug ...too much sholder contrast in image... fix him....

gm_labels        = [3,8,42,17,18,53,54,11,12,13,26,50,51,52,58,9,10,47,48,49,16,28,60]
wm_labels        = [2,7,41,46]
csf_labels       = [4,5,14,15,24,31, 43,44,63, 72]
'========================================================================================'

def freesufer_create_tissues(population, workspace_dir, freesurfer_dir):

	#1. get aseg files
	#2. convert asegs to niftis
	#3. swaps dims to SPM orientation
	#4. register freesurfer files to spm space
	#5. create tissue masks from labels

	#subject = population[subject_index]
	count= 0
	for subject in population:
		count +=1
		print '========================================================================================'
		print '%s- Grabbing FREESURFER reconall for subject %s_%s' %(count, subject, workspace_dir[-1])

		subject_dir     = os.path.join(workspace_dir ,  subject)
		anatomical_dir  = os.path.join(subject_dir   , 'anatomical_original')
		anatomical_file = os.path.join(anatomical_dir, 'ANATOMICAL.nii')

		# check if the file exists
		if os.path.isfile(anatomical_file):
			print '..'
			if os.path.isfile(os.path.join(freesurfer_dir, subject, 'mri', 'aseg.mgz')):
				print 'Brain already segmented .......................... moving on'
				#print 'check data here ---> %s' %(os.path.join(freesurfer_dir, subject))
			else:
				print 'Run reconall for GTS_control_%s and then come back to me' %subject
		else:
			print 'anatomical file for subject %s not found' %subject



		'============================================================================================'
		'                           Convert Freesurfer MGZs to Nifti'
		'============================================================================================'

		seg_dir     = os.path.join(freesurfer_dir, subject)
		t1_mgz      = os.path.join(seg_dir, 'mri', 'T1.mgz')    # T1 image in freesurfer orientation
		aseg_mgz    = os.path.join(seg_dir, 'mri', 'aseg.mgz')  # freesurfer segmentation file

		if os.path.isfile(os.path.join(workspace_dir, subject, 'segmentation_freesurfer', 'aseg.nii')):
			print 'MGZs already converted to NIFTI .................. moving on'
		else:
			print 'converting Freesurfer MGZ files to NIFTI......'

			try:
				os.makedirs(os.path.join(workspace_dir, subject, 'segmentation_freesurfer'))
			except OSError:
				out_fs_dir  = str(os.path.join(workspace_dir, subject, 'segmentation_freesurfer'))
			out_fs_dir  = str(os.path.join(workspace_dir, subject, 'segmentation_freesurfer'))

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
		'                           SWAP dims to SPM orientation -- AP IS LR -- 					 '
		'============================================================================================'
		out_fs_dir  = str(os.path.join(workspace_dir, subject, 'segmentation_freesurfer'))

		if os.path.isfile(os.path.join(out_fs_dir, 'aseg_swapdim.nii.gz')):
			print 'Dimensions already swapped ....................... moving on'
		else:
			print 'Swapping dimensions of freesurfer files to AIL'
			fs_t1_nii      = os.path.join(out_fs_dir, 'T1.nii')
			fs_aseg_nii    = os.path.join(out_fs_dir, 'aseg.nii')

			swapdim_t1 = fsl.SwapDimensions()
			swapdim_t1.inputs.in_file     = fs_t1_nii
			swapdim_t1.inputs.new_dims    = ('AP', 'IS', 'LR')
			swapdim_t1.inputs.out_file    = '%s/T1_swapdim.nii.gz' %out_fs_dir
			swapdim_t1.inputs.output_type = 'NIFTI_GZ'
			swapdim_t1.run()

			swapdim_aseg = fsl.SwapDimensions()
			swapdim_aseg.inputs.in_file     = fs_aseg_nii
			swapdim_aseg.inputs.new_dims    = ('AP', 'IS', 'LR')
			swapdim_aseg.inputs.out_file    = '%s/aseg_swapdim.nii.gz' %out_fs_dir
			swapdim_aseg.inputs.output_type = 'NIFTI_GZ'
			swapdim_aseg.run()

		'============================================================================================'
		'                                     Registration                                           '
		'============================================================================================'



		if os.path.isfile(os.path.join(out_fs_dir, 'freesurfer_aseg_2spm.nii.gz')):
			print 'Freesurfer to SPM affine already calculated....... moving on'
		else:
			print 'Registring freesurfer affines to SPM space ..........'
			anat_spm       = os.path.join(workspace_dir, subject, 'anatomical_original', 'ANATOMICAL.nii')
			fs_t1_swapdim      = os.path.join(out_fs_dir, 'T1_swapdim.nii.gz')
			fs_aseg_swapdim    = os.path.join(out_fs_dir, 'aseg_swapdim.nii.gz')

			#register freesurfer T1  to SPM space
			anat_flirt = fsl.FLIRT()
			anat_flirt.inputs.in_file         = fs_t1_swapdim
			anat_flirt.inputs.reference       = anat_spm
			anat_flirt.inputs.output_type     = "NIFTI"
			anat_flirt.inputs.bins     		  = 256
			anat_flirt.inputs.cost            = 'mutualinfo'
			anat_flirt.inputs.searchr_x       = [-90, 90]
			anat_flirt.inputs.searchr_y       = [-90, 90]
			anat_flirt.inputs.searchr_z       = [-90, 90]
			#anat_flirt.inputs.dof     		  = 6
			anat_flirt.inputs.interp 		  = 'nearestneighbour'
			anat_flirt.inputs.out_file        = '%s/freesurfer_T1_2spm.nii' %out_fs_dir
			anat_flirt.inputs.out_matrix_file = '%s/freesurfer_T1_2spm_xfm.mat' %out_fs_dir
			anat_flirt.run()

			# Apply fs2spm xfm to aseg file
			fs2spm_xfm = '%s/freesurfer_T1_2spm_xfm.mat' %out_fs_dir
			aseg_applyxfm = fsl.ApplyXfm()
			aseg_applyxfm.inputs.in_file         = fs_aseg_swapdim
			aseg_applyxfm.inputs.reference       = anat_spm
			aseg_applyxfm.inputs.interp 		 = 'nearestneighbour'
			aseg_applyxfm.inputs.in_matrix_file  = fs2spm_xfm
			aseg_applyxfm.inputs.apply_xfm       = True
			aseg_applyxfm.inputs.out_file        = '%s/freesurfer_aseg_2spm.nii.gz' %out_fs_dir
			aseg_applyxfm.run()

			'============================================================================================'
			'                                     Create Tissue Masks                                    '
			'============================================================================================'
		if os.path.isfile(os.path.join(out_fs_dir, 'freesurfer_GM_mask.nii.gz')):
			print 'Tissues already extracted as nifti files.......... moving on'
		else:
			print 'Extracting Tissue classes from Labels and saving as a nifti file'
			aseg 		= str(os.path.join(workspace_dir, subject, 'segmentation_freesurfer','freesurfer_aseg_2spm.nii.gz'))
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
	#freesufer_create_tissues(pop_test, workspace_a, freesurfer_a)
	freesufer_create_tissues(population_a, workspace_a, freesurfer_a)
	freesufer_create_tissues(population_b, workspace_b, freesurfer_b)















