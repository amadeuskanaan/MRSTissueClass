__author__ = 'kanaan' '18.03.2015'

import os
import errno
import string
import subprocess

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
valid_chars = '-_.() %s%s' %(string.ascii_letters, string.digits)


'========================================================================================'

afs_dir_a      =  '/xxx'
afs_dir_b      =  '/xxx'

workspace_a    = '/scr/xxx'
workspace_b    = '/scr/xxx'

population_a   = [ 'xxx']
population_b   = [ 'xxx', ]

'========================================================================================'

def run_lcmodel_GTS_data(population_list, population_type, workspace_dir, afs_dir):
    print ' Remember to SSH into Sandra.. You will get empty demo results if you dont. '

    count = 0
    for subject in population_list:
        count +=1
        print '=======================x================================================================='
        print '                   %s-Running Lcmodel for subject %s_%s '%(count,subject,workspace_dir[-1])
        print ''

        #define subject afs_dir
        subject_afs       = os.path.join(afs_dir, population_type, subject, 'SVS')
        subject_workspace = os.path.join(workspace_dir, subject)

        ACC_MET=[]
        THA_MET=[]
        STR_MET=[]

        ACC_H2O=[]
        THA_H2O=[]
        STR_H2O=[]

        '========================================================================================'
        '                              Locating RDA files                                        '
        '========================================================================================'
        #locating and copying rda_files locally
        for root, dirs, files in os.walk(subject_afs, topdown=False):
            for name in files:
                if 'meas' not in name:
                    if 'SUPPRESSED' in name or 'WS' in name:
                        if 'ACC' in name or 'acc' in name or 'Acc' in name:
                            ACC_MET.append(os.path.join(root, name))
                        elif 'TH' in name or 'th' in name or 'Th' in name:
                            THA_MET.append(os.path.join(root,name))
                        elif 'STR' in name or 'ST' in name or 'st' in name:
                            STR_MET.append(os.path.join(root, name))
                    if 'HEAD' in name and 'REF' in name:
                        if 'ACC' in name or 'acc' in name or 'Acc' in name:
                            ACC_H2O.append(os.path.join(root, name))
                        elif 'TH' in name or 'th' in name or 'Th' in name:
                            THA_H2O.append(os.path.join(root,name))
                        elif 'STR' in name or 'ST' in name or 'st' in name:
                            STR_H2O.append(os.path.join(root, name))

        print  '#########ACC##########'
        print ACC_MET[0]
        print ACC_H2O[0]
        print ''
        print  '#########THA##########'
        print THA_MET[0]
        print THA_H2O[0]
        print ''
        print  '#########STR##########'
        print STR_MET[0]
        print STR_H2O[0]

        '========================================================================================'
        '                                    LCMODEL                                              '
        '========================================================================================'


        # 'Warning---> Must run from Sandra where the lcmodel licence is located'
        #
        # $Step 1: Create output folders
        #          $mkdir ./met
        #          $mkdir ./water
        #
        # $Step 2: Run lcmodel binary bin2raw to generete lcmodel freq/header input file
        #          $ $HOME/.lcmodel/siemens/bin2raw {./folder}/WS_SUPPRESSED.rda ./ met
        #          $ $HOME/.lcmodel/siemens/bin2raw {./folder}REF_HEAD.rda ./ water
        #
        # $Step 3: Create control file with the correct header information... This is the holy grail..
        #          For best effects, generate a control via lcmodel and use this as a template for your data
        #
        # $Step 4: Run the lcmodel  executable-script standardA4pdf for quantitation
        #          $sh standard4pdf {./folder} 19 {./folder} {./folder}

        voxels = {'ACC': (ACC_MET[0], ACC_H2O[0]),
                  'THA': (THA_MET[0], THA_H2O[0]),
                  'STR': (STR_MET[0], STR_H2O[0]),}

        for voxel in voxels:

            if os.path.isfile(voxels[voxel][0]) and  os.path.isfile(voxels[voxel][1]):
                print ''
                print '========================='
                print '====    %s ZONE     ===='%voxel
                print '========================='

                #creating local dir to place oroginal and byproduct files

                mkdir_p(os.path.join(workspace_dir, subject, 'lcmodel'))
                mkdir_p(os.path.join(workspace_dir, subject, 'lcmodel', '%s'%voxel))
                mkdir_p(os.path.join(workspace_dir, subject, 'lcmodel', '%s'%voxel, 'met'))
                mkdir_p(os.path.join(workspace_dir, subject, 'lcmodel', '%s'%voxel, 'h2o'))
                lcmodel_dir  = os.path.join(workspace_dir, subject, 'lcmodel', '%s'%voxel)

                '''
                Read Scan parameters from RDA file
                '''
                reader = open(voxels[voxel][0], 'r')
                for line in reader:
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
                    elif 'StudyDate' in line:
                        datex = line[0:19]

                volume = PSR * PSC * PS3d

                '''
                BIN2RAW
                '''
                #run bin2raw ..... must be in SANDRA
                if os.path.isfile(os.path.join(lcmodel_dir, 'met', 'RAW')) and  os.path.isfile(os.path.join(lcmodel_dir, 'h2o', 'RAW')):
                    print 'Bin2raw already run.........................moving on '
                else:
                    print 'RDA files exist. Generating RAW frequency files with BIN2RAW'
                    met_bin2raw = ['/home/raid3/kanaan/.lcmodel/siemens/bin2raw', '%s'%voxels[voxel][0], '%s/'%lcmodel_dir, 'met']
                    h2o_bin2raw = ['/home/raid3/kanaan/.lcmodel/siemens/bin2raw', '%s'%voxels[voxel][1], '%s/'%lcmodel_dir, 'h2o']

                    subprocess.call(met_bin2raw)
                    subprocess.call(h2o_bin2raw)

                '''
                Building the control file
                '''
                if os.path.isfile(os.path.join(lcmodel_dir, 'control')):
                    print 'Control file already created................moving on'
                else:
                    print 'Processing Spectra with LCMODEL'
                    print '...building control file'
                    file = open(os.path.join(lcmodel_dir, 'control'), "w")
                    file.write(" $LCMODL\n")
                    file.write(" title= '%s(%s %s %skg); %s; %s %sx%sx%s; TR/TE/NS=%s/%s/%s' \n" %(subject, Sex, Age, Weight, datex, voxel, PSR,PSC,PS3d, TR,TE, NS ))
                    file.write(" srcraw= '%s' \n" %voxels[voxel][0])
                    file.write(" srch2o= '%s' \n" %voxels[voxel][1])
                    file.write(" savdir= '%s' \n" %lcmodel_dir)
                    file.write(" ppmst= 4.0\n")
                    file.write(" ppmend= 0.2\n")
                    file.write(" nunfil= 1024\n")
                    file.write(" ltable= 7\n")
                    file.write(" lps= 8\n")
                    file.write(" lcsv= 11\n")
                    file.write(" hzpppm= 1.2328e+02\n")
                    file.write(" filtab= '%s/table'\n" %lcmodel_dir)
                    file.write(" filraw= '%s/met/RAW'\n" %lcmodel_dir)
                    file.write(" filps= '%s/ps'\n" %lcmodel_dir)
                    file.write(" filh2o= '%s/h2o/RAW'\n" %lcmodel_dir)
                    file.write(" filcsv= '%s/spreadsheet.csv'\n" %lcmodel_dir)
                    file.write(" filbas= '/home/raid3/kanaan/.lcmodel/basis-sets/press_te30_3t_01a.basis'\n")
                    file.write(" echot= %s.00 \n" %TE)
                    file.write(" dows= T \n")
                    file.write(" doecc= T\n")
                    file.write(" deltat= 8.330e-04\n")
                    file.write(" $END\n")
                    file.close()


                '''
                Execute quantitation.... running standardA4pdf
                '''

                #      LCMgui executes this script in background with 3 or 4 arguments.
                # They are $1--$4:
                #
                # $1: absolute path of temporary directory produced by LCMgui.
                #
                # $2: For the N'th run started from an LCMgui session,
                #     $2 = N*5 + <your default "nice" value> (but with $2 <= 19).
                #     This provides a crude way to assign successive runs lower priorities,
                #     as illustrated below.
                #
                # $3: absolute path of the Output Script that will print out your results
                #     and save files.  This Output Script is automatically produced by LCMgui.
                #
                # $4: absolute path of the directory where your results will be saved, if you
                #     elected in the LCMgui "Save Files" menu to have files saved.
                #     If you did not elect to have files saved, then $4 is missing.


                if os.path.isfile(os.path.join(lcmodel_dir, 'spreadsheet.csv')):
                    print 'Spectrum already processed .................moving on'
                else:
                    print '...running standardA4pdf execution-script '
                    print ''
                    lcmodel_command = ['/bin/sh','/home/raid3/kanaan/.lcmodel/execution-scripts/standardA4pdfv3',
                                            '%s' %lcmodel_dir,
                                            '19',
                                            '%s' %lcmodel_dir,
                                            '%s' %lcmodel_dir]

                    print subprocess.list2cmdline(lcmodel_command)
                    print ''
                    #print bin2raw_command
                    subprocess.call(lcmodel_command)
                    
                    reader = open(os.path.join(lcmodel_dir, 'table'), 'r')
                    for line in reader:
                        if 'FWHM' in line:
                            fwhm = float(line[9:14])
                            snrx  = line[29:31]

                            fwhm_hz = fwhm * 123.24
                            file = open(os.path.join(lcmodel_dir, 'snr.txt'), "w")
                            file.write('%s, %s, %s' %(fwhm,fwhm_hz, snrx))
                            file.close()
                    
if __name__ == "__main__":
    #run_lcmodel_GTS_data(test_pop, 'probands', workspace_a, afsdir_a, )
    run_lcmodel_GTS_data(population_a, 'probands', workspace_a, afsdir_a)
    run_lcmodel_GTS_data(population_b, 'probands', workspace_b, afsdir_b)
