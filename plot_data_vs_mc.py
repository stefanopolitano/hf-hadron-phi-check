import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

input_data = ['/home/stefano/Desktop/cernbox/checks/dmeson_phi/hf-hadron-phi-check/output_testPP_22Pass7/cent_0_100/pt_2_3/bkg_0_0.0300_sig_0.0000_1/df_sel.parquet',
              '/home/stefano/Desktop/cernbox/checks/dmeson_phi/hf-hadron-phi-check/output_testPP_22Pass7/cent_0_100/pt_3_5/bkg_0_0.0300_sig_0.0000_1/df_sel.parquet',
              '/home/stefano/Desktop/cernbox/checks/dmeson_phi/hf-hadron-phi-check/output_testPP_22Pass7/cent_0_100/pt_8_12/bkg_0_0.0300_sig_0.0000_1/df_sel.parquet',
              ]
input_mc = ['/home/stefano/Desktop/cernbox/checks/dmeson_phi/download/pt2_3/Prompt_pT_2_3_ModelApplied.parquet.gzip',
            '/home/stefano/Desktop/cernbox/checks/dmeson_phi/download/pt3_5/Prompt_pT_3_5_ModelApplied.parquet.gzip',
            '/home/stefano/Desktop/cernbox/checks/dmeson_phi/download/pt8_12/Prompt_pT_8_12_ModelApplied.parquet.gzip']

sels = ['ML_output_Bkg < 0.03', 'ML_output_Bkg < 0.03', 'ML_output_Bkg < 0.03']
labels = ['pt_2_3', 'pt3_5', 'pt8_12']

for idf, (data, mc, sel, label) in enumerate(zip(input_data, input_mc, sels, labels)):
    
    df_data = pd.read_parquet(data, engine='pyarrow')
    df_mc = pd.read_parquet(mc, engine='pyarrow')
    df_mc_sel = df_mc.query(sel, inplace=False)
    
    fig, ax = plt.subplots(figsize=(8, 6))

    sgn_weights = df_data['sgn_sweights']
    df_data['fPhi'].hist(bins=100, weights=sgn_weights, alpha=0.5, density=True, range=(0, 2*np.pi), color='r', label='Data (sPlot)')
    ax.set_xlabel('fPhi')
    df_mc_sel['fPhi'].hist(bins=100, alpha=0.1, density=True, range=(0, 2*np.pi), color='b', label='MC (Prompt)')

    ax.set_xlabel('fPhi')
    ax.set_ylabel('Counts')
    ax.legend()

    fig.savefig(f'./phi_data_vs_mc_{label}.png')


    