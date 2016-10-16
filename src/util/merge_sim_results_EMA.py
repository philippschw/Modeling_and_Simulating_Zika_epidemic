import sys
sys.path
sys.path.append('/home/philipp/Dropbox/Workspace_Zika_Models_Philipp/src')
del sys

from ema_workbench.util import merge_results, load_results, save_results

filename = 'EMA108_vFinal_FullRUNLaptop'
results2 = load_results(r'simulation_results/'+filename+'.tar.gz')

filename = 'EMA324_vFinal_FullRUN_12core'
results1 = load_results(r'simulation_results/'+filename+'.tar.gz')

merged =  merge_results(results1, results2, downsample=None)
print ('merge_1_successful')

results2, results1 = None, None

filename = 'EMA108_vFinal_FullRUN_hometv'
results3 = load_results(r'simulation_results/'+filename+'.tar.gz')
merged =  merge_results(merged, results3, downsample=None)
print ('merge_1_successful')

experiments, outcomes = merged

import pandas as pd
for key, value in outcomes.iteritems():
    outcomes[key] = pd.DataFrame.from_dict(value)
experiments =  pd.DataFrame.from_dict(experiments)
experiments.dropna(axis=0, inplace=True)
for key, value in outcomes.iteritems():
    value.dropna(axis=0, inplace=True)
    
print ('nr of experiments: ', len(experiments), '   nr of outcomes: ', len(outcomes['6_exposed']))

saved_exp = experiments.to_dict()
saved_out = {}
for key, value in outcomes.iteritems():
    saved_out[key] = value.to_dict()

saved_results = saved_exp, saved_out

save_results(saved_results, r'simulation_results/FULLRUN_merged_cleaned.tar.gz')

print ('END!')


