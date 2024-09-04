########
## Imports
########

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

# Enable LaTeX rendering in matplotlib
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

PLOTS_DIR: str = "plots"

BAREMETAL_ARRAY_FILE: str = "./baremetal-no-ssl_arrays.csv"
BAREMETAL_DF_FILE:    str = "./baremetal-no-ssl_dataframes.csv"
KUBE_ARRAY_FILE:      str = "./kube_arrays.csv"
KUBE_DF_FILE:         str = "./kube_dataframes.csv"


########
## Function definition
########
def plot_series(
        baremetal:    pd.DataFrame,
    kube:             pd.DataFrame,
        function:     str  = "",
        title:        str  = "",
        y_quantity:   str  = "rate_mean",
        std_col_name: str  = "rate_std",
        show_std:     bool = True,
        ideal_case:   bool = True,
        file_to_save: str  = ""
    ) -> None:
    """
    Plot the rate of a function in baremetal and kubernetes environments.

    Parameters
    ----------
    baremetal : pd.DataFrame
        Dataframe containing the baremetal data.
    kube : pd.DataFrame
        Dataframe containing the kubernetes data.
    function : str
        Name of the function to plot.
    title : str
        Title of the plot, if not provided, the function name will be used.
    y_quantity : str
        Column name of the quantity to plot.
    std_col_name : str
        Column name of the standard deviation.
    show_std : bool
        Whether to show the standard deviation.
    ideal_case : bool
        Whether to plot the ideal case.
    file_to_save : str
        Name of the file to save the plot. If not provided, the plot will be shown and not saved.

    Returns
    -------
    None
    """

    # Extract the number of cores once for all
    ncores_bm: np.ndarray = baremetal['n'].unique()
    ncores_k:  np.ndarray = kube['n'].unique()

    bm: np.ndarray = baremetal[baremetal['name'] == function][y_quantity].values
    k:  np.ndarray = kube[kube['name'] == function][y_quantity].values

    if show_std:
        b_std: np.ndarray = baremetal[baremetal['name'] == function][std_col_name].values
        k_std: np.ndarray = kube[kube['name'] == function][std_col_name].values

        bm_upper: np.ndarray = bm + b_std
        bm_lower: np.ndarray = bm - b_std
        k_upper:  np.ndarray = k + k_std
        k_lower:  np.ndarray = k - k_std

    if ideal_case:
        i: np.ndarray = bm[0] * (ncores_bm / ncores_bm[0])

    # Plot the data
    plt.figure(figsize=FIG_SIZE)

    plt.plot(ncores_bm, bm, label="baremetal", marker="s", color=COLORS[0])

    plt.plot(ncores_k, k, label="kubernetes", marker="D", color=COLORS[1])

    if show_std:
        plt.fill_between(ncores_bm, bm_lower, bm_upper, color=COLORS[0], alpha=ALPHA)
        plt.fill_between(ncores_k, k_lower, k_upper, color=COLORS[1], alpha=ALPHA)

    if ideal_case:
        plt.plot(ncores_bm, i, color=COLORS[2], linestyle="--", label="Ideal case")


    # Aesthetics settings
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


    plt.xlabel('Number of cores', fontsize = XLABEL_FONTSIZE, labelpad = XLABEL_PAD)
    plt.ylabel('Rate (Mb/s)', fontsize = YLABEL_FONTSIZE, labelpad = YLABEL_FONTSIZE)
    if not title:
        title = function
    plt.title(title, fontsize = TITLE_FONTSIZE, pad = TITLE_PAD)
    plt.legend(loc = 'best', fontsize = LEGEND_FONTSIZE, frameon = False)

    # Save or show the plot
    if file_to_save:
        plt.savefig(PLOTS_DIR + "/" + file_to_save)
        plt.close
    else:
     plt.show()


########
## Main
########

def main()->None:
    # Load the data
    baremetal_array: pd.DataFrame = pd.read_csv(BAREMETAL_ARRAY_FILE)
    baremetal_df:    pd.DataFrame = pd.read_csv(BAREMETAL_DF_FILE)
    kube_array:      pd.DataFrame = pd.read_csv(KUBE_ARRAY_FILE)
    kube_df:         pd.DataFrame = pd.read_csv(KUBE_DF_FILE)

    # Plot the data
    os.makedirs(PLOTS_DIR, exist_ok=True)

    # Array:
    plot_series(baremetal_array, kube_array, function="block-wise operation", title="Blockwise operation \\texttt{x +=1} (\\texttt{dask.map\\_block()})", file_to_save="array-block-wise-operation.pdf")
    plot_series(baremetal_array, kube_array, function="create random 2D-array", title="Randomly initialize a 2D-array", file_to_save="array-create-random-2D-array.pdf")
    plot_series(baremetal_array, kube_array, function="elementwise computation", title="Elementwise computation \\texttt{y = dask.sin(x)**2+dask.cos(x)**2}", file_to_save="array-elementwise-computation.pdf")
    plot_series(baremetal_array, kube_array, function="random access", title="Random access", file_to_save="array-random-access.pdf", ideal_case=False)
    plot_series(baremetal_array, kube_array, function="reduction (std) along axis", title="Reduction operation (std) row by row", file_to_save="array-reduction-std-along-axis.pdf")
    plot_series(baremetal_array, kube_array, function="reduction operation (std)", title="Reduction operation (std) for all the matrix entries", file_to_save="array-reduction-operation-std.pdf")
    plot_series(baremetal_array, kube_array, function="sum the transpose", title="Sum the transpose $B=A+A^T$", file_to_save="array-sum-the-transpose.pdf")

    # DataFrame:
    plot_series(baremetal_df, kube_df, function="block-wise operation", title="Block-wise operation \\texttt{x += 1}", file_to_save="df-block-wise-operation.pdf", ideal_case=True)
    plot_series(baremetal_df, kube_df, function="create random dataframe", title="Randomly initialize a \\texttt{dask.DataFrame}", file_to_save="df-create-random-dataframe.pdf", ideal_case=True)
    # plot_series(baremetal_df, kube_df, function="group-by apply operation", title="Group-by apply operation", file_to_save="df-group-by-apply-operation.pdf", ideal_case=False)
    plot_series(baremetal_df, kube_df, function="group-by operation", title="\\texttt{groupby('col_1').mean()} operation", file_to_save="df-group-by-operation.pdf", ideal_case=True)
    plot_series(baremetal_df, kube_df, function="group-by operation (2 columns)", title="\\texttt{groupby(['multiple','columns])} operation", file_to_save="df-group-by-operation-2-columns.pdf", ideal_case=True)
    plot_series(baremetal_df, kube_df, function="order data", title="Sort data", file_to_save="df-order-data.pdf", ideal_case=True)
    plot_series(baremetal_df, kube_df, function="random access", title="Random access", file_to_save="df-random-access.pdf", ideal_case=False)

    print(f"All plots saved in {PLOTS_DIR} directory.")

if __name__ == "__main__":
    main()
