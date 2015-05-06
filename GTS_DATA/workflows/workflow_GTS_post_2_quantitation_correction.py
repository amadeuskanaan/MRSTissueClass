__author__ = 'kanaan' 'April 09 2015'

import os
import pandas as pd
import string

#'========================================================================================'
afs_dir_a      =  '/xxx'
afs_dir_b      =  '/xxx'

workspace_a    = '/scr/xxx'
workspace_b    = '/scr/xxx'

population_a   = [ 'xxx']
population_b   = [ 'xxx', ]
#'========================================================================================'

def quantitation_correction(population, workspace_dir, voxel_name):

    # get lcmodel output dataframe
    quantitation = pd.read_csv(os.path.join(workspace_dir,'group_statistics','quantitation_%s_%s_lcmodel.csv'%(voxel_name, workspace_dir[-1])))
    quantitation.drop(quantitation.columns[0], axis = 1, inplace= True)

    # get tissue proportions dataframe
    proportions  = pd.read_csv(os.path.join(workspace_dir, 'group_statistics', 'proportions_%s_%s.csv'%(voxel_name, workspace_dir[-1])))
    proportions.drop(proportions.columns[0], axis = 1, inplace= True)

    #grab tissue proportion data separately
    gm_spm  = proportions['GM_SPM_%s'%voxel_name]
    gm_fsl  = proportions['GM_FSL_%s'%voxel_name]
    gm_fsu  = proportions['GM_SURFER_%s'%voxel_name]

    wm_spm  = proportions['WM_SPM_%s'%voxel_name]
    wm_fsl  = proportions['WM_FSL_%s'%voxel_name]
    wm_fsu  = proportions['WM_SURFER_%s'%voxel_name]

    cm_spm  = proportions['CSF_SPM_%s'%voxel_name]
    cm_fsl  = proportions['CSF_FSL_%s'%voxel_name]
    cm_fsu  = proportions['CSF_SURFER_%s'%voxel_name]


    # grab metabolites to correct

    creatine   = quantitation[' Cre']
    choline    = quantitation[' GPC+PCh']
    naa_naag   = quantitation[' NAA+NAAG']
    inositol   = quantitation[' mI']
    glutamate  = quantitation[' Glu']
    glutamine  = quantitation[' Gln']
    glx        = quantitation[' Glu+Gln']

    def correct(lcmodel, frac_gm, frac_wm, frac_csf):

        import math

        #lcmodel correction factor
        factor =(55.55 / (35.88 * 0.7))

        # relative water content in tissue.. determined experimentally.
        alpha_gm  = 0.81
        alpha_wm  = 0.71
        alpha_csf = 1.0

        #attentuation factor for water
        R_H2O_GM  = (1.0-math.e**(-3000.0/1820.0)) * math.e**(-30.0/99.0)
        R_H2O_WM  = (1.0-math.e**(-3000.0/1084.0)) * math.e**(-30.0/69.0)
        R_H2O_CSF = (1.0-math.e**(-3000.0/4163.0)) * math.e**(-30.0/503.0)

        #########  Correction Equations  #######
        # tissel equation
        Cmet1 =  (lcmodel    *   (((frac_csf    * 1. * (1. - frac_csf)) + (frac_gm * 0.81 + frac_wm * 0.71))/ (1. - frac_csf )))

        # gusseuw equation
        Cmet2  =  (lcmodel)   *   ((( frac_gm    * alpha_gm    * R_H2O_GM  +
                                     frac_wm    * alpha_wm    * R_H2O_WM  +
                                     frac_csf   * alpha_csf   * R_H2O_CSF ) /
                                    (frac_gm    * 1.0    + frac_wm * 1.0))) * factor
        # gusseew csf equation
        Cmet3 = (lcmodel)   * (1/ (1-frac_csf) )

        return Cmet2

    #########################################################################################################
    #spm
    spm_creatine   = correct(creatine,  gm_spm, wm_spm, cm_spm)
    spm_choline    = correct(choline,   gm_spm, wm_spm, cm_spm)
    spm_naa_naag   = correct(naa_naag,  gm_spm, wm_spm, cm_spm)
    spm_inositol   = correct(inositol,  gm_spm, wm_spm, cm_spm)
    spm_glutamate  = correct(glutamate, gm_spm, wm_spm, cm_spm)
    spm_glutamine  = correct(glutamine, gm_spm, wm_spm, cm_spm)
    spm_glx        = correct(glx,       gm_spm, wm_spm, cm_spm)

    #quantitation spm
    column_order= ['SUBJECTS_%s'%workspace_dir[-1] ,'Cre', 'GPC+PCh','NAA+NAAG','mI','Glu','Gln','Glu+Gln']

    quantitation_spm = pd.DataFrame({'SUBJECTS_%s'%workspace_dir[-1] :  quantitation['Subject'],
                                  'Cre'                           :  spm_creatine           ,
                                  'GPC+PCh'                       :  spm_choline            ,
                                  'NAA+NAAG'                      :  spm_naa_naag           ,
                                  'mI'                            :  spm_inositol           ,
                                  'Glu'                           :  spm_glutamate          ,
                                  'Gln'                           :  spm_glutamine          ,
                                  'Glu+Gln'                       :  spm_glx                ,})

    quantitation_spm = quantitation_spm.reindex(columns=column_order)

    #########################################################################################################
    #fsl
    fsl_creatine   = correct(creatine,  gm_fsl, wm_fsl, cm_fsl)
    fsl_choline    = correct(choline,   gm_fsl, wm_fsl, cm_fsl)
    fsl_naa_naag   = correct(naa_naag,  gm_fsl, wm_fsl, cm_fsl)
    fsl_inositol   = correct(inositol,  gm_fsl, wm_fsl, cm_fsl)
    fsl_glutamate  = correct(glutamate, gm_fsl, wm_fsl, cm_fsl)
    fsl_glutamine  = correct(glutamine, gm_fsl, wm_fsl, cm_fsl)
    fsl_glx        = correct(glx,       gm_fsl, wm_fsl, cm_fsl)


    #quantitation fsl
    quantitation_fsl = pd.DataFrame({'SUBJECTS_%s'%workspace_dir[-1] :  quantitation['Subject'],
                                  'Cre'                           :  fsl_creatine           ,
                                  'GPC+PCh'                       :  fsl_choline            ,
                                  'NAA+NAAG'                      :  fsl_naa_naag           ,
                                  'mI'                            :  fsl_inositol           ,
                                  'Glu'                           :  fsl_glutamate          ,
                                  'Gln'                           :  fsl_glutamine          ,
                                  'Glu+Gln'                       :  fsl_glx                ,})

    quantitation_fsl = quantitation_fsl.reindex(columns=column_order)

    #########################################################################################################
    #fsu
    fsu_creatine   = correct(creatine,  gm_fsu, wm_fsu, cm_fsu)
    fsu_choline    = correct(choline,   gm_fsu, wm_fsu, cm_fsu)
    fsu_naa_naag   = correct(naa_naag,  gm_fsu, wm_fsu, cm_fsu)
    fsu_inositol   = correct(inositol,  gm_fsu, wm_fsu, cm_fsu)
    fsu_glutamate  = correct(glutamate, gm_fsu, wm_fsu, cm_fsu)
    fsu_glutamine  = correct(glutamine, gm_fsu, wm_fsu, cm_fsu)
    fsu_glx        = correct(glx,       gm_fsu, wm_fsu, cm_fsu)

    #quantitation fsu
    quantitation_fsu = pd.DataFrame({'SUBJECTS_%s'%workspace_dir[-1] :  quantitation['Subject'],
                                  'Cre'                           :  fsu_creatine           ,
                                  'GPC+PCh'                       :  fsu_choline            ,
                                  'NAA+NAAG'                      :  fsu_naa_naag           ,
                                  'mI'                            :  fsu_inositol           ,
                                  'Glu'                           :  fsu_glutamate          ,
                                  'Gln'                           :  fsu_glutamine          ,
                                  'Glu+Gln'                       :  fsu_glx                ,})
    quantitation_fsu = quantitation_fsu.reindex(columns=column_order)
    #########################################################################################################

    # save outsputs as csv files
    quantitation_spm.to_csv(os.path.join(workspace_dir, 'group_statistics','quantitation_%s_correction_%s_spm.csv'%(voxel_name, workspace_dir[-1])))
    quantitation_fsl.to_csv(os.path.join(workspace_dir, 'group_statistics','quantitation_%s_correction_%s_fsl.csv'%(voxel_name, workspace_dir[-1])))
    quantitation_fsu.to_csv(os.path.join(workspace_dir, 'group_statistics','quantitation_%s_correction_%s_fsu.csv'%(voxel_name, workspace_dir[-1])))

    return quantitation, quantitation_spm, quantitation_fsl, quantitation_fsu


