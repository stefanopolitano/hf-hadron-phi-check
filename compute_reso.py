#!/usr/bin/env python
import ROOT
from ROOT import gStyle
import pandas as pd
import numpy as np

from plot_utils import LoadGraphAndSyst, GetCanvas, GetLegend, GetCanvas3sub, SaveCanvas, SetGlobalStyle, SetObjectStyle


SetGlobalStyle(padleftmargin=0.16, padrightmargin=0.16, padbottommargin=0.14, padtopmargin=0.08,
               opttitle=1, titleoffsety=1.6, labelsize=0.05, titlesize=0.05,
               labeloffset=0.01, titleoffset=1.2, labelfont=42, titlefont=42)

# Alternative: RGB format
cols = [
    ROOT.kRed-4,
    ROOT.kAzure-2,
    ROOT.kOrange+1,
    ROOT.kSpring+2
]

def compute_reso(infile, ptmin, ptmax):
    # Load the DataFrame from a .parquet file
    # Replace 'data.parquet' with your actual file name if different.
    df = pd.read_parquet(infile)
    suffix = f'pt_{ptmin}_{ptmax}'
    #label = "3 < #it{p}_{T} < 5 GeV/#it{c}"
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.05)

    # Specify the column to use (change "data" if your column has a different name)
    data_col = "fImpactParameterXY"
    data_weight = "sgn_sweights"

    # Determine histogram parameters based on the data
    nphibins = 16
    phi_edges = np.linspace(0, 2 * np.pi, nphibins + 1)  # +1 to define bin edges correctly

    n_bins = 1600 
    xmin = -0.005
    xmax = 0.005

    # Draw results
    canvas = ROOT.TCanvas("canvas", "Gaussian Fit with Tail Correction", 1600, 1600)
    canvas.Divide(4, 4)

    hists, fits = [], []
    th2s = ROOT.TH2F(f"histsd", ";#varphi; #it{d^{0}}_{xy}", nphibins,
                     np.array(phi_edges,dtype=np.float64), 60, -0.015, 0.015)
    hmu = ROOT.TH1F("histmu", ";#varphi; #mu(#it{d^{0}_{xy}})", nphibins,
                    np.array(phi_edges, dtype=np.float64))
    hrms = ROOT.TH1F("histsigma", ";#varphi; #sigma(#it{d^{0}_{xy}})", nphibins,
                     np.array(phi_edges, dtype=np.float64))
    th2_mean = ROOT.TH1F(f"hist2dmean", ";#varphi; #it{d^{0}}_{xy}", nphibins,
                         np.array(phi_edges, dtype=np.float64))
    hreso = ROOT.TH1F("histreso", ";#varphi; #sigma(#it{d^{0}_{xy}})/#mu(#it{d^{0}_{xy}})", nphibins,
                      np.array(phi_edges, dtype=np.float64))
    SetObjectStyle(th2_mean, markerstyle=ROOT.kFullCircle, color=ROOT.kRed-4)

    for iphi in range(1, th2s.GetNbinsX()+1):
        phimin = phi_edges[iphi-1]
        phimax = phi_edges[iphi]
        hists.append(ROOT.TH1F(f"hist{iphi}", ";#it{d^{0}}_{xy};Entries", n_bins, -0.8, 0.8))

        # Fill the histogram with data from the specified column
        for _, (dca, phi, w) in enumerate(zip(df[data_col], df['fPhi'], df[data_weight])):
            if phi > phimin and phi < phimax:
                hists[-1].Fill(dca, w)
            if iphi-1 == 0:  th2s.Fill(phi, dca, w)

        if iphi-1 == 0:      
            for ibin in range(1, th2s.GetNbinsX()+1):
                hist_proj_dummy = th2s.ProjectionY(f'proj_{ibin}_mean_deltacent',
                                                        ibin,
                                                        ibin)
                th2_mean.SetBinContent(ibin, hist_proj_dummy.GetMean())
                th2_mean.SetBinError(ibin, 1.e-9)
            canv_dxy_phi, hframe = GetCanvas('canv_dxy_phi', ';#varphi; #it{d^{0}}_{xy}', ymin=-0.015, ymax=0.015, xmin=0, xmax=np.pi*2)
            hframe.GetYaxis().SetMaxDigits(1)
            th2s.Draw('COLZ same')
            th2_mean.Draw('hist pe same')
            latex.DrawLatexNDC(0.22, 0.8, suffix)
            SaveCanvas(canv_dxy_phi, f'{outdir}/canv_dxy_phi', suffix)

        # Define exclusion region (central region: -0.008 < x < 0.008)
        fits.append(ROOT.TF1("gaus_prefit", "gaus", xmin, xmax))
        fits[-1].SetParameters(hists[-1].GetMaximum(), hists[-1].GetMean(), hists[-1].GetRMS())
        SetObjectStyle(fits[-1], linecolor=ROOT.kRed-4)

        canvas.cd(iphi)
        latex.DrawLatexNDC(0.22, 0.80, f'{ptmin} < #it{{p}}_{{T}} < {ptmax} (GeV/{{c}})')
        hists[-1].GetXaxis().SetRangeUser(-0.02, 0.02)
        hists[-1].GetXaxis().SetNdivisions(505)
        hists[-1].GetYaxis().SetRangeUser(-0.02, hists[-1].GetMaximum()*1.6)
        hists[-1].Fit(fits[-1], 'R')    
        hists[-1].Draw('same')
        fits[-1].Draw('same')
        latex.DrawLatexNDC(0.22, 0.80, f'{phimin:.2f} < #varphi < {phimax:.2f}')
        latex.DrawLatexNDC(0.22, 0.74, f'#mu = {fits[-1].GetParameter(1):.8f} +-{fits[-1].GetParError(1):.8f}')
        latex.DrawLatexNDC(0.22, 0.68, f'#sigma = {fits[-1].GetParameter(2):.8f} +-{fits[-1].GetParError(2):.8f}')
        canvas.Update()

        hmu.SetBinContent(iphi, fits[-1].GetParameter(1))
        hrms.SetBinContent(iphi, fits[-1].GetParameter(2))
        hmu.SetBinError(iphi, fits[-1].GetParError(1))
        hrms.SetBinError(iphi, fits[-1].GetParError(2))
        canvas.cd(16)

        if phimax > 6: break
    
    SetObjectStyle(hrms, markerstyle=ROOT.kFullCircle, color=ROOT.kRed-4)
    hreso = hrms.Clone('hreso')
    hreso.Divide(hmu)
    hrms.GetYaxis().SetRangeUser(0.0018, 0.0024)
    hrms.GetYaxis().SetDecimals()
    hrms.GetYaxis().SetMaxDigits(2)
    hmu.GetYaxis().SetDecimals()
    hmu.GetYaxis().SetMaxDigits(2)

    outFile = ROOT.TFile(f'{outdir}/dxy_phi_{suffix}.root', 'recreate')
    canv_dxy_phi.Write()
    th2s.Write()
    th2_mean.Write()
    canvas.Write()
    for h in hists:
        h.Write()
    for f in fits:
        f.Write()
    hrms.Write()
    hmu.Write()
    hreso.Write()

    SaveCanvas(canvas, f'{outdir}/canv_sigma_dxy_phi', suffix)

    return hmu, hrms, hreso

