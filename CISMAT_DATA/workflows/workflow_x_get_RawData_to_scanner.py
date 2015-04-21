__author__ = 'kanaan'



import os
import dicom as pydicom
import shutil
import errno




afs_dir        = '/xxx'
population_young_a = ['xxx']
workspace_a    = 'xxx'





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
