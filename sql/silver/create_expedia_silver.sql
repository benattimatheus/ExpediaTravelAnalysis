DROP TABLE IF EXISTS expedia_silver;

CREATE TABLE expedia_silver AS
SELECT
    id,
    date_time,
    site_name,
    posa_continent,
    user_location_country,
    user_location_region,
    user_location_city,
    COALESCE(orig_destination_distance, -1) AS orig_destination_distance,
    user_id,
    is_mobile,
    is_package,
    channel,
    srch_ci::DATE,
    srch_co::DATE,
    (srch_co - srch_ci) AS stay_duration,
    (srch_ci - date_time::date) AS advance_booking_days,
    srch_adults_cnt,
    srch_children_cnt,
    CASE WHEN srch_children_cnt > 0 THEN 1 ELSE 0 END AS is_family_trip,
    (srch_adults_cnt + srch_children_cnt) AS total_guests,
    srch_rm_cnt,
    CASE WHEN srch_rm_cnt > 1 THEN 1 ELSE 0 END AS is_multi_room,
    CASE
        WHEN srch_adults_cnt = 1 AND srch_children_cnt = 0 THEN 'solo'
        WHEN srch_children_cnt > 0 THEN 'family'
        ELSE 'group'
        END AS trip_type,
    srch_destination_id,
    srch_destination_type_id,
    is_booking,
    cnt,
    hotel_continent,
    hotel_country,
    hotel_market,
    hotel_cluster
FROM public.expedia_raw
WHERE srch_ci IS NOT NULL
  AND srch_co IS NOT NULL
  AND srch_co > srch_ci
  AND user_id IS NOT NULL;