from tabnanny import check

import numpy as np
from scipy.optimize import linprog
import pandas as pd

# from Q2'26 to Q4'27
tam_list = [27.4, 34.9, 39.0, 44.7, 51.5, 52.5, 53.5]
node_1_yield = [0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98]
node_2_yield = [0.82, 0.95, 0.98, 0.98, 0.98, 0.98, 0.98]
node_3_yield = [0.25, 0.35, 0.50, 0.65, 0.85, 0.95, 0.98]

# Objective Function = maximise(qx1 + rx2 + sx3 + sum_CAPEX*initialToolCount_allWorkshops)
# q, r, s is the coefficients of x1, x2, x3 for each quarter calculated in excel

def get_quarter_details(tam_list, node_1_yield, node_2_yield, node_3_yield, count):
    return [tam_list[count], node_1_yield[count], node_2_yield[count], node_3_yield[count]]

def get_coefficients(file_name, quarter):
    coeff_all_quarters = pd.read_csv(file_name)
    coeff = coeff_all_quarters.iloc[:,quarter]
    # [q, r, s, sum_CAPEX*initialToolCount_allWorkshops]
    return coeff.to_list()

def main():
    initial_values = [12000, 5000, 1000]
    ans = []
    for i, x in enumerate(tam_list):
        quarter = get_quarter_details(tam_list, node_1_yield, node_2_yield, node_3_yield, i)
        coefficients = get_coefficients("Coefficients_1biv.csv", i+2)
        c = [coefficients[0], coefficients[1], coefficients[2]]

        # Constraints
        # GBpW * yield * x + GBpW * yield * y + GBpW * yield * z <= 10**6 * (TAM + 2) / 13
        # -qx1 - rx2 - sx3 <= sum_CAPEX*initialToolCount_allWorkshops
        # 0 * x + 0 * y + 0 * z = 0
        A = [[100 * quarter[1], 150 * quarter[2], 270 * quarter[3]],
             [-coefficients[0], -coefficients[1], -coefficients[2]],
             [0, 0, 0]
             ]
        b = [((quarter[0]+2) * pow(10, 6) / 13),
             coefficients[3],
             0
             ]

        bounds_curr = [(max(0, initial_values[0] - 2500), initial_values[0] + 2500),
                       (max(0, initial_values[1] - 2500), initial_values[1] + 2500),
                       (max(0, initial_values[2] - 2500), initial_values[2] + 2500)]

        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds_curr, method='highs')

        if result.success:
            prelim_ans = (int(result.x[0]), int(result.x[1]), int(result.x[2]))
            c_gbprod = [100 * quarter[1], 150 * quarter[2], 270 * quarter[3]]
            check_TAM = ((quarter[0]+2) * pow(10, 6) / 13) - (c_gbprod[0] * prelim_ans[0]) - (c_gbprod[1] * prelim_ans[1]) - (c_gbprod[2] * prelim_ans[2])
            profit = coefficients[0] * prelim_ans[0] + coefficients[1] * prelim_ans[1] + coefficients[2] * prelim_ans[2] + coefficients[3]
            print(profit)
            prelim_ans += (check_TAM*13, profit*13)
            ans.append(prelim_ans)
        else:
            ans.append(())

        initial_values = [int(result.x[0]), int(result.x[1]), int(result.x[2])]

    # Make into data frame
    df = pd.DataFrame(ans)

    # Save to a CSV file
    df.to_csv("Q1biv Values.csv", index=False, header=["Node1", "Node2", "Node3", "Difference/quarter", "Profit/quarter"])

if __name__ == "__main__":
    main()