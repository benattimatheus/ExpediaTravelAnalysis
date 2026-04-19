DROP TABLE IF EXISTS gold_conversion_by_segment;

CREATE TABLE gold_conversion_by_segment AS
SELECT
    CASE
        WHEN is_mobile = 1 THEN 'mobile'
        ELSE 'other'
    END AS device,

    channel,
    trip_type,

    CASE
        WHEN is_package = 1 THEN 'part_of_package'
        ELSE 'other'
    END AS package,

    CASE
        WHEN cnt = 1 THEN 'low'
        WHEN cnt BETWEEN 2 AND 5 THEN 'medium'
        ELSE 'high'
    END AS session_intensity,

    CASE
        WHEN advance_booking_days <= 3 THEN 'last_minute'
        WHEN advance_booking_days <= 14 THEN 'short_term'
        WHEN advance_booking_days <= 60 THEN 'mid_term'
        ELSE 'long_term'
    END AS booking_window,

    CASE
        WHEN stay_duration <= 2 THEN 'short_stay'
        WHEN stay_duration <= 7 THEN 'medium_stay'
        ELSE 'long_stay'
    END AS stay_type,

    CASE
        WHEN orig_destination_distance < 100 THEN 'near'
        WHEN orig_destination_distance < 1000 THEN 'medium'
        WHEN orig_destination_distance >= 1000 THEN 'far'
        ELSE 'unknown'
    END AS distance_group,

    srch_destination_type_id,

    COUNT(*) AS total_events,
    SUM(is_booking) AS total_bookings,
    ROUND(AVG(is_booking), 4) AS booking_rate

FROM public.expedia_silver

GROUP BY
    is_mobile,
    channel,
    trip_type,
    is_package,
    session_intensity,
    booking_window,
    stay_type,
    distance_group,
    srch_destination_type_id

HAVING COUNT(*) > 50

ORDER BY booking_rate DESC;