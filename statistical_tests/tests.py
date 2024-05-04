from scipy.stats import f_oneway
import pandas as pd
from tabulate import tabulate

class OneWayAnova:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def run(self, variable_of_interest, *group_variables):
        # Drop rows with NaN values in the variable of interest and group variables
        data = self.dataframe[[variable_of_interest, *group_variables]].dropna()

        # Perform one-way ANOVA for each group variable
        results = []
        for group_var in group_variables:
            unique_groups = data[group_var].unique()
            if len(unique_groups) > 1:  # Check if there's more than one group
                grouped_data = [data[data[group_var] == group][variable_of_interest] for group in unique_groups]
                f_statistic, p_value = f_oneway(*grouped_data)
                results.append([group_var, f_statistic, p_value])
            else:
                print(f"Skipping {group_var} as it has only one group.")

        # Print results in a table
        if results:
            result_table = pd.DataFrame(results, columns=['Group Variable', 'F-Statistic', 'P-value'])
            print(tabulate(result_table, headers='keys', tablefmt='pretty', showindex=False))
        else:
            print("No valid group variables found to perform ANOVA.")