if __name__ == "__main__":

    infiles = ['/home/stefano/Desktop/cernbox/checks/dmeson_phi/hf-hadron-phi-check/output_testPP_22Pass7/cent_0_100/pt_2_3/bkg_0_0.0300_sig_0.0000_1/df_sel.parquet',
               '/home/stefano/Desktop/cernbox/checks/dmeson_phi/hf-hadron-phi-check/output_testPP_22Pass7/cent_0_100/pt_3_5/bkg_0_0.0300_sig_0.0000_1/df_sel.parquet',
               '/home/stefano/Desktop/cernbox/checks/dmeson_phi/hf-hadron-phi-check/output_testPP_22Pass7/cent_0_100/pt_8_12/bkg_0_0.0300_sig_0.0000_1/df_sel.parquet'
               ]
    outdir = '/home/stefano/Desktop/cernbox/checks/dmeson_phi/hf-hadron-phi-check/d0xy_vs_phi'
    ptmins = [2, 3, 8]
    ptmaxs = [3, 5, 12]
    hmus, hrms, hresos = [], [], []

    creso = ROOT.TCanvas("creso", "", 1600, 600)
    creso.Divide(2, 1)
    leg = GetLegend(header='', xmax=0.5, ncolumns=1, ymin=0.7, ymax=0.85)
    for i, (infile, ptmin, ptmax) in enumerate(zip(infiles, ptmins, ptmaxs)):
        hmu, hrm, hreso = compute_reso(infile, ptmin, ptmax)
        hmus.append(hmu)
        hrms.append(hrm)
        hresos.append(hreso)
        SetObjectStyle(hmus[-1], markerstyle=ROOT.kFullCircle, color=cols[i])
        SetObjectStyle(hrms[-1], markerstyle=ROOT.kFullCircle, color=cols[i])
        SetObjectStyle(hresos[-1], markerstyle=ROOT.kFullCircle, color=cols[i])
        leg.AddEntry(hmus[-1], f'{ptmin} < #it{{p}}_{{T}} < {ptmax} (GeV/#it{{c}})', 'p')

    creso.cd(1)
    hmus[0].GetYaxis().SetRangeUser(-0.002, 0.002)
    hmus[0].GetYaxis().SetTitle('#mu(#it{d^{0}_{xy}})')
    for h in hmus:
        h.Draw('same')
    leg.Draw()
    creso.cd(2)
    hrms[0].GetYaxis().SetRangeUser(5.e-4, 32e-4)
    hrms[0].GetYaxis().SetTitle('#sigma(#it{d^{0}_{xy}})')
    for h in hrms:
        h.Draw('same')
    creso.Update()
    SaveCanvas(creso, f'{outdir}/dxy_vphi_vpt', '')

    input("Press Enter to exit...")