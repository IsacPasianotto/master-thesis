########
## Imports
########

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple

# Enable LaTeX rendering in Matplotlib for text and labels
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

########
## Constants
########

# Colorblind-friendly palette
COLORS: list[str] = ['#648FFF', '#DC267F', '#FE6100', '#785EF0', '#FFB000']

XLABEL_FONTSIZE: int = 12
YLABEL_FONTSIZE: int = 12
XLABEL_PAD:      int = 5
YLABEL_PAD:      int = 10
TITLE_FONTSIZE:  int = 16
TITLE_PAD:       int = 10
LEGEND_FONTSIZE: int = 11
ALPHA:           float = 0.2
FIG_SIZE: Tuple[int, int] = (9, 6)

DATA_FILE: str = './processed_data_aggregated.csv'
PLOTS_DIR: str = 'plots'

########
## Plot function
########

def make_plot(
        data:         pd.DataFrame,
        title:        str,
        ylabel:       str,
        unit_y_label: str,
        file_to_save: str = "",
        statistics:   str = 'Mean',
        logscale:     bool = True,
        variances:    bool = False
    ) -> None:

    """
    Make a plot of the benchmark data contained in a given DataFrame.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the benchmark data.
    title : str
        Title of the plot.
    ylabel : str
        Label for the y-axis.
    unit_y_label : str
        Unit of the y-axis. It will be displayed in square brackets.
    file_to_save : str, optional
        Name of the file to save the plot. If not provided, the plot will be displayed.
    statistics : str, optional
        Statistics to plot. Default is 'Mean'.
    logscale : bool, optional
        If True, the plot will be displayed in log scale. Default is True.
    variances : bool, optional
        If True, the plot will include variance bands. Default is False.

    Returns
    -------
    None
    """
    # Extract sizes for x-axis
    sizes: np.ndarray = data['Size'].unique()

    baremetal: np.ndarray = data[data['CNI'] == 'baremetal'][statistics].values
    flannel:   np.ndarray = data[data['CNI'] == 'flannel'][statistics].values
    calico:    np.ndarray = data[data['CNI'] == 'calico'][statistics].values
    cilium:    np.ndarray = data[data['CNI'] == 'cilium'][statistics].values

    baremetal_std: np.ndarray = data[data['CNI'] == 'baremetal']['Std'].values
    flannel_std:   np.ndarray = data[data['CNI'] == 'flannel']['Std'].values
    calico_std:    np.ndarray = data[data['CNI'] == 'calico']['Std'].values
    cilium_std:    np.ndarray = data[data['CNI'] == 'cilium']['Std'].values

    baremetal_lower, baremetal_upper = baremetal - baremetal_std, baremetal + baremetal_std
    flannel_lower,   flannel_upper   = flannel - flannel_std, flannel + flannel_std
    calico_lower,    calico_upper    = calico  - calico_std, calico + calico_std
    cilium_lower,    cilium_upper    = cilium - cilium_std, cilium + cilium_std

    # Plotting
    plt.figure(figsize=FIG_SIZE)
    plt.plot(sizes, baremetal, label='baremetal', marker='o', color=COLORS[0])
    plt.plot(sizes, flannel, label='flannel', marker='s', color=COLORS[1])
    plt.plot(sizes, calico, label='calico', marker='^', color=COLORS[2])
    plt.plot(sizes, cilium, label='cilium', marker='D', color=COLORS[3])

    # Add variance bands if requested
    if variances:
        plt.fill_between(sizes, baremetal_lower, baremetal_upper, color=COLORS[0], alpha=ALPHA)
        plt.fill_between(sizes, flannel_lower, flannel_upper, color=COLORS[1], alpha=ALPHA)
        plt.fill_between(sizes, calico_lower, calico_upper, color=COLORS[2], alpha=ALPHA)
        plt.fill_between(sizes, cilium_lower, cilium_upper, color=COLORS[3], alpha=ALPHA)

    # Set logarithmic scale if requested
    if logscale:
        plt.yscale('log')
        plt.xscale('log')

    if logscale:
        plt.xlabel(r'$\log{\left(\# \textrm{ of texttt{MPI\_CHAR} sent}\right)}$', fontsize = XLABEL_FONTSIZE, labelpad = XLABEL_PAD)
        plt.ylabel(r'$\log{\left(\textrm{' + ylabel + r'}\right)}\quad\left[\log{\left(' + unit_y_label + r'\right)}\right]$', fontsize = YLABEL_FONTSIZE, labelpad = YLABEL_PAD)

    else:
        plt.xlabel(r'\# of \texttt{MPI\_CHAR} sent', fontsize = XLABEL_FONTSIZE, labelpad = XLABEL_PAD)
        plt.ylabel(ylabel + r'$\quad\left[' + unit_y_label + r'\right]$', fontsize = YLABEL_FONTSIZE, labelpad = YLABEL_PAD)


    # Access the current axes
    ax = plt.gca()
    # Hide the top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.minorticks_off()
    plt.title(title, fontsize=TITLE_FONTSIZE, pad= TITLE_PAD)
    plt.legend(loc ='best', fontsize=LEGEND_FONTSIZE, frameon=False)

    if file_to_save:
        plt.savefig(PLOTS_DIR + '/' + file_to_save)
        plt.close()
    else:
        # no file to save, show it
        plt.show()

