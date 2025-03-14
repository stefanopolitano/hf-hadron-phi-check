import ROOT
from ROOT import gStyle, gROOT
import pandas as pd
from scipy.interpolate import InterpolatedUnivariateSpline

#_________________________________________________________________________________________________________________________________________
# Utility functions
def SetGlobalStyle(**kwargs):
    '''
    Method to set global style.

    Parameters
    ----------

    - padrightmargin (float), default = 0.035
    - padleftmargin (float), default = 0.12
    - padtopmargin (float), default = 0.035
    - padbottommargin (float), default = 0.1

    - titlesize (float), default = 0.050
    - titlesizex (float), default = 0.050
    - titlesizey (float), default = 0.050
    - titlesizez (float), default = 0.050

    - labelsize (float), default = 0.045
    - labelsizex (float), default = 0.045
    - labelsizey (float), default = 0.045
    - labelsizez (float), default = 0.045

    - titleoffset (float), default = 1.2
    - titleoffsetx (float), default = 1.2
    - titleoffsey (float), default = 1.2
    - titleoffsetz (float), default = 1.2

    - opttitle (int), default = 0
    - optstat (int), default = 0

    - padtickx (int), default = 1
    - padticky (int), default = 1

    - maxdigits (int), default no max value

    - palette (int), default kBird
    '''

    # pad margins
    if 'padrightmargin' in kwargs:
        gStyle.SetPadRightMargin(kwargs['padrightmargin'])
    else:
        gStyle.SetPadRightMargin(0.035)

    if 'padleftmargin' in kwargs:
        gStyle.SetPadLeftMargin(kwargs['padleftmargin'])
    else:
        gStyle.SetPadLeftMargin(0.12)

    if 'padtopmargin' in kwargs:
        gStyle.SetPadTopMargin(kwargs['padtopmargin'])
    else:
        gStyle.SetPadTopMargin(0.035)

    if 'padbottommargin' in kwargs:
        gStyle.SetPadBottomMargin(kwargs['padbottommargin'])
    else:
        gStyle.SetPadBottomMargin(0.1)

    # title sizes
    if 'titlesize' in kwargs:
        gStyle.SetTitleSize(kwargs['titlesize'], 'xyz')
    else:
        gStyle.SetTitleSize(0.050, 'xyz')

    if 'titlesizex' in kwargs:
        gStyle.SetTitleSize(kwargs['titlesizex'], 'x')
    if 'titlesizey' in kwargs:
        gStyle.SetTitleSize(kwargs['titlesizex'], 'y')
    if 'titlesizez' in kwargs:
        gStyle.SetTitleSize(kwargs['titlesizex'], 'z')

    # label sizes
    if 'labelsize' in kwargs:
        gStyle.SetLabelSize(kwargs['labelsize'], 'xyz')
    else:
        gStyle.SetLabelSize(0.045, 'xyz')

    if 'labelsizex' in kwargs:
        gStyle.SetLabelSize(kwargs['labelsizex'], 'x')
    if 'labelsizey' in kwargs:
        gStyle.SetLabelSize(kwargs['labelsizey'], 'y')
    if 'labelsizez' in kwargs:
        gStyle.SetLabelSize(kwargs['labelsizez'], 'z')

    # title offsets
    if 'titleoffset' in kwargs:
        gStyle.SetTitleOffset(kwargs['titleoffset'], 'xyz')
    else:
        gStyle.SetTitleOffset(1.2, 'xyz')

    if 'titleoffsetx' in kwargs:
        gStyle.SetTitleOffset(kwargs['titleoffsetx'], 'x')
    if 'titleoffsety' in kwargs:
        gStyle.SetTitleOffset(kwargs['titleoffsety'], 'y')
    if 'titleoffsetz' in kwargs:
        gStyle.SetTitleOffset(kwargs['titleoffsetz'], 'z')

    # other options
    if 'opttitle' in kwargs:
        gStyle.SetOptTitle(kwargs['opttitle'])
    else:
        gStyle.SetOptTitle(0)

    if 'optstat' in kwargs:
        gStyle.SetOptStat(kwargs['optstat'])
    else:
        gStyle.SetOptStat(0)

    if 'padtickx' in kwargs:
        gStyle.SetPadTickX(kwargs['padtickx'])
    else:
        gStyle.SetPadTickX(1)

    if 'padticky' in kwargs:
        gStyle.SetPadTickY(kwargs['padticky'])
    else:
        gStyle.SetPadTickY(1)

    gStyle.SetLegendBorderSize(0)

    if 'maxdigits' in kwargs:
        TGaxis.SetMaxDigits(kwargs['maxdigits'])

    if 'palette' in kwargs:
        gStyle.SetPalette(kwargs['palette'])

    gROOT.ForceStyle()

