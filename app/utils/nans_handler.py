import numpy as np
import pandas as pd


def create_nan(data: pd.DataFrame, prob: float=0.5) -> pd.DataFrame:
    """
    Create Nans in input data    
    
    Parameters
    ----------
    - `data` - input pandas DataFrame
    - `prob` - probabilyli that each sample will be replaced by Nan
    """
    mask = np.random.binomial(n=1, p=prob, size=data.shape).astype(np.float32)
    mask[mask == 0] = np.nan
    return mask * data.select_dtypes(include='number')


def fill_nans_mean(data: pd.DataFrame) -> pd.DataFrame:
    """
    Fill nant using neam of neighbors algorithm  

    Examples
    ----------
    ::
        [1, 2, 3, NAN, NAN, NAN, 11] - >
     -> [1, 2, 3, 7,   7,   7,   11]
    """
    filled_data = data.copy()
    for column in filled_data.columns[1:]:
        nan_indices = filled_data[column].index[filled_data[column].apply(np.isnan)]
        for index in nan_indices:
            prev_index = filled_data[column].index[filled_data[column].apply(lambda x: not np.isnan(x)) & (filled_data[column].index <= index)].max()
            next_index = filled_data[column].index[filled_data[column].apply(lambda x: not np.isnan(x)) & (filled_data[column].index >= index)].min()
            if np.isnan(prev_index):
                prev_index = filled_data[column].first_valid_index()
                filled_data.loc[index, column] = filled_data.loc[prev_index, column]
            if np.isnan(next_index):
                next_index = filled_data[column].last_valid_index()
                filled_data.loc[index, column] = filled_data.loc[prev_index, column]

            mean_value = (filled_data.at[prev_index, column] + filled_data.at[next_index, column]) / 2

            filled_data.loc[prev_index+1:next_index-1, column] = mean_value
            
    return filled_data
