__author__ = 'kanaan'

import os
import subprocess


afs_dir        = '/xxx'
population_young_a = ['xxx']
workspace_a    = 'xxx'


def run_lcmodel_CISMAT_data(population, workspace_dir):
    print ' Remember to SSH into Sandra.. You will get empty demo results if you dont. '

    count = 0

    for subject in population:
        count +=1
        print '========================================================================================'
        print '                    %s-Running LCMODEL ON subject %s_%s' %(count,subject[0:4], subject[4:10])
        print '.'
        # define subject directory and location of rda file
        subject_dir   = os.path.join(workspace_dir ,  subject[0:4])
        rda_dir       = os.path.join(subject_dir   , 'rda_original')
        rda_file      = os.path.join(rda_dir, '%s.rda'%subject[0:10])

        MET = []
        H2O = []


        print 'Creating lcmodel output directories'
        try:
            os.makedirs(os.path.join(workspace_dir, subject[0:4], 'lcmodel'))
        except OSError:
            lcmodel_dir = os.path.join(workspace_dir, subject[0:4], 'lcmodel')
        lcmodel_dir = os.path.join(workspace_dir, subject[0:4], 'lcmodel')

        '''
        Creating output Directories
        '''

        #Creating metabolite dir where bin2raw lcmodel outputs will be located
        # RAW file will contain the frequencies in ascii format
        try:
            os.makedirs(os.path.join(lcmodel_dir, 'met'))
        except OSError:
            bin2raw_dir = os.path.join(lcmodel_dir, 'met')
        bin2raw_dir = os.path.join(lcmodel_dir, 'met')

        #creating temp dir for control file
        #control file is the holy grail.. contains all the information that the lcmodel execution scripts need to run
        try:
            os.makedirs(os.path.join(lcmodel_dir, 'temp'))
        except OSError:
            temp_dir = os.path.join(lcmodel_dir, 'temp')
        temp_dir = os.path.join(lcmodel_dir, 'temp')

        print '....All output dirs createed succesfully'
        print '....Files should be located here --->%s' %lcmodel_dir
        print '.'

        '''
        Read Scam parameters from RDA file
        '''
        rda_read = open(rda_file, 'r')

        for line in rda_read:
            if 'SeriesDescription' in line:
                Series = line[19:30]
            elif 'TR:' in line:
                TR = line[4:8]
            elif 'TE:' in line:
                TE = line[4:6]
            elif 'NumberOfAverages' in line:
                NS = line[18:21]
            elif 'AcquisitionNumber' in line:#
                ACQ = line[19:21]
            elif 'PatientSex' in line:
                Sex = line[12:13]
            elif 'SeriesNumber' in line:
                Seriesnum = line[14:16]
            elif 'PatientAge' in line:#
                Age = line[12:15]
            elif 'PatientWeight' in line:
                Weight = line[15:17]
            elif 'PixelSpacingRow' in line:
                PSR = float(line[17:20])
            elif 'PixelSpacingCol' in line:
                PSC = float(line[17:20])
            elif 'PixelSpacing3D:' in line:
                PS3d = float(line[16:19])

        svs_volume = PSR * PSC * PS3d

        '''
        BIN2RAW
        '''

        #run bin2raw
        print 'Running LCMODEL bin2raw binary to generate metabolite RAW frequency file'
        #run matlab code to create registered mask from rda file
        bin2raw_command = ['/home/raid3/kanaan/.lcmodel/siemens/bin2raw', '%s'%rda_file, '%s/'%lcmodel_dir, 'met']
        print subprocess.list2cmdline(bin2raw_command)

        #print bin2raw_command
        subprocess.call(bin2raw_command)
        print 'raw file generated'
        print '........'

        '''
        Build the control file... The holy grail.....

        Usually, lcmgui takes care of this.. therfore impoartant to ensure paramater accuracy...
        '''
        print 'Creating new control file for lcmodel'
        file = open(os.path.join(lcmodel_dir, 'control'), "w")
        file.write("$LCMODL\n")
        #file.write("title= Subject=%s(%s %s %skg); Date:%s; Series/Acq=%s/%s; %s; TR/TE/NS=%s/%s/%s; %s \n" %(subject[0:4], Sex, Age, Weight,  subject[4:10], Seriesnum,ACQ, Series, TR,TE, NS, svs_volume))
        file.write("title= '%s(%s %s %skg), Date:%s, TR/TE/NS=%s/%s/%s\n'" %(subject[0:4],Sex, Age, Weight,subject[4:10],TR,TE, NS))
        file.write("srcraw='%s' \n" %rda_file)
        file.write("savdir='%s' \n" %lcmodel_dir)
        file.write("ppmst= 4.0\n")
        file.write("ppmend= 0.2\n")
        file.write("nunfil= 1024\n")
        file.write("ltable= 7\n")
        file.write("lps= 8\n")
        file.write("lcsv= 11\n")
        file.write("hzpppm= 1.2328e+02\n")
        file.write("filtab= '%s/table'\n" %lcmodel_dir)
        file.write("filraw= '%s/met/RAW'\n" %lcmodel_dir)
        file.write("filps= '%s/ps'\n" %lcmodel_dir)
        file.write("filcsv= '%s/spreadsheet.csv'\n" %lcmodel_dir)
        file.write("filbas= '/home/raid3/kanaan/.lcmodel/basis-sets/press_te30_3t_01a.basis'\n")
        file.write("echot= %s.00 \n" %TE)
        file.write("deltat= 8.330e-04\n")
        file.write("$END\n")
        file.close()
        print '....Control filed created'
        print '.....'

        '''
        Run LCMODEL Execution script StandradA4pdf
        '''
        print '..'
        print 'Processing Spectra with LCMODEL'
        lcmodel_command = ['sh',
                           '/home/raid3/kanaan/.lcmodel/execution-scripts/standardA4pdf',
                           '%s' %lcmodel_dir,
                           '19',
                           '%s' %lcmodel_dir,
                           '%s' %lcmodel_dir]

        print subprocess.list2cmdline(lcmodel_command)

        #print bin2raw_command
        subprocess.call(lcmodel_command)
        print '..'
        print '..'
        print '..'
        print 'lcmodel processing complete'
        print '###################################################'

run_lcmodel(population_a, workspace_a)