def SetObjectStyle(obj, **kwargs):
    '''
    Method to set root object style.

    Parameters
    ----------

    - obj: object to set style

    - linecolor (int) default 1 (black)
    - linealpha (float) default 1
    - linewidth (int) default 2
    - linestyle (int) default 1

    - markercolor (int) default 1 (black)
    - markeralpha (float) default 1
    - markerstyle (int) default 20 (full circle)
    - markersize (int) default 20 (full circle)

    - fillcolor (int) default no filling
    - fillalpha (float) default 1
    - fillstyle (int) default 0 (no style)

    - color (int) sets same color for line, marker and fill
    - alpha (float) sets same alpha for line, marker and fill
    '''

    # alpha parameters
    lalpha = kwargs.get('linealpha', 1)
    malpha = kwargs.get('markeralpha', 1)
    falpha = kwargs.get('fillalpha', 1)
    if 'alpha' in kwargs:
        lalpha = kwargs['alpha']
        malpha = kwargs['alpha']
        falpha = kwargs['alpha']
    if 'linealpha' in kwargs:
        lalpha = kwargs['linealpha']
    if 'markeralpha' in kwargs:
        malpha = kwargs['markeralpha']
    if 'fillalpha' in kwargs:
        falpha = kwargs['fillalpha']

    # line styles
    if 'linecolor' in kwargs:
        if lalpha < 1:
            obj.SetLineColorAlpha(kwargs['linecolor'], lalpha)
        else:
            obj.SetLineColor(kwargs['linecolor'])
    else:
        if lalpha < 1:
            obj.SetLineColorAlpha(1, lalpha)
        else:
            obj.SetLineColor(1)

    if 'linewidth' in kwargs:
        obj.SetLineWidth(kwargs['linewidth'])
    else:
        obj.SetLineWidth(2)

    if 'linestyle' in kwargs:
        obj.SetLineStyle(kwargs['linestyle'])
    else:
        obj.SetLineStyle(1)

    # marker styles
    if 'markercolor' in kwargs:
        if malpha < 1:
            obj.SetMarkerColorAlpha(kwargs['markercolor'], malpha)
        else:
            obj.SetMarkerColor(kwargs['markercolor'])
    else:
        if malpha < 1:
            obj.SetMarkerColorAlpha(1, malpha)
        else:
            obj.SetMarkerColor(1)

    if 'markersize' in kwargs:
        obj.SetMarkerSize(kwargs['markersize'])
    else:
        obj.SetMarkerSize(1)

    if 'markerstyle' in kwargs:
        obj.SetMarkerStyle(kwargs['markerstyle'])
    else:
        obj.SetMarkerStyle(20)

    # fill styles
    if 'fillcolor' in kwargs:
        if falpha < 1:
            obj.SetFillColorAlpha(kwargs['fillcolor'], falpha)
        else:
            obj.SetFillColor(kwargs['fillcolor'])

    if 'fillstyle' in kwargs:
        obj.SetFillStyle(kwargs['fillstyle'])

    #global color
    if 'color' in kwargs:
        if lalpha < 1:
            obj.SetLineColorAlpha(kwargs['color'], lalpha)
        else:
            obj.SetLineColor(kwargs['color'])
        if malpha < 1:
            obj.SetMarkerColorAlpha(kwargs['color'], malpha)
        else:
            obj.SetMarkerColor(kwargs['color'])
        if falpha < 1:
            obj.SetFillColorAlpha(kwargs['color'], falpha)
        else:
            obj.SetFillColor(kwargs['color'])

