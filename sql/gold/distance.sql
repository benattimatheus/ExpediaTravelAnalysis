DROP TABLE IF EXISTS gold_distance_analysis;

CREATE TABLE gold_distance_analysis AS
SELECT
    CASE 
        WHEN orig_destination_distance < 0 THEN 'unknown'
        WHEN orig_destination_distance < 100 THEN 'near'
        WHEN orig_destination_distance < 1000 THEN 'medium'
        ELSE 'far'
    END AS distance_group,

    COUNT(*) AS total_events,
    SUM(is_booking) AS total_bookings,
    ROUND(AVG(is_booking), 4) AS booking_rate

FROM public.expedia_silver

GROUP BY distance_group

HAVING COUNT(*) > 50

ORDER BY booking_rate DESC;