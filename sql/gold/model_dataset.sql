DROP TABLE IF EXISTS gold_model_dataset;

CREATE TABLE gold_model_dataset AS
SELECT
    s.date_time,
    s.user_id,

    s.is_mobile,
    s.is_package,
    s.channel,
    s.cnt,

    s.trip_type,
    s.is_family_trip,
    s.is_multi_room,
    s.total_guests,

    s.stay_duration,
    s.advance_booking_days,

    s.user_location_country,
    s.hotel_country,
    s.srch_destination_id,
    s.srch_destination_type_id,

    s.orig_destination_distance,
    CASE
        WHEN s.orig_destination_distance < 0 THEN 'unknown'
        WHEN s.orig_destination_distance < 100 THEN 'near'
        WHEN s.orig_destination_distance < 1000 THEN 'medium'
        ELSE 'far'
    END AS distance_group,

    CASE
        WHEN s.orig_destination_distance < 0 THEN 1
        ELSE 0
    END AS is_distance_unknown,

    CASE
        WHEN s.orig_destination_distance < 0 THEN NULL
        ELSE s.orig_destination_distance
    END AS distance_clean,

    CASE
        WHEN s.orig_destination_distance < 0 AND s.is_mobile = 1 THEN 'unknown_mobile'
        WHEN s.orig_destination_distance < 0 THEN 'unknown_desktop'
        WHEN s.orig_destination_distance < 100 THEN 'near'
        WHEN s.orig_destination_distance < 1000 THEN 'medium'
        ELSE 'far'
    END AS distance_behavior_group,

    ub.booking_rate AS user_booking_rate,
    ub.avg_session_intensity,
    ub.avg_stay_duration,
    ub.avg_advance_booking_days,
    ub.mobile_usage_rate,

    --dp.booking_rate AS destination_booking_rate,
    dp.total_events AS destination_popularity,

    --hc.booking_rate AS cluster_booking_rate,
    --hc.total_events AS cluster_popularity,

    s.hotel_cluster,
    s.is_booking

FROM public.expedia_silver s

LEFT JOIN gold_user_behavior ub
    ON s.user_id = ub.user_id

LEFT JOIN gold_destination_performance dp
    ON s.srch_destination_id = dp.srch_destination_id

LEFT JOIN gold_hotel_cluster_performance hc
    ON s.hotel_cluster = hc.hotel_cluster

WHERE
    s.user_id IS NOT NULL
    AND s.hotel_cluster IS NOT NULL
    AND s.stay_duration > 0
    AND s.advance_booking_days >= 0;