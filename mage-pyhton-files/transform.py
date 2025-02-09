import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    datetime_dim=df[['tpep_pickup_datetime','tpep_dropoff_datetime']].drop_duplicates().reset_index(drop=True)
    datetime_dim['Pick_hour']=datetime_dim['tpep_pickup_datetime'].dt.hour
    datetime_dim['Pick_day']=datetime_dim['tpep_pickup_datetime'].dt.day
    datetime_dim['Pick_month']=datetime_dim['tpep_pickup_datetime'].dt.month
    datetime_dim['Pick_year']=datetime_dim['tpep_pickup_datetime'].dt.year
    datetime_dim['Pick_weekday']=datetime_dim['tpep_pickup_datetime'].dt.weekday

    datetime_dim['Drop_hour']=datetime_dim['tpep_dropoff_datetime'].dt.hour
    datetime_dim['Drop_day']=datetime_dim['tpep_dropoff_datetime'].dt.day
    datetime_dim['Drop_month']=datetime_dim['tpep_dropoff_datetime'].dt.month
    datetime_dim['Drop_year']=datetime_dim['tpep_dropoff_datetime'].dt.year
    datetime_dim['Drop_weekday']=datetime_dim['tpep_dropoff_datetime'].dt.weekday

    datetime_dim['datetime_id']=datetime_dim.index

    datetime_dim=datetime_dim[['datetime_id','tpep_pickup_datetime','Pick_hour','Pick_day','Pick_month',
                           'Pick_year','Pick_weekday','tpep_dropoff_datetime',
                           'Drop_hour','Drop_day','Drop_month','Drop_year','Drop_weekday']]
    
    passenger_count_dim=df[['passenger_count']].drop_duplicates().reset_index(drop=True)
    passenger_count_dim['passenger_count_id']=passenger_count_dim.index
    passenger_count_dim=passenger_count_dim[['passenger_count_id','passenger_count']]

    trip_distance_dim=df[['trip_distance']].drop_duplicates().reset_index(drop=True)
    trip_distance_dim['trip_distance_id']=trip_distance_dim.index
    trip_distance_dim=trip_distance_dim[['trip_distance_id','trip_distance']]

    rate_code_type={
        1:"Standard rate",
        2:"JFK",
        3:"Newark",
        4:"Nassau or Westchester",
        5:"Negotiated fare",
        6:"Group ride"
    }

    Rate_code_dim=df[['RatecodeID']].drop_duplicates().reset_index(drop=True)
    Rate_code_dim['rate_code_id']=Rate_code_dim.index
    Rate_code_dim['Rate_code_name']=Rate_code_dim['RatecodeID'].map(rate_code_type)
    Rate_code_dim=Rate_code_dim[['rate_code_id','RatecodeID','Rate_code_name']]

    Payment_type_name = {
        1:"Credit card",
        2:"Cash",
        3:"No charge",
        4:"Dispute",
        5:"Unknown",
        6:"Voided trip"
    }

    Payment_type_dim=df[['payment_type']].drop_duplicates().reset_index(drop=True)
    Payment_type_dim['payment_type_id']=Payment_type_dim.index
    Payment_type_dim['payment_type_name']=Payment_type_dim['payment_type'].map(Payment_type_name)
    Payment_type_dim=Payment_type_dim[['payment_type_id','payment_type','payment_type_name']]

    fact_table=df.merge(passenger_count_dim,on='passenger_count')\
            .merge(trip_distance_dim,on='trip_distance')\
            .merge(Rate_code_dim,on='RatecodeID')\
            .merge(datetime_dim,on=['tpep_pickup_datetime','tpep_dropoff_datetime'])\
            .merge(Payment_type_dim,on='payment_type')\
            [['VendorID','datetime_id','passenger_count_id','trip_distance_id','rate_code_id',
                'PULocationID','DOLocationID','payment_type_id','store_and_fwd_flag','fare_amount','extra',
                'mta_tax','tip_amount','tolls_amount','improvement_surcharge','total_amount']]

    return {"datetime_dim":datetime_dim.to_dict(orient="dict"),
    "passenger_count_dim":passenger_count_dim.to_dict(orient="dict"),
    "trip_distance_dim":trip_distance_dim.to_dict(orient="dict"),
    "Rate_code_dim":Rate_code_dim.to_dict(orient="dict"),
    "Payment_type_dim":Payment_type_dim.to_dict(orient="dict"),
    "fact_table":fact_table.to_dict(orient="dict")
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
