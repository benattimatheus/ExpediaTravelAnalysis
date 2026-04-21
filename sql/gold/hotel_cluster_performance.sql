DROP TABLE IF EXISTS gold_hotel_cluster_performance;

CREATE TABLE gold_hotel_cluster_performance AS
SELECT
    hotel_cluster,

    COUNT(*) AS total_events,
    SUM(is_booking) AS total_bookings,
    ROUND(AVG(is_booking), 4) AS booking_rate

FROM public.expedia_silver

WHERE hotel_cluster IS NOT NULL

GROUP BY hotel_cluster

HAVING COUNT(*) > 50

ORDER BY booking_rate DESC;