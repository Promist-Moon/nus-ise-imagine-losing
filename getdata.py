import pandas as pd


## DATA GETTERS

# select a row of loading data
def get_weekly_loading(loading_data: pd.DataFrame, quarter):
    return (loading_data.iloc[quarter] / 13).to_list()

# randomly select a row of rpt data
def random_weekly_rpt(rpt_data: pd.DataFrame):
    row = rpt_data.sample(n=1)
    return row.iloc[0].to_list()

# get utilisation data for workstation
def get_utilisation(utilisation_data: dict, workstation_name: str):
    return utilisation_data.loc[workstation_name]

# get tool count data for workstation
def get_tool_count(tool_count_data: dict, workstation_name: str, quarter: int):
    return tool_count_data.iloc[quarter].loc[workstation_name]