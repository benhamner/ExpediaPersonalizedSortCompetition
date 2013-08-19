SELECT srch_id,
       COUNT(srch_id)
FROM UserSearch
GROUP BY srch_id
ORDER BY COUNT(srch_id) DESC;

SELECT srch_id,
       SUM(click_bool) num_clicks,
       SUM(booking_bool) num_bookings
FROM UserSearch
GROUP BY srch_id
ORDER BY SUM(click_bool) DESC;

SELECT srch_id,
       SUM(click_bool) num_clicks,
       SUM(booking_bool) num_bookings
FROM UserSearch
GROUP BY srch_id
ORDER BY SUM(booking_bool) DESC;

SELECT SUM(booking_bool) num_bookings,
       COUNT(DISTINCT srch_id) num_searches
FROM UserSearch;

SELECT random_bool,
       COUNT(random_bool)
FROM UserSearch
GROUP BY random_bool;

SELECT min(date_time),
       max(date_time)
FROM UserSearch;

SELECT srch_id, COUNT(DISTINCT date_time)
FROM UserSearch
GROUP BY srch_id
ORDER BY COUNT(DISTINCT date_time) DESC;

SELECT site_id, COUNT(site_id)
FROM UserSearch
GROUP BY site_id;

SELECT site_id, COUNT(site_id)
FROM UserSearch
GROUP BY site_id
ORDER BY COUNT(site_id) DESC;

SELECT prop_country_id, COUNT(prop_country_id)
FROM UserSearch
GROUP BY prop_country_id
ORDER BY COUNT(prop_country_id) DESC;

SELECT prop_id, COUNT(prop_id)
FROM UserSearch
GROUP BY prop_id
ORDER BY COUNT(prop_id) DESC;

SELECT visitor_location_country_id, COUNT(visitor_location_country_id)
FROM UserSearch
GROUP BY visitor_location_country_id
ORDER BY COUNT(visitor_location_country_id) DESC;

SELECT DISTINCT prop_starrating
FROM UserSearch;