########
## Main
########

def main():

    # -- Load data --
    data: pd.DataFrame = pd.read_csv(DATA_FILE)

    # -- Latency --
    latency:       pd.DataFrame = data[data['Benchmark'] == 'latency']
    latency_mp:    pd.DataFrame = data[data['Benchmark'] == 'latency_mp']
    multi_latency: pd.DataFrame = data[data['Benchmark'] == 'multi-latency']

    latency_1:       pd.DataFrame = latency[latency['Nodes'] == 1]
    latency_2:       pd.DataFrame = latency[latency['Nodes'] == 2]
    latency_mp_1:    pd.DataFrame = latency_mp[latency_mp['Nodes'] == 1]
    latency_mp_2:    pd.DataFrame = latency_mp[latency_mp['Nodes'] == 2]
    multi_latency_1: pd.DataFrame = multi_latency[multi_latency['Nodes'] == 1]
    multi_latency_2: pd.DataFrame = multi_latency[multi_latency['Nodes'] == 2]

    # -- Bandwidth --
    bw:     pd.DataFrame = data[data['Benchmark'] == 'bw']
    bibw:   pd.DataFrame = data[data['Benchmark'] == 'bibw']
    mbw_mr: pd.DataFrame = data[data['Benchmark'] == 'mbw_mr']

    bw_1:       pd.DataFrame = bw[bw['Nodes'] == 1]
    bw_2:       pd.DataFrame = bw[bw['Nodes'] == 2]
    bibw_1:     pd.DataFrame = bibw[bibw['Nodes'] == 1]
    bibw_2:     pd.DataFrame = bibw[bibw['Nodes'] == 2]
    mbw_mr_1:   pd.DataFrame = mbw_mr[mbw_mr['Nodes'] == 1]
    mbw_mr_2:   pd.DataFrame = mbw_mr[mbw_mr['Nodes'] == 2]

    # -- Make plots --
    os.makedirs(PLOTS_DIR, exist_ok=True)

    make_plot(latency_1, '\\texttt{osu_latency} -- Pods on the same node', ylabel='Latency', unit_y_label = r'\mu s', file_to_save = 'latency-1-node.pdf', logscale=True)
    make_plot(latency_2, '\\texttt{osu_latency} -- Pods on 2 different nodes', ylabel='Latency', unit_y_label = r'\mu s', file_to_save = 'latency-2-nodes.pdf', logscale=True)
    make_plot(latency_mp_1, '\\texttt{osu_latency} -- Pods on the same node', ylabel='Latency', unit_y_label = r'\mu s', file_to_save = 'latency_mp-1-node.pdf', logscale=True)
    make_plot(latency_mp_2, '\\texttt{osu_latency} -- Pods on 2 different nodes', ylabel='Latency', unit_y_label = r'\mu s', file_to_save = 'latency_mp-2-nodes.pdf', logscale=True)
    make_plot(multi_latency_1, '\\texttt{osu_multi_lat} -- Pods on the same node', ylabel='Latency', unit_y_label = r'\mu s', file_to_save = 'multi-latency-1-node.pdf', logscale=True)
    make_plot(multi_latency_2, '\\texttt{osu_multi_lat} -- Pods on 2 different nodes', ylabel='Latency', unit_y_label = r'\mu s', file_to_save = 'multi-latency-2-nodes.pdf', logscale=True)

    make_plot(bw_1, '\\texttt{osu_bw} -- Pods on the same node', ylabel='Bandwidth', unit_y_label = r'MB/s', file_to_save = 'bw-1-node.pdf', logscale=True)
    make_plot(bw_2, '\\texttt{osu_bw} -- Pods on 2 different nodes', ylabel='Bandwidth', unit_y_label = r'MB/s', file_to_save = 'bw-2-nodes.pdf', logscale=True)
    make_plot(bibw_1, '\\texttt{osu_bibw} -- Pods on the same node', ylabel='Bandwidth', unit_y_label = r'MB/s', file_to_save = 'bibw-1-node.pdf', logscale=True)
    make_plot(bibw_2, '\\texttt{osu_bibw} -- Pods on 2 different nodes', ylabel='Bandwidth', unit_y_label = r'MB/s', file_to_save = 'bibw-2-nodes.pdf', logscale=True)
    make_plot(mbw_mr_1, '\\texttt{osu_mbw_mr} -- Pods on the same node', ylabel='Bandwidth', unit_y_label = r'MB/s', file_to_save = 'mbw_mr-1-node.pdf', logscale=True)
    make_plot(mbw_mr_2, '\\texttt{osu_mbw_mr} -- Pods on 2 different nodes', ylabel='Bandwidth', unit_y_label = r'MB/s', file_to_save = 'mbw_mr-2-nodes.pdf', logscale=True)

    print('Plots saved in the' + PLOTS_DIR + ' directory.')

if __name__ == '__main__':
    main()
