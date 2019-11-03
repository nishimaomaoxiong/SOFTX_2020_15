import pandas as pd
import numpy as np

'''
    This module contains several normalization methods. 
    See ReadMe.md for usage example.
'''


def zero_one_normalize(df: pd.DataFrame, excluded_colnames: list = []) -> pd.DataFrame:
    """
    Applies the MinMaxScaler from the module sklearn.preprocessing to find
    the min and max of each column and transforms the values into the range
    of [0,1]. The transformation is given by::

        X_scaled = (X - X.min(axis=0)) / range
    where::
        range = X.max(axis=0) - X.min(axis=0)

    Note: In case multiple dataframes are used (i.e., several partitions of
    dataset in training and testing), make sure that all of them will
    be passed to this method at once, and as one single dataframe. Otherwise,
    the normalization will be carried out on local (as opposed to global)
    extrema, which is incorrect.

    :param df: the dataframe to be normalized.
    :param excluded_colnames: the name of non-numeric columns (e.g. TimeStamp,
    ID etc) that must be excluded before normalization takes place.
    They will be added back to the normalized data.
    :return: the same dataframe as input, with the label column unchanged,
    except that now the numerical values are transformed into a [0, 1]-range.
    """
    from sklearn.preprocessing import MinMaxScaler

    # Separate data (numeric) from those to be excluded (ids and labels)
    numeric_colnames = [colname for colname in list(df) if colname not in excluded_colnames]
    # Exclude all non-numeric columns
    df_numeric = df[numeric_colnames].select_dtypes(include=np.number)
    excluded_colnames.extend(df[numeric_colnames].select_dtypes(exclude=np.number).columns)
    df_ids_labels = df[excluded_colnames]

    # prepare normalizer and normalize
    scaler = MinMaxScaler()
    res_ndarray = scaler.fit_transform(df_numeric)  # type:np.ndarray
    df_numeric = pd.DataFrame(res_ndarray, columns=list(df_numeric), dtype=float)  # type:pd.DataFrame

    # Reset the indices (so that they match)
    df_ids_labels.reset_index()
    df_numeric.reset_index()

    # Add the excluded columns back
    df_norm = df_ids_labels.join(df_numeric)

    return df_norm


def negativeone_one_normalize(df: pd.DataFrame, excluded_colnames: list = []) -> pd.DataFrame:
    """
    Applies the `MinMaxScaler` from the module `sklearn.preprocessing` to find
    the min and max of each column and transforms the values into the range
    of [-1,1]. The transformation is given by::

        X_scaled = scale * X - 1 - X.min(axis=0) * scale
    where::
        scale = 2 / (X.max(axis=0) - X.min(axis=0))

    Note: In case multiple dataframes are used (i.e., several partitions of
    dataset in training and testing), make sure that all of them will
    be passed to this method at once, and as one single dataframe. Otherwise,
    the normalization will be carried out on local (as opposed to global)
    extrema, which is incorrect.

    :param df: the dataframe to be normalized.
    :param excluded_colnames: the name of non-numeric columns (e.g. TimeStamp,
    ID etc) that must be excluded before normalization takes place.
    They will be added back to the normalized data.
    :return: the same dataframe as input, with the label column unchanged,
    except that now the numerical values are transformed into a [-1, 1]-range.
    """
    from sklearn.preprocessing import MinMaxScaler

    # Separate data (numeric) from those to be excluded (ids and labels)
    numeric_colnames = [colname for colname in list(df) if colname not in excluded_colnames]
    # Exclude all non-numeric columns
    df_numeric = df[numeric_colnames].select_dtypes(include=np.number)
    excluded_colnames.extend(df[numeric_colnames].select_dtypes(exclude=np.number).columns)
    df_ids_labels = df[excluded_colnames]

    # prepare normalizer and normalize
    scaler = MinMaxScaler((-1, 1))
    res_ndarray = scaler.fit_transform(df_numeric)  # type:np.ndarray
    df_numeric = pd.DataFrame(res_ndarray, columns=list(df_numeric), dtype=float)  # type:pd.DataFrame

    # Reset the indices (so that they match)
    df_ids_labels.reset_index()
    df_numeric.reset_index()

    # Add the excluded columns back
    df_norm = df_ids_labels.join(df_numeric)

    return df_norm


