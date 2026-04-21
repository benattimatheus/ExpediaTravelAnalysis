DROP TABLE IF EXISTS gold_destination_performance;

CREATE TABLE gold_destination_performance AS
SELECT
    srch_destination_id,
    srch_destination_type_id,

    COUNT(*) AS total_events,
    SUM(is_booking) AS total_bookings,
    ROUND(AVG(is_booking), 4) AS booking_rate

FROM public.expedia_silver

GROUP BY
    srch_destination_id,
    srch_destination_type_id

HAVING COUNT(*) > 50

ORDER BY booking_rate DESC;