def PlotEmptyClone(graph, leg, msize):
    """
    Creates an empty clone of a graph with adjusted marker style for legend entry.
    
    Args:
        graph (ROOT.TGraph): The input graph.
        leg (ROOT.TLegend): Legend to add the entry to.
        msize (float): Marker size.
    """
    clone = graph.Clone(graph.GetName() + '_clone')

    # Map filled markers to empty equivalents
    marker_map = {
        33: 27, 34: 28, 20: 24, 21: 25, 
        29: 30, 47: 46, 43: 42, 45: 44
    }
    mstyle = marker_map.get(graph.GetMarkerStyle(), graph.GetMarkerStyle())

    SetObjectStyle(clone, markercolor=ROOT.kBlack, markersize=msize, linewidth=0, markerstyle=mstyle)

    if leg:
        leg.AddEntry(clone, ' ', 'p')
    
    clone.Draw('PZ same')

def GetCanvas(name, axisname, xmin=0.4, xmax=40, ymin=-0.20, ymax=0.62):
    """
    Creates a ROOT canvas with a log-x scale and formatted frame.
    
    Args:
        name (str): Name of the canvas.
    
    Returns:
        tuple: (canvas, frame)
    """
    canv = ROOT.TCanvas(name, name, 800, 800)
    
    hframe = canv.DrawFrame(xmin, ymin, xmax, ymax, axisname)
    hframe.GetYaxis().SetDecimals()
    hframe.GetYaxis().SetTitleOffset(1.6)
    hframe.GetXaxis().SetMoreLogLabels()

    return canv, hframe

def GetCanvas3sub(name, axisname):
    """
    Creates a canvas with three adjacent subpads sharing the y-axis.
    
    Args:
        name (str): Name of the canvas.
    
    Returns:
        tuple: (canvas, frames)
    """
    canvas = ROOT.TCanvas(name, name, 1600, 600)
    canvas.Divide(3, 1, 0, 0)  # Remove spacing between pads

    frames = []
    for i in range(3):
        canvas.cd(i + 1)
        pad = ROOT.gPad
        pad.SetLeftMargin(0.18 if i == 0 else 0.0)  # First pad has a y-axis margin
        pad.SetRightMargin(0.05 if i == 2 else 0.0) # Last pad has right margin
        
        frame = pad.DrawFrame(-0.5, -0.20, 40, 0.62, axisname)
        frame.SetTitle("")
        
        if i > 0:
            frame.GetYaxis().SetLabelSize(0)
            frame.GetYaxis().SetTickLength(0.040)
            frame.GetXaxis().SetTickLength(0.025)
        else:
            frame.GetYaxis().SetTitleSize(0.05)
            frame.GetYaxis().SetTitleOffset(1.6)
            frame.GetYaxis().SetDecimals()

        frames.append(frame)

    return canvas, frames

def GetCanvas2sub(name, xmins, xmaxs, ymins_mass, ymaxs_mass, ymins_v2, ymaxs_v2, axisnametop, axisnamebottom):
    """
    Creates a canvas with two adjacent subpads (one for mass on top, one for v2 on bottom), 
    sharing the x-axis while maintaining different y-axis ranges.

    Args:
        name (str): Name of the canvas.
        xmins (float): Minimum x-axis value (common for both pads).
        xmaxs (float): Maximum x-axis value (common for both pads).
        ymins_mass (float): Minimum y-axis value for the mass panel.
        ymaxs_mass (float): Maximum y-axis value for the mass panel.
        ymins_v2 (float): Minimum y-axis value for the v2 panel.
        ymaxs_v2 (float): Maximum y-axis value for the v2 panel.
        axisnametop (str): Y-axis title for the mass plot.
        axisnamebottom (str): Y-axis title for the v2 plot.

    Returns:
        tuple: (canvas, frames)
    """
    # Create canvas with 2 rows (top = mass, bottom = v2)
    canvas = ROOT.TCanvas(name, name, 600, 900)  
    canvas.Divide(1, 2, 0, 0.0)  # Small spacing between top and bottom

    frames = []
    for i in range(2):
        canvas.cd(i + 1)
        pad = ROOT.gPad
        pad.SetBottomMargin(0.18 if i == 1 else 0.0)  # Bottom pad has more space for x-axis
        pad.SetTopMargin(0.02 if i == 0 else 0.0)  # Top pad has less space
        pad.SetRightMargin(0.02)

        # Set the correct y-axis range for each pad
        if i == 0:  # Mass plot (top)
            frame = pad.DrawFrame(xmins, ymins_mass, xmaxs, ymaxs_mass, axisnametop)
        else:  # v2 plot (bottom)
            frame = pad.DrawFrame(xmins, ymins_v2, xmaxs, ymaxs_v2, axisnamebottom)

        frame.SetTitle("")

        if i == 0:  # Hide x-axis labels on the top pad
            frame.GetXaxis().SetLabelSize(0)
        else:  # Show x-axis on the bottom pad
            frame.GetXaxis().SetTitleSize(0.05)

        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.6)
        frame.GetYaxis().SetDecimals()

        frames.append(frame)

    return canvas, frames

