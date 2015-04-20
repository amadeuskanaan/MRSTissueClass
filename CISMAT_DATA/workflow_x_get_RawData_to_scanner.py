__author__ = 'kanaan'



import os
import dicom as pydicom
import shutil
import errno

afs_dir        = '/a/projects/cnps124_ms/probands/'
carlos_subject = '/scr/carlos1/xchg/ASK/CISMAT_DATA_UPLOAD'

carlos_all_a     = '/scr/carlos1/xchg/ASK/CISMAT_DATA_UPLOAD/population_a_dicoms'
carlos_all_b     = '/scr/carlos1/xchg/ASK/CISMAT_DATA_UPLOAD/population_b_dicoms'
carlos_all_c     = '/scr/carlos1/xchg/ASK/CISMAT_DATA_UPLOAD/population_c_dicoms'

population_young_a = ['BB2T040407.TRIO', 'EK5T040407.TRIO', 'FM4T040330.TRIO', 'GA3T040405.TRIO', 'HS5T040712.TRIO','KM4T040427.TRIO',
                      'ME1T040628.TRIO', 'MH4T040407.TRIO', 'NC2T040405.TRIO', 'NT2T040407.TRIO', 'WM8T040420.TRIO','ZK1T040405.TRIO']
population_young_b = ['BB2T040628.TRIO', 'EK5T040706.TRIO', 'FM4T040712.TRIO', 'GA3T040629.TRIO', 'HS5T040810.TRIO', 'KM4T040719.TRIO',
                      'ME1T040712.TRIO', 'MH4T040628.TRIO', 'NC2T040712.TRIO', 'NT2T040628.TRIO', 'WM8T040706.TRIO', 'ZK1T040628.TRIO']
population_young_c = ['BB2T040719.TRIO', 'EK5T040719.TRIO', 'FM4T040727.TRIO', 'GA3T040907.TRIO', 'HS5T040901.TRIO','ME1T040803.TRIO',
                      'MH4T040719.TRIO', 'NC2T040810.TRIO', 'NT2T040712.TRIO', 'WM8T040719.TRIO', 'ZK1T040713.TRIO']
def get_svs_dicoms(population, afs_dir, out_dir, dump_dir):
    count= 0
    for subject in population:
        # define dicom directory for each subject
        dicom_dir       = os.path.join(afs_dir, subject[0:4], 'RawData', subject)
        out_dir_sub     = os.path.join(out_dir, subject)
        print 'Copying DICOM of subject %s to carlos'%subject[0:10]
        print ''
        print 'source_dir      = %s' %dicom_dir
        print 'destination_dir = %s' %out_dir_sub
        print '.'
        print '.'
        print '.'
        shutil.copytree(dicom_dir, out_dir_sub)

        print 'Moving all data into population_dir '
        count +=1
        out_dir_all = os.path.join(dump_dir)

        for file in os.listdir(out_dir_sub):
            #print file
            shutil.move(os.path.join(out_dir_sub, file),
                       os.path.join(out_dir_all, '%s_%s_'%(count, subject[0:10]) + file ))

        # # define desitation directory for nifti outputs
        # try:
        #     os.makedirs(os.path.join(out_dir, subject[0:4]))
        # except OSError:
        #     svs_folder  = str(os.path.join(out_dir, subject[0:4]))
        #
        # svs_folder  = str(os.path.join(out_dir, subject[0:4]))
        #
        # # create a list of all dicoms with absolute paths for each file
        # dicom_list = []
        # for dicom in os.listdir(dicom_dir):
        #     dicom = os.path.join(dicom_dir, dicom)
        #     dicom_list.append(dicom)
        #
        # # grab SeriesDescription and append SVS files to list
        # SVS_list = []
        # for dicom in dicom_list:
        #     try:
        #         dcm_read = pydicom.read_file(dicom)
        #         sequence = dcm_read.SeriesDescription
        #         if 'svs' in sequence:
        #             shutil.copy(dicom ,  str(os.path.join(out_dir, subject[0:4], dicom[-6:0])))
        #
        #     except AttributeError:
        #        continue



get_svs_dicoms(population_young_b, afs_dir, carlos_subject, carlos_all_b)
get_svs_dicoms(population_young_c, afs_dir, carlos_subject, carlos_all_c)
