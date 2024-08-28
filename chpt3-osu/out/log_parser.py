########
## Imports
########
import os
import sys
import csv
import pandas as pd


########
## Function definition
########

def log_parser(
        input_file:    str,
        n_val_per_col: int = 2
    ) -> list[list[int, float, str, int, str]]:
    """
    Parse the log file given in input and return a list of lists containing the
    data in that file.

    Parameters:
    -----------
    input_file: str
        The path to the log file to parse.
    n_val_per_col: int
        The number of column the OSU file generates in the output. Default value is 2.

    Returns:
    --------
    data: list[list[int, float, str, int, str]]
        A list of lists containing the data in the log
    """
    data: list[list[int, float, str, int, str]] = []

    bench_name: str = input_file.split(".")[0]
    n_nodes:    str = '1' if '1' in bench_name else '2'
    situation:  str = bench_name.split(n_nodes)[0][:-1]   # -1 to remove final "-"
    bench:      str = bench_name.split(n_nodes)[1]
    bench = bench[7:] if n_nodes == "2" else bench[6:]     # "-nodes-" -> 7 characters, "-node-" -> 6

    try:
        with open(input_file, 'r') as file:
            for line in file:
                values = line.split()
                if len(values) != n_val_per_col:
                    continue
                if n_val_per_col == 3 and values[0] == '#':
                    continue
                data.append([int(values[0]), float(values[1]), situation, int(n_nodes), bench])
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

    return data

def generate_csv(
        todo: list[str],
        out_file_name: str
    ) -> None:
    """
    Generate the CSV file containing the data from the log files.
    For each file generated in the todo list it call the log_parser function and
    appends the result to the CSV file.
    """
    with open(out_file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Size', 'Measure', 'CNI', 'Nodes', 'Benchmark'])

    for f in todo:
        n_val: int = 3 if 'mbw_mr' in f else 2
        data: list[list[int, float, int, str, str]] = log_parser(f, n_val)

        with open(out_file_name, 'a') as csvfile:
            csv_writer = csv.writer(csvfile)
            for Size, Measure, CNI, Nodes, Benchmark in data:
                csv_writer.writerow([Size, Measure, CNI, Nodes, Benchmark])


########
## Main function
########

def main():
    """
    Main function of the script.
    """

    all_txt_files: list[str] = [file for file in os.listdir(os.getcwd()) if file.endswith(".txt")]
    processed_out_file_name: str = "processed_data.csv"
    generate_csv(all_txt_files, processed_out_file_name)

    # Create also an "aggregated" version of the data
    data: pd.DataFrame = pd.read_csv(processed_out_file_name)
    agg_functions: list[str] = ['mean', 'median', 'std', 'min', 'max']

    agg_data: pd.DataFrame = data.groupby(['Size', 'CNI', 'Nodes', 'Benchmark']).agg(agg_functions).reset_index()
    agg_data.columns = ['Size', 'CNI', 'Nodes', 'Benchmark', 'Mean', 'Median', 'Std', 'Min', 'Max']
    agg_data.to_csv("processed_data_aggregated.csv", index=False)

if __name__ == "__main__":
    main()