def standardize(df: pd.DataFrame, excluded_colnames: list= []) -> pd.DataFrame:
    """
    Applies the StandardScaler from the module sklearn.preprocessing by
    removing the mean and scaling to unit variance. The transformation
    is given by:
        .. math::
            z = (x - u) / s

    where `x` is a feature vector, `u` is the mean of the vector, and `s`
    represents its standard deviation.

    Note: In case multiple dataframes are used (i.e., several partitions of
    dataset in training and testing), make sure that all of them will
    be passed to this method at once, and as one single dataframe. Otherwise,
    the normalization will be carried out on local (as opposed to global)
    extrema, which is incorrect.

    :param df: the dataframe to be normalized.
    :param excluded_colnames: the name of non-numeric columns (e.g. TimeStamp,
    ID etc) that must be excluded before normalization takes place. They will
    be added back to the normalized data.
    :return: the same dataframe as input, with the label column unchanged,
    except that now the numeric values are transformed into a range with mean
    at 0 and unit standard deviation.
    """
    from sklearn.preprocessing import StandardScaler

    # Separate data (numeric) from those to be excluded (ids and labels)
    numeric_colnames = [colname for colname in list(df) if colname not in excluded_colnames]
    # Exclude all non-numeric columns
    df_numeric = df[numeric_colnames].select_dtypes(include=np.number)
    excluded_colnames.extend(df[numeric_colnames].select_dtypes(exclude=np.number).columns)
    df_ids_labels = df[excluded_colnames]

    # prepare normalizer and normalize
    scaler = StandardScaler()
    res_ndarray = scaler.fit_transform(df_numeric)  # type:np.ndarray
    df_numeric = pd.DataFrame(res_ndarray, columns=list(df_numeric), dtype=float)  # type:pd.DataFrame

    # Reset the indices (so that they match)
    df_ids_labels.reset_index()
    df_numeric.reset_index()

    # Add the excluded columns back
    df_norm = df_ids_labels.join(df_numeric)

    return df_norm


def robust_standardize(df: pd.DataFrame, excluded_colnames: list = []) -> pd.DataFrame:
    """
    Applies the RobustScaler from the module sklearn.preprocessing by
    removing the median and scaling the data according to the quantile
    range (IQR). This transformation is robust to outliers.

    Note: In case multiple dataframes are used (i.e., several partitions of
    dataset in training and testing), make sure that all of them will
    be passed to this method at once, and as one single dataframe. Otherwise,
    the normalization will be carried out on local (as opposed to global)
    extrema, hence unrepresentative IQR. This is a bad practice.

    :param df: the dataframe to be normalized.
    :param excluded_colnames: the name of non-numeric (e.g. TimeStamp,
    ID etc)  that must be excluded before normalization takes place.
    They will be added back to the normalized data.

    :return: the same dataframe as input, with the label column unchanged,
    except that now the numerical values are transformed into new range
    determined by IQR.
    """
    from sklearn.preprocessing import RobustScaler

    # Separate data (numeric) from those to be excluded (ids and labels)
    numeric_colnames = [colname for colname in list(df) if colname not in excluded_colnames]
    # Exclude all non-numeric columns
    df_numeric = df[numeric_colnames].select_dtypes(include=np.number)
    excluded_colnames.extend(df[numeric_colnames].select_dtypes(exclude=np.number).columns)
    df_ids_labels = df[excluded_colnames]

    # prepare normalizer and normalize
    scaler = RobustScaler()
    res_ndarray = scaler.fit_transform(df_numeric)  # type:np.ndarray
    df_numeric = pd.DataFrame(res_ndarray, columns=list(df_numeric), dtype=float)  # type:pd.DataFrame

    # Reset the indices (so that they match)
    df_ids_labels.reset_index()
    df_numeric.reset_index()

    # Add the excluded columns back
    df_norm = df_ids_labels.join(df_numeric)

    return df_norm