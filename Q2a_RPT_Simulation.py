import pandas as pd
from getdata import *


## SIMULATORS

# check if weekly rpt makes (tool requirement < tool count)
def sufficient_tools(
        weekly_loading: list,
        weekly_rpt: list, 
        utilisation: float, 
        tool_count: int
        ):
    
    if len(weekly_loading) != len(weekly_rpt):
        raise ValueError('Loading count does not match RPT value count')

    working_time = sum([load * rpt for load, rpt in zip(weekly_loading, weekly_rpt)])

    criteria = working_time / (7 * 24 * 60 * utilisation) < tool_count

    if criteria:
        return True
    
    return False


# simulate n number of weeks and calculate weekly success probability
def simulate_week(rpt_data: pd.DataFrame, 
                  loading_data: pd.DataFrame, 
                  utilisation_data: dict,
                  tool_count_data: pd.DataFrame,
                  tool_name: str,
                  quarter: int,
                  n: int):  # number of simulations
    
    weekly_success = 0
    weekly_loading = get_weekly_loading(loading_data, quarter)

    for i in range(n):
        if sufficient_tools(weekly_loading=weekly_loading, 
                            weekly_rpt=random_weekly_rpt(rpt_data),
                            utilisation=utilisation_data,
                            tool_count=get_tool_count(tool_count_data=tool_count_data,
                                                      tool_name=tool_name,
                                                      quarter=quarter)):
            weekly_success += 1
        
    success_rate = weekly_success / n
    


# simulate success rate of tool across quarters
# def simulate_tool():
    # success_rate = {}
    # for quarter in range(len(loading_data)):
        

        
    
    # return success_rate


## main
def main():

    # files
    rpt_df = pd.read_csv("rpt.csv")
    node_loading_df = pd.read_csv("Q1a calculated values.csv")
    tool_count_df = pd.read_csv("tool_requirement.csv")

    # df pre-processing
    tool_loading_df = node_loading_df.set_axis(
        labels=['H', 'I', 'J', 'difference'],
        axis=1
        )

    return

    # default data
    default_utilisation = {
        'H': 0.85,
        'I': 0.75,
        'J': 0.60
    }

    sim = simulate_week(rpt_data=rpt_df, 
                        loading_data=loading_df, 
                        utilisation_data=default_utilisation,
                        tool_count_data=tool_count_df,
                        n=10)
    print(sim)

    return 0


main()