from helper import *

# ----------------------------- Loading the data -----------------------------

csv_file_A = 'dataset_A.csv'
csv_file_B = 'dataset_B.csv'
header = ['id', 'Company Name', 'Website', 'Phone Number', 'Address', 'Postal Code', 'City', 'Country']

data_A = filtering(csv_file_A, header)
data_B = filtering(csv_file_B, header)


# ----------------------------- Data Processing -----------------------------

data_A = processing(data_A)
data_B = processing(data_B)


# ----------------------------- Creating the csv result file -----------------------------

graph_possbilities = group_companies_by_word(data_B['Name Decomposition'])
greedy_matching(data_A, data_B, graph_possbilities)

    