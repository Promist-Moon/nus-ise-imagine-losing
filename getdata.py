import pandas as pd


## DATA GETTERS
# Note: Quarters are represented by its index in the DataFrame for the loading plan

# select a row of loading data
def get_weekly_loading(loading_data: pd.DataFrame, 
                       quarter: int,
                       weeks: int=13) -> list:
    
    return (loading_data.iloc[quarter] / weeks).to_list()


# randomly select a row of rpt data
def random_weekly_rpt(rpt_data: pd.DataFrame) -> list:

    row = rpt_data.sample(n=1)
    return row.iloc[0].to_list()


# default utilisation data
def get_default_utilisation() -> dict:
    return {
        'H': 0.85,
        'I': 0.75,
        'J': 0.60
    }


# get utilisation data for workstation
def get_utilisation(utilisation_data: dict, 
                    tool_name: str) -> float:
    
    return utilisation_data[tool_name]


# get tool count for a specific tool in some quarter
def get_tool_count(tool_count_data: pd.DataFrame, 
                   quarter: int,
                   tool_name: str) -> int:
    
    return tool_count_data.iloc[quarter].loc[tool_name]



# TESTING GROUND
def functional_test():

    # files
    rpt_df = pd.read_csv("rpt.csv")
    node_loading_df = pd.read_csv("Q1a calculated values.csv")
    tool_count_df = pd.read_csv("tool_requirement.csv")

    # get data
    weekly_loading = get_weekly_loading(loading_data=node_loading_df,
                                        quarter=0)
    weekly_rpt = [random_weekly_rpt()]