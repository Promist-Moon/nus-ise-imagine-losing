import numpy as np
from scipy.optimize import linprog
import pandas as pd

# from Q2'26 to Q4'27
tam_list = [27.4, 34.9, 39.0, 44.7, 51.5, 52.5, 53.5]
node_1_yield = [0.98, 0.98, 0.98, 0.98, 0.98, 0.98, 0.98]
node_2_yield = [0.82, 0.95, 0.98, 0.98, 0.98, 0.98, 0.98]
node_3_yield = [0.25, 0.35, 0.50, 0.65, 0.85, 0.95, 0.98]

def get_quarter_details(tam_list, node_1_yield, node_2_yield, node_3_yield, count):
    return [tam_list[count], node_1_yield[count], node_2_yield[count], node_3_yield[count]]

def main():
    initial_values = [12000, 5000, 1000]
    ans = []
    for i, x in enumerate(tam_list):
        quarter = get_quarter_details(tam_list, node_1_yield, node_2_yield, node_3_yield, i)
        c = [-100 * quarter[1], -150 * quarter[2], -270 * quarter[3]]

        # Constraints (Ax <= b)
        # -100(0.98)(x) - 150(0.82)(y) - 270(0.25)(z) <= 10^6 * tam / 13
        A = [[100 * quarter[1], 150 * quarter[2], 270 * quarter[3]],
             [0, 0, 0],
             ]
        b = [quarter[0] * pow(10, 6) / 13, 0]

        bounds_curr = [(max(0, initial_values[0] - 2500), initial_values[0] + 2500),
                       (max(0, initial_values[1] - 2500), initial_values[1] + 2500),
                       (max(0, initial_values[2] - 2500), initial_values[2] + 2500)]

        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds_curr, method='highs')

        if result.success:
            prelim_ans = (int(result.x[0]), int(result.x[1]), int(result.x[2]))
            check = (quarter[0] * pow(10, 6) / 13) - (-c[0] * prelim_ans[0]) - (-c[1] * prelim_ans[1]) - (-c[2] * prelim_ans[2])
            prelim_ans += (check,)
            ans.append(prelim_ans)
        else:
            ans.append(())

        initial_values = [int(result.x[0]), int(result.x[1]), int(result.x[2])]

    # print(ans)
    df = pd.DataFrame(ans)

    # Save to a CSV file
    df.to_csv("Calculated values.csv", index=False, header=["Node1", "Node2", "Node3", "difference"])

if __name__ == "__main__":
    main()