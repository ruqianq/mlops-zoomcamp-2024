if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    base_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
    yellow_url = 'yellow/'
    green_url = 'green/'
    fhv_url = 'fhv/'
    

    return pd.read_csv(
        url, sep=',', compression='gzip'
        )


    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
