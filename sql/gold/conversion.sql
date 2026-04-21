DROP TABLE IF EXISTS gold_conversion_by_segment;

CREATE TABLE gold_conversion_by_segment AS
SELECT
    is_mobile,
    channel,
    trip_type,
    is_package,

    COUNT(*) AS total_events,
    SUM(is_booking) AS total_bookings,
    ROUND(AVG(is_booking), 4) AS booking_rate

FROM public.expedia_silver

GROUP BY
    is_mobile,
    channel,
    trip_type,
    is_package

HAVING COUNT(*) > 50

ORDER BY booking_rate DESC;