def GetLegend(xmin=0.19, ymin=0.62, xmax=0.75, ymax=0.77, textsize=0.04, ncolumns=2, header=' ', fillstyle=0):
    """
    Creates a formatted legend.
    
    Args:
        xmin, ymin, xmax, ymax (float): Legend position.
        textsize (float): Text size in legend.
        ncolumns (int): Number of columns in legend.
        header (str): Header text for legend.
        fillstyle (int): Fill style.
    
    Returns:
        ROOT.TLegend: Configured legend.
    """
    leg = ROOT.TLegend(xmin, ymin, xmax, ymax)
    leg.SetTextSize(textsize)
    leg.SetNColumns(ncolumns)
    leg.SetFillStyle(fillstyle)
    leg.SetHeader(header)
    return leg

def SystX(graph, syst, percentage=0.2):
    for i in range(graph.GetN()):
        stat = 2*graph.GetErrorXlow(i)
        syst.SetPointEXlow(i, stat*percentage)
        syst.SetPointEXhigh(i, stat*percentage)
    return syst

def LoadGraphAndSyst(path_to_file, graph_name, syst_name, syst_fd, color, marker, markersize=2):
    """
    Loads graph and systematic uncertainties from a ROOT file.
    
    Args:
        path_to_file (str): Path to ROOT file.
        graph_name (str): Name of the graph.
        syst_name (str): Name of systematic uncertainty graph.
        syst_fd (str): Additional systematic uncertainty graph.
        color (int): Color of the graph.
        marker (int): Marker style.
        markersize (float): Marker size.
    
    Returns:
        tuple: (graph, syst, syst_fd) if both systematic uncertainties are provided,
               (graph, syst) if only one is provided, or (graph) otherwise.
    """
    infile = ROOT.TFile.Open(path_to_file)
    graph = infile.Get(graph_name)
    SetObjectStyle(graph, markerstyle=marker, markercolor=color, markersize=markersize, linecolor=color, linewidth=2)

    if syst_name:
        gsyst = infile.Get(syst_name)
        SetObjectStyle(gsyst, markerstyle=marker, markercolor=color, markersize=markersize, linecolor=color, linewidth=2, fillalpha=0, fillstyle=0)
        gsyst = SystX(graph, gsyst)

        if syst_fd:
            gsyst_fd = infile.Get(syst_fd)
            SetObjectStyle(gsyst_fd, markerstyle=marker, markercolor=color, markersize=markersize, linecolor=color, linewidth=1, fillcolor=color, fillalpha=0.4, fillstyle=1000)
            gsyst_fd = SystX(graph, gsyst_fd, 0.1)
            return graph, gsyst, gsyst_fd

        return graph, gsyst
    return graph

def DrawStatSystEmpty(graph, gsyst, gfd, leg, markersize=2):
    gsyst.Draw('5 same')
    if gfd:
        gfd.Draw('5 same')
    graph.Draw('PZ same')
    PlotEmptyClone(graph, leg, markersize)

def SaveCanvas(canv, title, suffix='', formats=('pdf', 'png')):
    """
    Saves canvas in multiple formats.
    
    Args:
        canv (ROOT.TCanvas): Canvas to save.
        title (str): Output file name.
        suffix (str): Additional suffix.
        formats (tuple): File formats.
    """
    for form in formats:
        canv.SaveAs(f'{title}{suffix}.{form}')
