import pandas as pd
import numpy as np
from getdata import *


## SIMULATORS

# check if (tool requirement < tool count) is satisfied given a certain weekly rpt
def insufficient_tools(
        weekly_tooltime: float,
        utilisation: float, 
        tool_count: int
        ):

    tool_requirement = weekly_tooltime / (7 * 24 * 60 * utilisation)
    criteria = tool_requirement > tool_count
    # print(f'{weekly_tooltime=}, {tool_requirement=}, {tool_count=}, {criteria=}')

    if criteria:
        return True
    
    return False


# simulate quarterly (or average weekly success rate) of a tool in a given quarter
def simulate_quarter(
        rpt_data: pd.DataFrame, 
        loading_data: pd.DataFrame, 
        utilisation_data: dict,
        tool_count_data: pd.DataFrame,
        quarter: int,
        tool_list: list,     # list of tools to be simulated
        weeks: int=13,       # number of simulations, set to 13 weeks by default
        mode: str='quarter'  
              # 'quarter': returns True only if all weeks in the quarter are successful
              # 'week': returns average weekly success rate
        ) -> dict:


    def collect_data(tool_name: str):
        weekly_loading = get_weekly_loading(loading_data=loading_data, 
                                            quarter=quarter,
                                            tool_name=tool_name)
        tool_utilisation = get_utilisation(utilisation_data=utilisation_data, 
                                           tool_name=tool_name)
        tool_count = get_tool_count(tool_count_data=tool_count_data,
                                    quarter=quarter,
                                    tool_name=tool_name)
        return weekly_loading, tool_utilisation, tool_count


    def sim_quarterly(weekly_loading: float, 
                      tool_utilisation: float, 
                      tool_count: int) -> bool:
        for i in range(weeks):
            weekly_tooltime = weekly_loading * random_weekly_rpt(
                rpt_data=rpt_data,
                tool_name=tool_name,
                loading=int(weekly_loading)
                )
            
            if insufficient_tools(
                weekly_tooltime=weekly_tooltime, 
                utilisation=tool_utilisation,
                tool_count=tool_count):
                return True
            else:
                pass
        
        return False


    def sim_weekly(weekly_loading: float, 
                   tool_utilisation: float, 
                   tool_count: int) -> float:
        fail_count = 0
        for i in range(weeks):
            weekly_tooltime = weekly_loading * random_weekly_rpt(
                rpt_data=rpt_data,
                tool_name=tool_name,
                loading=int(weekly_loading)
                )
            
            if insufficient_tools(
                weekly_tooltime=weekly_tooltime, 
                utilisation=tool_utilisation,
                tool_count=tool_count
                ):
                fail_count += 1
        
        return fail_count / weeks


    # simulation (iterating through list of tools)
    result = {}
    for tool_name in tool_list:

        weekly_loading, tool_utilisation, tool_count = collect_data(tool_name)

        if mode == 'quarter':
            sim_output = sim_quarterly(weekly_loading=weekly_loading, 
                                       tool_utilisation=tool_utilisation, 
                                       tool_count=tool_count)
        elif mode == 'week':
            sim_output = sim_weekly(weekly_loading=weekly_loading, 
                                    tool_utilisation=tool_utilisation, 
                                    tool_count=tool_count)
        
        result[tool_name] = sim_output
    
    return result


# run success rate simulaton for every quarter
def simulate_all(
        rpt_data: pd.DataFrame, 
        loading_data: pd.DataFrame, 
        utilisation_data: dict,
        tool_count_data: pd.DataFrame,
        cycles: int,
        quarters: int,
        tool_list: list,
        mode: str='quarter'
        ):
    
    result = []
    for quarter in range(quarters):
        print(f'Quarter {quarter}')

        quarter_result = []
        for i in range(cycles):
            # print(f'Cycle {i}')
            quarter_result.append(simulate_quarter(
                rpt_data=rpt_data, 
                loading_data=loading_data,
                utilisation_data=utilisation_data,
                tool_count_data=tool_count_data,
                quarter=quarter,
                tool_list=tool_list,
                mode=mode
                )
            )

        quarter_average = pd.DataFrame(quarter_result).mean(axis=0)
        result.append(quarter_average)
    
    return pd.concat(result, axis=1).T


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


    # distribution of RPT mean
    # def sample_rpt(tool_name: str) -> list:
    #     return [random_weekly_rpt(
    #         rpt_df, tool_name, int(get_weekly_loading(tool_loading_df, 0, 'H'))
    #     ) for i in range(100000)]
    

    # rpt_samples = pd.DataFrame(
    #     {'H': sample_rpt('H'),
    #      'I': sample_rpt('I'),
    #      'J': sample_rpt('J')}
    #      )
    
    # rpt_samples.to_csv("rpt_samples.csv")


    # simulation
    sim = simulate_all(
        rpt_data=rpt_df, 
        loading_data=tool_loading_df,
        utilisation_data=utilisation,
        tool_count_data=tool_count_df,
        cycles=1000,
        quarters=8,
        tool_list=['H', 'I', 'J'],
        mode='quarter')
    
    sim.to_csv("simulation.csv")

    return 0


main()