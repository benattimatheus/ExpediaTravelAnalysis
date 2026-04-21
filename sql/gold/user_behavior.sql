DROP TABLE IF EXISTS gold_user_behavior;

CREATE TABLE gold_user_behavior AS
SELECT
    user_id,

    COUNT(*) AS total_events,
    SUM(is_booking) AS total_bookings,
    ROUND(AVG(is_booking), 4) AS booking_rate,

    ROUND(AVG(cnt), 2) AS avg_session_intensity,
    MAX(cnt) AS max_session_intensity,

    ROUND(AVG(is_mobile), 2) AS mobile_usage_rate,

    ROUND(AVG(stay_duration), 2) AS avg_stay_duration,
    ROUND(AVG(advance_booking_days), 2) AS avg_advance_booking_days,

    ROUND(AVG(total_guests), 2) AS avg_guests,
    ROUND(AVG(is_family_trip), 2) AS family_trip_rate,
    ROUND(AVG(is_multi_room), 2) AS multi_room_rate

FROM public.expedia_silver

WHERE user_id IS NOT NULL

GROUP BY user_id

ORDER BY booking_rate DESC;