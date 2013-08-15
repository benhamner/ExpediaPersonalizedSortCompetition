
SELECT COUNT(visitor_id) -- 16,118,859
FROM UserSearch

SELECT COUNT(DISTINCT visitor_id) -- 608616
FROM UserSearch

SELECT visitor_id,
       COUNT(visitor_id)
FROM UserSearch
GROUP BY visitor_id
ORDER BY COUNT(visitor_id) DESC

SELECT srch_id,
       COUNT(srch_id)
FROM UserSearch
GROUP BY srch_id
ORDER BY COUNT(srch_id) DESC

SELECT visitor_id,
       SUM(click_bool),
       SUM(booking_bool),
       COUNT(DISTINCT srch_id)
FROM UserSearch
GROUP BY visitor_id
ORDER BY SUM(click_bool) DESC