LOAD DATA INFILE '/var/lib/mysql-files/26-Education/Coursera/Coursera_reviews.csv'
INTO TABLE coursera_reviews
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(reviews, reviewers, date_reviews, rating, course_id);

LOAD DATA INFILE '/var/lib/mysql-files/26-Education/Coursera/Coursera_courses.csv'
INTO TABLE coursera_courses
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(name, institution, course_url, course_id);
