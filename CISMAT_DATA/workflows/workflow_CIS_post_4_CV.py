__author__ = 'kanaan'

import os
import pandas as pd
import numpy as np

workspace_a    = 'xxx'
workspace_b    = 'xxx'


population_a = ['xxx']

population_b = ['xxx']

def calc_cv(workspace_a, workspace_b):

    # get lcmodel quantitation dataframe
    lcm_a = pd.read_csv(os.path.join(workspace_a,'group_statistics','lcmodel_%s.csv'%workspace_a[-1]))
    lcm_a.drop(lcm_a.columns[0], axis = 1, inplace= True)
    lcm_b = pd.read_csv(os.path.join(workspace_b,'group_statistics','lcmodel_%s.csv'%workspace_b[-1]))
    lcm_b.drop(lcm_b.columns[0], axis = 1, inplace= True)

    #get quantiation correction dataframes
    spm_a = pd.read_csv(os.path.join(workspace_a,'group_statistics','lcmodel_correction_%s_spm.csv'%workspace_a[-1]))
    spm_a.drop(spm_a.columns[0], axis = 1, inplace= True)
    spm_b = pd.read_csv(os.path.join(workspace_b,'group_statistics','lcmodel_correction_%s_spm.csv'%workspace_b[-1]))
    spm_b.drop(spm_b.columns[0], axis = 1, inplace= True)

    fsl_a = pd.read_csv(os.path.join(workspace_a,'group_statistics','lcmodel_correction_%s_fsl.csv'%workspace_a[-1]))
    fsl_a.drop(fsl_a.columns[0], axis = 1, inplace= True)
    fsl_b = pd.read_csv(os.path.join(workspace_b,'group_statistics','lcmodel_correction_%s_fsl.csv'%workspace_b[-1]))
    fsl_b.drop(fsl_b.columns[0], axis = 1, inplace= True)

    fsu_a = pd.read_csv(os.path.join(workspace_a,'group_statistics','lcmodel_correction_%s_fsu.csv'%workspace_a[-1]))
    fsu_a.drop(fsu_a.columns[0], axis = 1, inplace= True)
    fsu_b = pd.read_csv(os.path.join(workspace_b,'group_statistics','lcmodel_correction_%s_fsu.csv'%workspace_b[-1]))
    fsu_b.drop(fsu_b.columns[0], axis = 1, inplace= True)

    # method to calcualte coefficient of variance between two dataframe columns ( CV = STDEV / MEAN)

    def calc_cv(df1,df2):
        # dump dataframe column values in numpy array
        arr1 = (np.array(df1))
        arr2 = (np.array(df2))

        #calculate pairwise CV and dump into empty list
        cv_arr = []
        for i in zip(arr1,arr2):
            cv     = 100 * (std(i) / mean(i))
            cv_arr.append(cv)

        return np.array(cv_arr)

    #calc cv's for lcm quantitation
    lcm_subjects   = [subject[0:4] for subject in lcm_a['Dataset']]
    lcm_cre_cv = calc_cv(lcm_a['Cre_Conc']      ,lcm_b['Cre_Conc'])
    lcm_cho_cv = calc_cv(lcm_a['GPC_PCh_Conc']  ,lcm_b['GPC_PCh_Conc'])
    lcm_naa_cv = calc_cv(lcm_a['NAA_NAAG_Conc'] ,lcm_b['NAA_NAAG_Conc'])
    lcm_ins_cv = calc_cv(lcm_a['mI_Conc']       ,lcm_b['mI_Conc'])
    lcm_glu_cv = calc_cv(lcm_a['Glu_Conc']      ,lcm_b['Glu_Conc'])
    lcm_gln_cv = calc_cv(lcm_a['Gln_Conc']      ,lcm_b['Gln_Conc'])
    lcm_glx_cv = calc_cv(lcm_a['Glu_Gln_Conc']  ,lcm_b['Glu_Gln_Conc'])

    column_order= ['Subjects','Cre', 'GPC+PCh','NAA+NAAG','mI','Glu','Gln','Glu+Gln']
    lcm_cv = pd.DataFrame({'Subjects'     :  lcm_subjects,
                           'Cre'          :  lcm_cre_cv          ,
                           'GPC+PCh'      :  lcm_cho_cv          ,
                           'NAA+NAAG'     :  lcm_naa_cv          ,
                           'mI'           :  lcm_ins_cv          ,
                           'Glu'          :  lcm_glu_cv          ,
                           'Gln'          :  lcm_gln_cv          ,
                           'Glu+Gln'      :  lcm_glx_cv           })
    lcm_cv = lcm_cv.reindex(columns=column_order)

    #calc cv's for spm  quantiation correction
    spm_cre_cv  = calc_cv(spm_a['Cre']      , spm_b['Cre'])
    spm_cho_cv  = calc_cv(spm_a['GPC+PCh']  , spm_b['GPC+PCh'])
    spm_naa_cv  = calc_cv(spm_a['NAA+NAAG'] , spm_b['NAA+NAAG'])
    spm_ins_cv  = calc_cv(spm_a['mI']       , spm_b['mI'])
    spm_glu_cv  = calc_cv(spm_a['Glu']      , spm_b['Glu'])
    spm_gln_cv  = calc_cv(spm_a['Gln']      , spm_b['Gln'])
    spm_glx_cv  = calc_cv(spm_a['Glu+Gln']  , spm_b['Glu+Gln'])

    spm_cv = pd.DataFrame({'Subjects'     :  lcm_subjects,
                           'Cre'          :  spm_cre_cv          ,
                           'GPC+PCh'      :  spm_cho_cv          ,
                           'NAA+NAAG'     :  spm_naa_cv          ,
                           'mI'           :  spm_ins_cv          ,
                           'Glu'          :  spm_glu_cv          ,
                           'Gln'          :  spm_gln_cv          ,
                           'Glu+Gln'      :  spm_glx_cv          ,})
    spm_cv = spm_cv.reindex(columns=column_order)

    #calc cv's for fsl quantiation correction
    fsl_cre_cv  = calc_cv(fsl_a['Cre']      , fsl_b['Cre'])
    fsl_cho_cv  = calc_cv(fsl_a['GPC+PCh']  , fsl_b['GPC+PCh'])
    fsl_naa_cv  = calc_cv(fsl_a['NAA+NAAG'] , fsl_b['NAA+NAAG'])
    fsl_ins_cv  = calc_cv(fsl_a['mI']       , fsl_b['mI'])
    fsl_glu_cv  = calc_cv(fsl_a['Glu']      , fsl_b['Glu'])
    fsl_gln_cv  = calc_cv(fsl_a['Gln']      , fsl_b['Gln'])
    fsl_glx_cv  = calc_cv(fsl_a['Glu+Gln']  , fsl_b['Glu+Gln'])

    fsl_cv = pd.DataFrame({'Subjects'     :  lcm_subjects,
                           'Cre'          :  fsl_cre_cv          ,
                           'GPC+PCh'      :  fsl_cho_cv          ,
                           'NAA+NAAG'     :  fsl_naa_cv          ,
                           'mI'           :  fsl_ins_cv          ,
                           'Glu'          :  fsl_glu_cv          ,
                           'Gln'          :  fsl_gln_cv          ,
                           'Glu+Gln'      :  fsl_glx_cv          ,})
    fsl_cv = fsl_cv.reindex(columns=column_order)

    #calc cv's for freesurfer quantiation correction
    fsu_cre_cv  = calc_cv(fsu_a['Cre']      , fsu_b['Cre'])
    fsu_cho_cv  = calc_cv(fsu_a['GPC+PCh']  , fsu_b['GPC+PCh'])
    fsu_naa_cv  = calc_cv(fsu_a['NAA+NAAG'] , fsu_b['NAA+NAAG'])
    fsu_ins_cv  = calc_cv(fsu_a['mI']       , fsu_b['mI'])
    fsu_glu_cv  = calc_cv(fsu_a['Glu']      , fsu_b['Glu'])
    fsu_gln_cv  = calc_cv(fsu_a['Gln']      , fsu_b['Gln'])
    fsu_glx_cv  = calc_cv(fsu_a['Glu+Gln']  , fsu_b['Glu+Gln'])

    fsu_cv = pd.DataFrame({'Subjects'     :  lcm_subjects,
                           'Cre'          :  fsu_cre_cv          ,
                           'GPC+PCh'      :  fsu_cho_cv          ,
                           'NAA+NAAG'     :  fsu_naa_cv          ,
                           'mI'           :  fsu_ins_cv          ,
                           'Glu'          :  fsu_glu_cv          ,
                           'Gln'          :  fsu_gln_cv          ,
                           'Glu+Gln'      :  fsu_glx_cv          ,})
    fsu_cv = fsu_cv.reindex(columns=column_order)



    return lcm_cv, spm_cv, fsl_cv, fsu_cv

