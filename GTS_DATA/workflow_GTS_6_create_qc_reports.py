__author__ = 'kanaan' 'March_21_2015'

import os
import errno
import string

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

#assert len(sys.argv)== 2
#subject_index=int(sys.argv[1])

'========================================================================================'

afsdir_a           = '/a/projects/nmr093a/'
afsdir_b           = '/a/projects/nmr093b/'


workspace_a    = '/scr/sambesi2/workspace/project_MRSTissueClass/GTS/study_a'
workspace_b    = '/scr/sambesi2/workspace/project_MRSTissueClass/GTS/study_b'

test_pop       = ['SI5T']
population_a   = [ 'BM8X', 'GF3T', 'GH4T', 'GSNT', 'HCTT', 'HM1X', 'HR8T', 'LMIT', 'MJBT', 'PAHT',
                   'RB1T', 'RJBT', 'RJJT', 'RMNT', 'SDCT', 'SI5T', 'SJBT', 'STQT', 'TJ5T', 'TR4T',
                   'TSCT', 'TV1T', 'ZT5T']
                  # no retest ---- >'KDET', 'NP4T', 'WJ3T',

population_b   = [ 'BM8X', 'GF3T', 'GH4T', 'GSNT', 'HCTT', 'HM1X', 'HR8T', 'LMIT', 'MJBT', 'PAHT',
                   'RB1T', 'RJBT', 'RJJT', 'RMNT', 'SDCT', 'SI5T', 'SJBT', 'STQT', 'TJ5T', 'TR4T',
                   'TSCT', 'TV1T', 'ZT5T', ]


'========================================================================================'



