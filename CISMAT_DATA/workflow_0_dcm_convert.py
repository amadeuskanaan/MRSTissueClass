__author__ = 'kanaan...Feb_20_2015' # complete run on 02.03.2015

import os
import dicom as pydicom
import nipype.interfaces.spm.utils as spmu

afs_dir        = '/a/projects/cnps124_ms/probands/'

population_young_a = ['BB2T040407.TRIO', 'EK5T040407.TRIO', 'FM4T040330.TRIO', 'GA3T040405.TRIO', 'HS5T040712.TRIO','KM4T040427.TRIO',
                      'ME1T040628.TRIO', 'MH4T040407.TRIO', 'NC2T040405.TRIO', 'NT2T040407.TRIO', 'WM8T040420.TRIO','ZK1T040405.TRIO']
population_young_b = ['BB2T040628.TRIO', 'EK5T040706.TRIO', 'FM4T040712.TRIO', 'GA3T040629.TRIO', 'HS5T040810.TRIO', 'KM4T040719.TRIO',
                      'ME1T040712.TRIO', 'MH4T040628.TRIO', 'NC2T040712.TRIO', 'NT2T040628.TRIO', 'WM8T040706.TRIO', 'ZK1T040628.TRIO']
population_young_c = ['BB2T040719.TRIO', 'EK5T040719.TRIO', 'FM4T040727.TRIO', 'GA3T040907.TRIO', 'HS5T040901.TRIO','ME1T040803.TRIO',
                                         'MH4T040719.TRIO', 'NC2T040810.TRIO', 'NT2T040712.TRIO', 'WM8T040719.TRIO', 'ZK1T040713.TRIO']

workspace_a    = '/scr/sambesi2/workspace/project_MRSTissueClass/CISMAT/study_a'
workspace_b    = '/scr/sambesi2/workspace/project_MRSTissueClass/CISMAT/study_b'
workspace_c    = '/scr/sambesi2/workspace/project_MRSTissueClass/CISMAT/study_c'


def dicom_convert(population, data_dir, workspace_dir):
    for subject in population:
        print '##############################################'
        print '  SPM DICOM CONVERSION for for %s' %subject
        # define dicom directory for each subject
        dicom_dir  = os.path.join(data_dir, subject[0:4], 'RawData', subject )

        # define desitation directory for nifti outputs
        try:
            os.makedirs(os.path.join(workspace_dir, subject[0:4], 'anatomical_original'))
        except OSError:
            continue

        out_nifti_dir  = str(os.path.join(workspace_dir, subject[0:4], 'anatomical_original'))

        # create a list of all dicoms with absolute paths for each file
        dicom_list = []
        for dicom in os.listdir(dicom_dir):
            dicom = os.path.join(dicom_dir, dicom)
            dicom_list.append(dicom)

        # grab SeriesDescription and append T1 files to list
        T1_list = []
        print 'reading dicom series descriptions'
        for dicom in dicom_list:
            try:
                dcm_read = pydicom.read_file(dicom)
                sequence = dcm_read.SeriesDescription
            except AttributeError:
                continue

            if 't1_mpr_sag_short' in sequence:
                T1_list.append(dicom)

            else:
                continue

        # convert T1 anatomical to NIFTI with SPM
        print 'Converting Dicom to Nifti for %s' %subject
        spm_dicom_convert                   = spmu.DicomImport()
        spm_dicom_convert.inputs.format     = 'nii'
        spm_dicom_convert.inputs.in_files   = T1_list
        spm_dicom_convert.inputs.output_dir = out_nifti_dir
        spm_dicom_convert.run()
        print '..................................'

        #rename file
        for file in os.listdir(out_nifti_dir):
            if file.endswith('nii'):
                os.rename(str(os.path.join(out_nifti_dir, file)),
                          str(os.path.join(out_nifti_dir, 'ANATOMICAL.nii')))

        print '  DONE  %s' %subject
        print '##############################################'
        print ''

'######################################################################################################################################'
'######################################################################################################################################'


#
#
# if __name__ == "__main__":
    #dicom_convert(population_young_a, afs_dir, workspace_a) # complete
    #spm_convert(population_young_b, afs_dir, workspace_b)   # complete
    #spm_convert(population_young_c, afs_dir, workspace_c)   # complete