import pandas as pd

def get_cov_stats(dfs_dir, samples, df, tool, preproc, seq_set_type, seq_set_name, mapping_postproc='mapped',
                  ext='.bb_stats'):
    dir_ev = dfs_dir + df + '/mapped/' + preproc + '/' + tool + '/' + seq_set_type + '/' + seq_set_name + '/' + mapping_postproc + '/'
    return load_cov_stats(samples, dir_ev, ext)


def load_cov_stats(samples, folder, ext, light=False):
    no_drop = ['#ID', "Length", "Ref_GC", "Avg_fold", 'Norm_fold', "Covered_percent", "Std_Dev"]
    exclude_main = ['Covered_bases', 'Read_GC', 'Plus_reads', 'Minus_reads', 'Median_fold']
    exclude_all = ['Length', 'Ref_GC', 'Covered_bases', 'Read_GC', 'Plus_reads', 'Minus_reads', 'Median_fold']
    if light:
        no_drop = ['#ID', "Length", "Ref_GC", "Avg_fold", 'Norm_fold', "Covered_percent"]
        exclude_main = ['Covered_bases', 'Read_GC', 'Plus_reads', 'Minus_reads', 'Median_fold', 'Std_Dev']
        exclude_all = ['Length', 'Ref_GC', 'Covered_bases', 'Read_GC', 'Plus_reads', 'Minus_reads', 'Median_fold',
                       'Std_Dev']
    dfs = []
    base = folder

    for i, s in enumerate(samples):
        fname = base + s + ext
        df = pd.read_csv(fname, sep='\t')
        df['Norm_fold'] = df['Avg_fold'] / (df['Plus_reads'] + df['Minus_reads'])
        if i == 0:
            df = df.drop(exclude_main, axis=1)
            df = df[no_drop]
            df = df.add_suffix('__' + s)
            df.rename(columns={'#ID__' + s: '#ID', 'Length__' + s: 'Length', 'Ref_GC__' + s: 'Ref_GC'}, inplace=True)
        else:
            df = df.drop(exclude_all, axis=1)
            df = df.add_suffix('__' + s)
            df.rename(columns={'#ID__' + s: '#ID'}, inplace=True)
        dfs.append(df)

    if len(dfs) > 1:
        merged = pd.merge(dfs[0], dfs[1], on='#ID', how='inner')
        for i, df in enumerate(dfs):
            if not ((i == 0) or (i == 1)):
                merged = pd.merge(merged, dfs[i], on='#ID', how='inner')
        return merged
    else:
        return dfs[0]


def load_coverage(samples, folder, ext='.bb_stats'):
    base = folder
    dfs = []
    for i, s in enumerate(samples):
        cov_file = base + s + ext
        cov_tf = pd.read_csv(cov_file, sep='\t', header=None, names=['seq', 'start', 'stop', 'cover'])
        dfs.append(cov_tf)
    return dfs