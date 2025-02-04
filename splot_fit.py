
import argparse
import sys
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # pylint: disable=wrong-import-position
import pandas as pd
import numpy as np
import uproot as up
import seaborn as sns
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
import itertools
from flarefly.data_handler import DataHandler
from flarefly.fitter import F2MassFitter
import yaml

def get_distribution(df, var):
    df = df[var]
    if "sgn_sweights" in df.columns:
        mean = np.average(df[var], weights=df['sgn_sweights'])
        sigma = np.sqrt(np.average((df[var] - mean)**2, weights=df['sgn_sweights']))
    else:
        print(f"Warning: sPlot weights not found in the dataframe. Using standard mean and sigma")
        mean = np.average(df[var])
        sigma = df[var].std()
    return mean, sigma

def plot_distribution(df, var):
    '''
    Plot the distribution of a variable applying the sPlot weights
    '''
    fig, ax = plt.subplots(figsize=(8, 6))
    if var == 'fPhi':
        # apply sPlot weights
        if "sgn_sweights" in df.columns:
            sgn_weights = df['sgn_sweights']
            df[var].hist(bins=100, weights=sgn_weights, alpha=0.5, density=True, range=(0, 2*np.pi), color='r', label='Signal')
            ax.set_xlabel(var)
            df[var].hist(bins=100, alpha=0.1, density=True, range=(0, 2*np.pi), color='b', label='Data')
        else:
            print(f"Warning: sPlot weights not found in the dataframe. Plotting data without weights")
            sns.histplot(df[var], bins=100, kde=True, ax=ax, color='b', label='Data')
    elif var == 'fImpactParameterXY':
        # apply sPlot weights
        if "sgn_sweights" in df.columns:
            sgn_weights = df['sgn_sweights']
            df[var].hist(bins=100, weights=sgn_weights, alpha=0.5, density=True, color='r', label='Signal')
            ax.set_xlabel(var)
            df[var].hist(bins=100, alpha=0.1, density=True, color='b', label='Data')
            # set log y
            ax.set_yscale('log')
            # set x range
            ax.set_xlim(-1, 1)
        else:
            print(f"Warning: sPlot weights not found in the dataframe. Plotting data without weights")
            sns.histplot(df[var], bins=100, kde=True, ax=ax, color='b', label='Data')
    ax.set_xlabel(var)
    ax.set_ylabel('Counts')
    ax.legend()
    return fig

def fit_mass(df, suffix, pt_min, pt_max, cfg, sub_dir):
    # Create the data handler
    data_handler = DataHandler(df, "fM")
    sgn_func = [cfg["fit_config"]["sgn_func"]] if cfg["fit_config"].get('sgn_func') else ["doublecb"]
    bkg_func = [cfg["fit_config"]["bkg_func"]] if cfg["fit_config"].get('bkg_func') else ["nobkg"]
    fitter_name = f"{sub_dir.split('/')[0]}_{suffix}_pt_{pt_min}_{pt_max}"
    

    fitter = F2MassFitter(data_handler, sgn_func, bkg_func, verbosity=0, name=fitter_name)
    fitter.set_signal_initpar(0, "mu", cfg["fit_config"]["mean"])
    fitter.set_signal_initpar(0, "sigma", cfg["fit_config"]["sigma"])
    fit_res = fitter.mass_zfit()
    sgn_sweights = fitter.get_sweights(sig_par_name=f'{fitter_name}_sgn', bkg_par_name=f'{fitter_name}_bkg')['signal']
    df.loc[:, 'sgn_sweights'] = sgn_sweights.astype(np.float32)
    
    out_dir_path = cfg['output']['dir'] + cfg['output']['suffix']
    with open(f"{out_dir_path}/failed_fits.txt", "a") as f:
        computed_sweights = True if sgn_sweights is not None else False
        f.write(
                f"{fitter_name}: fit_res.valid -> {fit_res.valid}, "
                f"fit_res.status -> {fit_res.status}, "
                f"fit_res.converged -> {fit_res.converged}, "
                f"sweights computed -> {computed_sweights} \n"
               )

    loc = ["lower left", "upper left"]
    ax_title = "phi (rad)"

    fig, _ = fitter.plot_mass_fit(
        style="ATLAS",
        show_extra_info = fitter._name_background_pdf_[0] != "nobkg" and fitter.get_background()[1] != 0,
        figsize=(8, 8), extra_info_loc=loc,
        axis_title=ax_title,
        logy=False
    )

    output_dir = os.path.join(out_dir_path, f'{sub_dir}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    fig.savefig(
        os.path.join(
            output_dir,
            f'mass_fit_{suffix}.png'
        ),
        dpi=300, bbox_inches="tight"
    )

    del fitter

