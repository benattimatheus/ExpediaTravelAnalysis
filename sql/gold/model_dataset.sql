DROP TABLE IF EXISTS gold_model_dataset;

CREATE TABLE gold_model_dataset AS
SELECT
    user_id,

    is_mobile,
    is_package,
    channel,
    cnt,

    trip_type,
    is_family_trip,
    is_multi_room,
    total_guests,

    stay_duration,
    advance_booking_days,

    user_location_country,
    hotel_country,
    srch_destination_id,
    srch_destination_type_id,

    orig_destination_distance,

    hotel_cluster,

    is_booking

FROM public.expedia_silver

WHERE
    user_id IS NOT NULL
    AND hotel_cluster IS NOT NULL
    AND stay_duration > 0
    AND advance_booking_days >= 0;