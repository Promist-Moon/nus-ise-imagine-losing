import pandas as pd
from getdata import *


## SIMULATORS

# check if (tool requirement < tool count) is satisfied given a certain weekly rpt
def sufficient_tools(
        weekly_loading: list,
        weekly_rpt: list, 
        utilisation: float, 
        tool_count: int
        ):

    working_time = sum([load * rpt for load, rpt in zip(weekly_loading, weekly_rpt)])
    tool_requirement = working_time / (7 * 24 * 60 * utilisation)
    criteria = tool_requirement < tool_count

    print(f'{working_time=}, {tool_requirement=}, {tool_count=}, {criteria=}')

    if criteria:
        return True
    
    return False


# simulate success rate of a tool in a given quarter
def simulate_quarter(
        rpt_data: pd.DataFrame, 
        loading_data: pd.DataFrame, 
        utilisation_data: dict,
        tool_count_data: pd.DataFrame,
        quarter: int,
        tool_list: list,  # list of tools to be simulated
        weeks: int=13  # number of simulations, set to 13 weeks by default
        ) -> dict:
    
    result = {}

    # data collection
    for tool_name in tool_list:
        weekly_loading = get_weekly_loading(loading_data=loading_data, 
                                            quarter=quarter)
        tool_utilisation = get_utilisation(utilisation_data=utilisation_data, 
                                           tool_name=tool_name)
        tool_count = get_tool_count(tool_count_data=tool_count_data,
                                    quarter=quarter,
                                    tool_name=tool_name)

        # simulation
        success_count = 0

        for i in range(weeks):
            if sufficient_tools(weekly_loading=weekly_loading, 
                                weekly_rpt=random_weekly_rpt(rpt_data),
                                utilisation=tool_utilisation,
                                tool_count=tool_count):
                success_count += 1

        success_rate = success_count / weeks

        result[tool_name] = success_rate
    
    return result
    


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
    utilisation = get_default_utilisation()

    # df pre-processing
    tool_loading_df = node_loading_df.set_axis(
        labels=['H', 'I', 'J', 'difference'],
        axis=1
        )


    sim = simulate_quarter(
        rpt_data=rpt_df, 
        loading_data=tool_loading_df,
        utilisation_data=utilisation,
        tool_count_data=tool_count_df,
        quarter=0,
        tool_list=['H', 'I', 'J']
        )
    
    print(sim)

    return 0


main()