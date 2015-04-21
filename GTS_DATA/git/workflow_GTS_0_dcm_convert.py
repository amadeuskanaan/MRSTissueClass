__author__ = 'kanaan'  '11.03.2015'

import os
import dicom as pydicom
import nipype.interfaces.spm.utils as spmu

afs_dir_a      =  '/xxx'
afs_dir_b      =  '/xxx'

workspace_a    = '/scr/xxx'
workspace_b    = '/scr/xxx'

population_a   = [ 'xxx']
population_b   = [ 'xxx', ]

def dicom_convert(population, data_dir, workspace_dir):
    count=0
    for subject in population:
	count +=1        
	print '====================================================================='
        print '%s- DICOM CONVERSION for for %s' %(count,subject)
        # define dicom directory for each subject
        dicom_dir  = os.path.join(data_dir, subject, 'DICOM' )

        # define desitation directory for nifti outputs
        try:
            os.makedirs(os.path.join(workspace_dir, subject, 'anatomical_original'))
        except OSError:
            out_nifti_dir = str(os.path.join(workspace_dir, subject, 'anatomical_original'))
        out_nifti_dir  = str(os.path.join(workspace_dir, subject, 'anatomical_original'))

        if not os.path.isfile(os.path.join(out_nifti_dir, 'ANATOMICAL.nii')):
            # create a list of all dicoms with absolute paths for each file
            dicom_list = []
            for dicom in os.listdir(dicom_dir):
                dicomstr = os.path.join(dicom_dir, dicom)
                dicom_list.append(dicomstr)

            # grab SeriesDescription and append T1 files to list
            T1_list = []
            print 'Reading dicom series descriptions'
            for dicom in dicom_list:
                try:
                    dcm_read = pydicom.read_file(dicom, force = True)
                    sequence = dcm_read.SeriesDescription
                except AttributeError:
                    continue

                if 'mp2rage_p3_602B_UNI_Images' in sequence:
                    T1_list.append(dicom)

            # convert T1 anatomical to NIFTI with SPM
            print 'Converting Dicom to Nifti for %s' %subject
            spm_dicom_convert                   = spmu.DicomImport()
            spm_dicom_convert.inputs.format     = 'nii'
            spm_dicom_convert.inputs.in_files   = T1_list
            spm_dicom_convert.inputs.output_dir = out_nifti_dir
            spm_dicom_convert.run()

            #rename file
            for file in os.listdir(out_nifti_dir):
                if file.endswith('nii'):
                    os.rename(str(os.path.join(out_nifti_dir, file)),
                              str(os.path.join(out_nifti_dir, 'ANATOMICAL.nii')))
        else:
            print 'subject already processed.......moving on'

        print '====================================================================='
        print ''

'######################################################################################################################################'
'######################################################################################################################################'


#
#
if __name__ == "__main__":
    dicom_convert(population_a, afs_dir_a, workspace_a) #complete on 11.03.2015
    dicom_convert(population_b, afs_dir_b, workspace_b) #complete on 11.03.2015
