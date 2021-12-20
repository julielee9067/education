CREATE TABLE coursera_courses (
    name varchar(45),
    institution varchar(45),
    course_url varchar(200),
    course_id varchar(45)
);

CREATE TABLE coursera_reviews (
    reviews varchar(500),
    reviewers varchar(45),
    date_reviews date,
    rating int,
    course_id varchar(45)
);