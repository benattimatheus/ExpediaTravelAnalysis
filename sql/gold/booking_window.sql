DROP TABLE IF EXISTS gold_booking_window;

CREATE TABLE gold_booking_window AS
SELECT
    CASE
        WHEN advance_booking_days < 0 THEN 'invalid'
        WHEN advance_booking_days <= 3 THEN 'last_minute'
        WHEN advance_booking_days <= 7 THEN 'short_term'
        WHEN advance_booking_days <= 30 THEN 'mid_term'
        ELSE 'long_term'
    END AS booking_window,

    COUNT(*) AS total_events,
    SUM(is_booking) AS total_bookings,
    ROUND(AVG(is_booking), 4) AS booking_rate

FROM public.expedia_silver

WHERE advance_booking_days IS NOT NULL

GROUP BY booking_window

HAVING COUNT(*) > 50

ORDER BY booking_rate DESC;