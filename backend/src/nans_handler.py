import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.impute import KNNImputer
from sklearn.metrics import root_mean_squared_error

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


def fill_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    """
    Интерполяция по времени позволяет заполнить пропуски, 
    используя соседние известные значения и информацию o времени.
    """

    # data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')
    data = data.interpolate(method='time', limit_direction='both')

    # Если вдруг остались незаполненные значения, то функция пытается заполнить их с помощью KNN, либо линейной регрессией

    imputer = KNNImputer(n_neighbors=5)
    data_filled = pd.DataFrame(imputer.fit_transform(data), columns=data.columns, index=data.index)

    for column in data_filled.columns[data_filled.isnull().any()]:
        missing_indices = data_filled[column].index[data_filled[column].isnull()]
        non_missing_indices = data_filled[column].index[~data_filled[column].isnull()]
        X = non_missing_indices.to_numpy().reshape(-1, 1)
        y = data_filled.loc[non_missing_indices, column].to_numpy().reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, y)
        missing_values = model.predict(missing_indices.to_numpy().reshape(-1, 1))
        data_filled.loc[missing_indices, column] = missing_values.flatten()

    data_filled.reset_index(inplace=True)

    return data_filled


def calculate_rmse(original_df: pd.DataFrame, filled_df: pd.DataFrame) -> float:
    """
    original_df - исходный dataframe без пропусков
    filled_df - dataframe с заполненными пропусками
    """
    numeric_columns = original_df.select_dtypes(include=np.number).columns
    return root_mean_squared_error(original_df[numeric_columns].values.ravel(), filled_df[numeric_columns].values.ravel())
    # return np.sqrt(mean_squared_error(original_df[numeric_columns].values.ravel(), filled_df[numeric_columns].values.ravel()))