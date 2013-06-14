
SELECT COUNT(*)
FROM UserSearch

SELECT COUNT(DISTINCT userid)
FROM UserSearch

SELECT UserId,
       COUNT(UserId)
FROM UserSearch
GROUP BY UserId
ORDER BY COUNT(UserId) DESC

SELECT UserId,
       SUM(click_bool),
       SUM(order_bool)
FROM UserSearch
GROUP BY UserId
ORDER BY SUM(click_bool) DESC