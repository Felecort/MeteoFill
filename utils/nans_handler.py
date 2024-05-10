import numpy as np
import pandas as pd


def create_nan(data: pd.DataFrame, prob: float=0.5) -> pd.DataFrame:
    """
    Create Nans in input data
    - `data` - input pandas DataFrame
    - `prob` - probabilyli that each sample will be replaced by Nan
    """
    mask = np.random.binomial(n=1, p=prob, size=data.shape).astype(np.float32)
    mask[mask == 0] = np.nan
    return mask * data.select_dtypes(include='number')
