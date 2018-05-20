import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def get_data_for_plotly(samples):
    mp2_data_for_plotly = []

    return mp2_data_for_plotly


def read_mp2_data(samples, org='Bacteria', level='p__', norm_100=False):
    # k__Bacteria|p__Firmicutes|c__Clostridia
    data = []
    levels = ['k__', 'p__', 'c__', 'o__', 'f__', 'g__', 's__', 't__']
    throw_away = levels[levels.index(level) + 1]
    for s, loc in samples.items():
        # Load mp2 output as pandas table

        mp2 = pd.read_csv(loc, sep="\t")
        mp2['sample'] = s

        if norm_100:
            percent_of_org = mp2.loc[mp2['#SampleID'] == ('k__' + org)]['Metaphlan2_Analysis']
            # print(percent_of_org)
            norm = 1 / percent_of_org

            if (len(norm)) != 0:
                mp2['Metaphlan2_Analysis'] = pd.to_numeric(mp2['Metaphlan2_Analysis'], errors='coerce') * float(norm)
            # return mp2
        # Leave only desired level
        phyl = mp2.loc[~(mp2['#SampleID'].str.contains(throw_away))]
        phyl = phyl.loc[(phyl['#SampleID'].str.contains(level))]
        phyl = phyl.loc[(phyl['#SampleID'].str.contains(levels[0] + org))]

        # to wide format
        kk = pd.pivot_table(phyl, index='sample', columns=['#SampleID'])
        kk.columns = kk.columns.droplevel(0)
        kk = kk.reset_index()

        data.append(kk)
    return pd.concat(data, axis=0)