def create_mrs_qc(population, workspace_dir):
    for subject in population:
        import numpy as np
        import nibabel as nb
        import matplotlib.pyplot as plt
        import matplotlib
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm, mm, inch, pica
        import subprocess
	

        print '===================================================================================='        
        print '               Creating Quality Report for Subject %s' %subject	


        print 'Grabbing data--------'
        subject_dir = os.path.join(workspace_dir, subject)
        anatomical  = os.path.join(subject_dir, 'anatomical_original', 'ANATOMICAL.nii')
    
        mkdir_p(os.path.join(subject_dir, 'quality_control'))
        mkdir_p(os.path.join(subject_dir, 'quality_control', 'tmp'))
        out_dir = os.path.join(subject_dir, 'quality_control')
        tmp_dir = os.path.join(out_dir, 'tmp')


        #get masks
        acc = os.path.join(subject_dir, 'svs_voxel_mask', '%s%s_ACC_RDA_MASK.nii'%(subject,workspace_dir[-1]))
        tha = os.path.join(subject_dir, 'svs_voxel_mask', '%s%s_THA_RDA_MASK.nii'%(subject,workspace_dir[-1]))
        str = os.path.join(subject_dir, 'svs_voxel_mask', '%s%s_STR_RDA_MASK.nii'%(subject,workspace_dir[-1]))

        #get data
        anat_data =nb.load(anatomical).get_data()
        acc_data  =nb.load(acc).get_data()
        tha_data  =nb.load(tha).get_data()
        str_data = nb.load(str).get_data()

        # convert zeroes to nans
        acc_data[acc_data==0]=np.nan
        tha_data[tha_data==0]=np.nan
        str_data[str_data==0]=np.nan
	
        # grab and convert lcmodel plots
        acc_lcmodel = os.path.join(subject_dir, 'lcmodel', 'ACC', 'ps.pdf')
        tha_lcmodel = os.path.join(subject_dir, 'lcmodel', 'THA', 'ps.pdf')
        str_lcmodel = os.path.join(subject_dir, 'lcmodel', 'STR', 'ps.pdf')

        print 'Creating localization pngs'
        cnvrt_acc = ['convert', '-density', '150', '-trim', '%s'%acc_lcmodel,  '-quality', '300', '-sharpen', '0x1.0', '%s/ACC_lcmodel.png'%tmp_dir]
        cnvrt_tha = ['convert', '-density', '150', '-trim', '%s'%tha_lcmodel,  '-quality', '300', '-sharpen', '0x1.0', '%s/THA_lcmodel.png'%tmp_dir]
        cnvrt_str = ['convert', '-density', '150', '-trim', '%s'%str_lcmodel,  '-quality', '300', '-sharpen', '0x1.0', '%s/STR_lcmodel.png'%tmp_dir]

        subprocess.call(cnvrt_acc)
        subprocess.call(cnvrt_tha)
        subprocess.call(cnvrt_str)

        acc_lcmplot = os.path.join(tmp_dir, 'ACC_lcmodel-0.png')
        tha_lcmplot = os.path.join(tmp_dir, 'THA_lcmodel-0.png')
        str_lcmplot = os.path.join(tmp_dir, 'STR_lcmodel-0.png')

        # grab snr/fwhm data
        acc_snr = np.genfromtxt(os.path.join(subject_dir, 'lcmodel','ACC', 'snr.txt'), delimiter = ',')
        tha_snr = np.genfromtxt(os.path.join(subject_dir, 'lcmodel','THA', 'snr.txt'), delimiter = ',')
        str_snr = np.genfromtxt(os.path.join(subject_dir, 'lcmodel','STR', 'snr.txt'), delimiter = ',')


        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

        print''
        print '#############  Creating ACC Report   ###############'
        print '...done'

        if not os.path.isfile('%s/QC_REPORT_ACC.pdf'%out_dir):
            # plot acc
            fig =plt.figure()
            fig.set_size_inches(6.5, 6.5)
            fig.subplots_adjust(wspace=0.005)
            #1
            ax1 = plt.subplot2grid((1,3), (0,0),  colspan = 1, rowspan =1)
            ax1.imshow(anat_data[90,:,:], matplotlib.cm.bone_r )
            ax1.imshow(acc_data[90,:,:] , matplotlib.cm.rainbow_r, alpha = 0.7)
            ax1.set_xlim(23, 157)
            ax1.set_ylim(101, 230)
            ax1.axes.get_yaxis().set_visible(False)
            ax1.axes.get_xaxis().set_visible(False)
            #2
            ax2 = plt.subplot2grid((1,3), (0,1),  colspan = 1, rowspan =1)
            ax2.imshow(np.rot90(anat_data[:,:,90]), matplotlib.cm.bone_r )
            ax2.imshow(np.rot90(acc_data[:,:,90]) , matplotlib.cm.rainbow_r, alpha = 0.7 )
            ax2.set_xlim(230, 20)
            ax2.set_ylim(207, 4)
            ax2.axes.get_yaxis().set_visible(False)
            ax2.axes.get_xaxis().set_visible(False)
            #3
            ax3 = plt.subplot2grid((1,3), (0,2),  colspan = 1, rowspan =1)
            ax3.imshow(anat_data[:,190,:], matplotlib.cm.bone_r, origin='lower')
            ax3.imshow(acc_data[:,190,:] , matplotlib.cm.rainbow_r, alpha = 0.7, origin='lower')
            ax3.set_ylim(220, 50)
            ax3.axes.get_yaxis().set_visible(False)
            ax3.axes.get_xaxis().set_visible(False)
            fig.tight_layout()
            fig.savefig('%s/localization_acc.png'%out_dir, dpi=200, bbox_inches='tight')

            # create qc report

            acc_report = canvas.Canvas(os.path.join(out_dir,'QC_REPORT_ACC.pdf'), pagesize=(1280, 1556))
            acc_report.drawImage(os.path.join(out_dir,'localization_acc.png'), 1, inch*13.5)
            acc_report.setFont("Helvetica", 30)
            #c.drawString(inch*8, inch*11, 'SkullStripped' )
            acc_report.drawImage(acc_lcmplot, 30, inch*1, width = 1200, height = 800)
            acc_report.drawString(300, inch*20, ' %s%s, ACC, SNR=%s FWHM=%s ' %(subject,workspace_dir[-1],acc_snr[2],acc_snr[1]) )
            acc_report.showPage()
            acc_report.save()

        else:
            print 'ACC QC already created'


        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


        print''
        print  '#############  Creating THA Report   ###############'
        print '...done'
        if not os.path.isfile('%s/QC_REPORT_THA.pdf'%out_dir):
            # plot tha
            fig =plt.figure()
            fig.set_size_inches(6.5, 6.5)
            fig.subplots_adjust(wspace=0.005)
            #1
            ax1 = plt.subplot2grid((1,3), (0,0),  colspan = 1, rowspan =1)
            ax1.imshow(anat_data[140,:,:], matplotlib.cm.bone_r )
            ax1.imshow(tha_data[140,:,:] , matplotlib.cm.rainbow_r, alpha = 0.7)
            ax1.set_xlim(23, 157)
            ax1.set_ylim(101, 230)
            ax1.axes.get_yaxis().set_visible(False)
            ax1.axes.get_xaxis().set_visible(False)
            #2
            ax2 = plt.subplot2grid((1,3), (0,1),  colspan = 1, rowspan =1)
            ax2.imshow(np.rot90(anat_data[:,:,90]), matplotlib.cm.bone_r )
            ax2.imshow(np.rot90(tha_data[:,:,90]) , matplotlib.cm.rainbow_r, alpha = 0.7 )
            ax2.set_xlim(230, 20)
            ax2.set_ylim(207, 4)
            ax2.axes.get_yaxis().set_visible(False)
            ax2.axes.get_xaxis().set_visible(False)
            #3
            ax3 = plt.subplot2grid((1,3), (0,2),  colspan = 1, rowspan =1)
            ax3.imshow(anat_data[:,167,:], matplotlib.cm.bone_r, origin='lower')
            ax3.imshow(tha_data[:,167,:] , matplotlib.cm.rainbow_r, alpha = 0.7, origin='lower')
            ax3.set_xlim(38, 140)
            ax3.set_ylim(180, 80)
            ax3.axes.get_yaxis().set_visible(False)
            ax3.axes.get_xaxis().set_visible(False)
            fig.tight_layout()
            fig.savefig('%s/localization_tha.png'%out_dir, dpi=200, bbox_inches='tight')

            # create qc report

            tha_report = canvas.Canvas(os.path.join(out_dir,'QC_REPORT_THA.pdf'), pagesize=(1280, 1556))
            tha_report.drawImage(os.path.join(out_dir,'localization_tha.png'), 1, inch*13.5)
            tha_report.setFont("Helvetica", 30)
            #c.drawString(inch*8, inch*11, 'SkullStripped' )
            tha_report.drawImage(tha_lcmplot, 30, inch*1, width = 1200, height = 800)
            tha_report.drawString(300, inch*20, ' %s%s, THALAMUS, SNR=%s FWHM=%s ' %(subject,workspace_dir[-1],tha_snr[2],tha_snr[1]) )
            tha_report.showPage()
            tha_report.save()

        else:
            print 'THA QC already created'

        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


        print''
        print '#############  Creating STR Report   ###############'
        print '...done'
        if not os.path.isfile('%s/QC_REPORT_STR.pdf'%out_dir):
            # plot tha
            fig =plt.figure()
            fig.set_size_inches(6.5, 6.5)
            fig.subplots_adjust(wspace=0.005)
            #1
            ax1 = plt.subplot2grid((1,3), (0,0),  colspan = 1, rowspan =1)
            ax1.imshow(anat_data[120,:,:], matplotlib.cm.bone_r )
            ax1.imshow(str_data[120,:,:] , matplotlib.cm.rainbow_r, alpha = 0.7)
            ax1.set_xlim(23, 157)
            ax1.set_ylim(101, 230)
            ax1.axes.get_yaxis().set_visible(False)
            ax1.axes.get_xaxis().set_visible(False)
            #2
            ax2 = plt.subplot2grid((1,3), (0,1),  colspan = 1, rowspan =1)
            ax2.imshow(np.rot90(anat_data[:,:,70]), matplotlib.cm.bone_r )
            ax2.imshow(np.rot90(str_data[:,:,70]) , matplotlib.cm.rainbow_r, alpha = 0.7 )
            ax2.set_xlim(230, 20)
            ax2.set_ylim(207, 4)
            ax2.axes.get_yaxis().set_visible(False)
            ax2.axes.get_xaxis().set_visible(False)
            #3
            ax3 = plt.subplot2grid((1,3), (0,2),  colspan = 1, rowspan =1)
            ax3.imshow(anat_data[:,165,:], matplotlib.cm.bone_r, origin='lower')
            ax3.imshow(str_data[:,165,:] , matplotlib.cm.rainbow_r, alpha = 0.7, origin='lower')
            ax3.set_xlim(38, 140)
            ax3.set_ylim(180, 80)
            ax3.axes.get_yaxis().set_visible(False)
            ax3.axes.get_xaxis().set_visible(False)
            fig.tight_layout()
            fig.savefig('%s/localization_str.png'%out_dir, dpi=200, bbox_inches='tight')

            # create qc report

            str_report = canvas.Canvas(os.path.join(out_dir,'QC_REPORT_STR.pdf'), pagesize=(1280, 1556))
            str_report.drawImage(os.path.join(out_dir,'localization_str.png'), 1, inch*13.5)
            str_report.setFont("Helvetica", 30)
            #c.drawString(inch*8, inch*11, 'SkullStripped' )
            str_report.drawImage(str_lcmplot, 30, inch*1, width = 1200, height = 800)
            str_report.drawString(300, inch*20, ' %s%s, STRIATUM, SNR=%s FWHM=%s ' %(subject,workspace_dir[-1],str_snr[2],str_snr[1]) )
            str_report.showPage()
            str_report.save()

        else:
            print 'STR QC already created'


        print '===================================================================================='

if __name__ == "__main__":
    #create_mrs_qc(test_pop, workspace_a)
    create_mrs_qc(population_a, workspace_a)
    create_mrs_qc(population_b, workspace_b)
