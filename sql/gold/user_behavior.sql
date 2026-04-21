DROP TABLE IF EXISTS gold_user_behavior;

CREATE TABLE gold_user_behavior AS
SELECT
    user_id,

    COUNT(*) AS total_events,
    SUM(is_booking) AS total_bookings,
    ROUND(AVG(is_booking), 4) AS booking_rate,

    AVG(cnt) AS avg_session_intensity,
    MAX(cnt) AS max_session_intensity,

    AVG(is_mobile) AS mobile_usage_rate,

    AVG(stay_duration) AS avg_stay_duration,
    AVG(advance_booking_days) AS avg_advance_booking_days,

    AVG(total_guests) AS avg_guests,
    AVG(is_family_trip) AS family_trip_rate,
    AVG(is_multi_room) AS multi_room_rate

FROM public.expedia_silver

WHERE user_id IS NOT NULL

GROUP BY user_id

HAVING COUNT(*) > 5

ORDER BY booking_rate DESC;