def process(cfg_file_name):
    # Read the configuration file
    with open(cfg_file_name, 'r') as cfg_file:
        cfg = yaml.safe_load(cfg_file)

    pt_mins = cfg["pt_mins"]
    pt_maxs = cfg["pt_maxs"]
    cent_bins = cfg["cent_bins"]
    bdt_bkg_bins = cfg["bdt_bkg_bins"]
    bdt_sgn_bins = cfg["bdt_sgn_bins"]
    # if cfg["fit_config"].get("sgn_func") is None:
    if cfg['cuts'].get('key') is not None:
        cuts_mins = cfg['cuts']['bins_min']
        cuts_maxs = cfg['cuts']['bins_max']
    else:
        cuts_mins = [0 for _ in range(len(pt_mins))]
        cuts_maxs = [1 for _ in range(len(pt_mins))]

    # Read the input data
    data_df = up.open(cfg["inputs"]["data"])[cfg["inputs"]["fTreeDmeson"]].arrays(library="pd")
    print(f"Data file opened: {data_df.keys()}")

    # Create the file and write the first line
    out_dir_path = cfg['output']['dir'] + cfg['output']['suffix']
    if not os.path.exists(out_dir_path):
        os.makedirs(out_dir_path)
    with open(f"{out_dir_path}/failed_fits.txt", "w") as file:
        file.write("Failed fit configurations\n")

    for _, (cent_min, cent_max) in enumerate(zip(cent_bins[:-1], cent_bins[1:])):
        #selection = f'{cent_min} < fCentralityFT0C < {cent_max} and '
        selection = ''
        
        for _, (pt_min, pt_max, bkg_max, sig_min, cut_min, cut_max) in enumerate(zip(pt_mins,
                                                                                     pt_maxs,
                                                                                     bdt_bkg_bins,
                                                                                     bdt_sgn_bins,
                                                                                     cuts_mins,
                                                                                     cuts_maxs)):
            selection += f'0 < fMlScoreBkg < {bkg_max} and {sig_min} < fMlScoreNonPrompt < 1 and {pt_min} < fPt < {pt_max}'
            if cfg['cuts'].get('key') is not None:
                selection += f' and {cfg["cuts"]["key"]} > {cut_min} and {cfg["cuts"]["key"]} < {cut_max}'
            print(f"Selection: {selection}")
            out_dir = f"cent_{cent_min}_{cent_max}/pt_{pt_min:.0f}_{pt_max:.0f}/bkg_0_{bkg_max:.4f}_sig_{sig_min:.4f}_1"

            # apply selection
            df_sel = data_df.query(selection, inplace=False)
            
            # fit
            fit_mass(df_sel, selection, pt_min, pt_max, cfg, out_dir)

            # plot
            plot_distribution(df_sel, 'fPhi').savefig(
                os.path.join(out_dir_path, f'{out_dir}/phi_distribution.png')
            )
            plot_distribution(df_sel, 'fImpactParameterXY').savefig(
                os.path.join(out_dir_path, f'{out_dir}/impact_parameter_distribution.png')
            )
            selection = ''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Draw distributions')
    parser.add_argument('config_file', help='Path to the input configuration file')
    args = parser.parse_args()

    process(args.config_file)
