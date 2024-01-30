CREATE OR REPLACE TABLE `macro-polymer-407712.data_eng_project.tbl_analytics` AS (
SELECT 
f.VendorID,
d.tpep_pickup_datetime,
d.tpep_dropoff_datetime,
p.passenger_count,
t.trip_distance,
r.RatecodeID,
r.Rate_code_name,
pay.payment_type,
pay.payment_type_name,
f.PULocationID,
f.DOLocationID,
f.store_and_fwd_flag,
f.fare_amount,
f.extra,
f.mta_tax,
f.improvement_surcharge,
f.tip_amount,
f.tolls_amount,
f.total_amount
FROM `macro-polymer-407712.data_eng_project.fact_table` f 
JOIN `macro-polymer-407712.data_eng_project.datetime_dim` d on f.datetime_id=d.datetime_id
JOIN `macro-polymer-407712.data_eng_project.passenger_count_dim` p on p.passenger_count_id=f.passenger_count_id
JOIN `macro-polymer-407712.data_eng_project.trip_distance_dim` t on t.trip_distance_id=f.trip_distance_id
JOIN `macro-polymer-407712.data_eng_project.Rate_code_dim` r on r.rate_code_id=f.rate_code_id
JOIN `macro-polymer-407712.data_eng_project.Payment_type_dim` pay on pay.payment_type_id=f.payment_type_id);
