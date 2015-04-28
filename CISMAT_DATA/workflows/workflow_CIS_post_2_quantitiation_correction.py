__author__ = 'kanaan' '27.04.2015'



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