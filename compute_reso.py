#!/usr/bin/env python
import ROOT
from ROOT import gStyle
import pandas as pd
import numpy as np

from plot_utils import LoadGraphAndSyst, GetCanvas, GetLegend, GetCanvas3sub, SaveCanvas, SetGlobalStyle, SetObjectStyle


SetGlobalStyle(padleftmargin=0.16, padrightmargin=0.16, padbottommargin=0.14, padtopmargin=0.08,
               opttitle=1, titleoffsety=1.6, labelsize=0.05, titlesize=0.05,
               labeloffset=0.01, titleoffset=1.2, labelfont=42, titlefont=42)

# Load the DataFrame from a .parquet file
# Replace 'data.parquet' with your actual file name if different.
df = pd.read_parquet("/home/stefano/Desktop/cernbox/checks/dmeson_phi/hf-hadron-phi-check/output_testPP_22Pass7/cent_0_100/pt_3_5/bkg_0_0.0300_sig_0.0000_1/df_sel.parquet")
label = "3 < #it{p}_{T} < 5 GeV/#it{c}"
latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextSize(0.05)

# Specify the column to use (change "data" if your column has a different name)
data_col = "fImpactParameterXY"
data_weight = "sgn_sweights"

nphibins = 16
phi_edges = list(np.linspace(0, 2*np.pi, nphibins))

# Determine histogram parameters based on the data
data_min = df[data_col].min()
data_max = df[data_col].max()
n_bins = 1600  # You can adjust the number of bins if needed
xmin = -0.005
xmax = 0.005

# Draw results
canvas = ROOT.TCanvas("canvas", "Gaussian Fit with Tail Correction", 1600, 1600)
canvas.Divide(4, 4)

hrms = ROOT.TH1F("hist", ";#varphi; #sigma(#it{d^{0}_{xy}})", nphibins, 0, 2*np.pi)
hists, fits = [], []
th2s = []
th2_mean = []

for iphi, (phimin, phimax) in enumerate(zip(phi_edges[:-1], phi_edges[1:])):   
    hists.append(ROOT.TH1F(f"hist{iphi}", ";#it{d^{0}}_{xy};Entries", n_bins, -0.8, 0.8))
    th2s.append(ROOT.TH2F(f"hist{iphi}", ";#varphi; #it{d^{0}}_{xy}", 16, 0, 2*np.pi, 400, -0.1, 0.1))
    th2_mean.append(ROOT.TH1F(f"hist{iphi}", "Gaussian Fit Example;X values;Entries", 16, 0, 2*np.pi))
    SetObjectStyle(th2_mean[-1], markerstyle=ROOT.kFullCircle, color=ROOT.kRed-4)

    # Fill the histogram with data from the specified column
    for _, (dca, phi, w) in enumerate(zip(df[data_col], df['fPhi'], df[data_weight])):
        if phi > phimin and phi < phimax:
            hists[-1].Fill(dca, w)
        if iphi == 0:  th2s[-1].Fill(phi, dca, w)

    if iphi == 0:      
        for ibin in range(1, th2s[-1].GetNbinsX()+1):
            hist_proj_dummy = th2s[-1].ProjectionY(f'proj_{ibin}_mean_deltacent',
                                                    ibin,
                                                    ibin)
            th2_mean[-1].SetBinContent(ibin, hist_proj_dummy.GetMean())
            th2_mean[-1].SetBinError(ibin, hist_proj_dummy.GetRMS())
        canv_dxy_phi, hframe = GetCanvas('canv_dxy_phi', ';#varphi; #it{d^{0}}_{xy}', ymin=-0.015, ymax=0.015, xmin=0, xmax=np.pi*2)
        hframe.GetYaxis().SetMaxDigits(1)
        th2s[-1].Draw('COLZ same')
        th2_mean[-1].Draw('hist pe same')
        latex.DrawLatexNDC(0.22, 0.8, label)
        SaveCanvas(canv_dxy_phi, f'./canv_dxy_phi', '')

    # Define exclusion region (central region: -0.008 < x < 0.008)
    fits.append(ROOT.TF1("gaus_prefit", "gaus", xmin, xmax))
    fits[-1].SetParameters(hists[-1].GetMaximum(), hists[-1].GetMean(), hists[-1].GetRMS())
    SetObjectStyle(fits[-1], linecolor=ROOT.kRed-4)

    canvas.cd(iphi+1)
    hists[-1].GetXaxis().SetRangeUser(-0.02, 0.02)
    hists[-1].GetXaxis().SetNdivisions(505)
    hists[-1].GetYaxis().SetRangeUser(-0.02, hists[-1].GetMaximum()*1.6)
    hists[-1].Fit(fits[-1], 'R')    
    hists[-1].Draw('same')
    fits[-1].Draw('same')
    latex.DrawLatexNDC(0.22, 0.80, f'{phimin:.2f} < #varphi < {phimax:.2f}')
    latex.DrawLatexNDC(0.22, 0.74, f'#mu = {fits[-1].GetParameter(1):.4f} +-{fits[-1].GetParError(1):.4f}')
    latex.DrawLatexNDC(0.22, 0.68, f'#sigma = {fits[-1].GetParameter(2):.4f} +-{fits[-1].GetParError(2):.4f}')

    print("\nFinal Fit Results:")
    hrms.SetBinContent(iphi+1, fits[-1].GetParameter(2))
    hrms.SetBinError(iphi+1, fits[-1].GetParError(2))

canvas.cd(16)
SetObjectStyle(hrms, markerstyle=ROOT.kFullCircle, color=ROOT.kRed-4)
hrms.Draw()
hrms.GetYaxis().SetRangeUser(0.0018, 0.0024)
hrms.GetYaxis().SetDecimals()
hrms.GetYaxis().SetMaxDigits(2)

outFile = ROOT.TFile('dxy_phi.root', 'recreate')
canv_dxy_phi.Write()
th2s[-1].Write()
th2_mean[-1].Write()
canvas.Write()
for h in hists:
    h.Write()
for f in fits:
    f.Write()
hrms.Write()


SaveCanvas(canvas, f'./canv_sigma_dxy_phi', '')
input("Press Enter to exit...")