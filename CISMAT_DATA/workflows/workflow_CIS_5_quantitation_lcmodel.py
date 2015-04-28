__author__ = 'kanaan'

import os
import subprocess
__author__ = 'kanaan' '24.04.2015'

afs_dir        = '/xxx'
population_young_a = ['xxx']
workspace_a    = 'xxx'


CISMAT_dat = 'xxxx/cismat-svs-prob-all-2005-08-01.dat'

def get_cismat_data(frame, population, workspace_dir):
    import pandas as pd
    import os
    import errno

    df_all = pd.DataFrame.from_csv(frame, sep = '\s')

    # creat a dataframe and place reliable metabolite data for every subject
    reliable = df_all.loc[:, ['Dataset',
                              'Cre_Conc'     , 'Cre_pcSD',
                              'GPC_PCh_Conc' , 'GPC_PCh_pcSD',
                              'NAA_NAAG_Conc', 'NAA_NAAG_pcSD',
                              'mI_Conc'      , 'mI_pcSD',
                              'Glu_Conc'     , 'Glu_pcSD',
                              'Gln_Conc'     , 'Gln_pcSD',
                              'Glu_Gln_Conc' , 'Glu_Gln_pcSD'  ]]

    #get data from specific subjects list
    reliable = reliable.loc[reliable['Dataset'].isin(population)]


    #define output directory
    out_dir = os.path.join(workspace_dir, 'group_statistics')

    #create output directory
    try:
        os.makedirs(out_dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(out_dir):
            pass
        else: raise


    reliable.to_csv(os.path.join(out_dir, 'lcmodel_%s.csv'%workspace_dir[-1]))
    reliable.reindex()

    return reliable


if __name__ == "__main__":
    get_cismat_data(CISMAT_dat, populationxxx, workspace_xxx)


