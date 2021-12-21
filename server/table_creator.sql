CREATE TABLE instructor (
    instructor_id int NOT NULL,
    first_name varchar(45),
    last_name varchar(45),
    PRIMARY KEY (instructor_id)
);

CREATE TABLE course (
    course_id varchar(100) NOT NULL,
    instructor_id int,
    PRIMARY KEY (course_id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(instructor_id)
);

CREATE TABLE review (
    review_id int AUTO_INCREMENT,
    review varchar(1000),
    course_id varchar(100),
    reviewer varchar(45),
    date date,
    rating int,
    PRIMARY KEY (review_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE student (
    student_id int NOT NULL,
    first_name varchar(50),
    last_name varchar(50),
    email varchar(100),
    gender varchar(45),
    region varchar(45),
    highest_education varchar(45),
    imd_band varchar(45),
    age_band varchar(45),
    studied_credits int,
    disability varchar(45),
    PRIMARY KEY (student_id)
);

CREATE TABLE student_registration (
    student_id int NOT NULL,
    course_id int NOT NULL,
    is_registered bool NOT NULL DEFAULT FALSE,
    num_of_prev_attempts int,
    final_result varchar(45),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE assessment (
    assessment_id int NOT NULL,
    course_id int NOT NULL,
    assessment_type varchar(45),
    date int,
    weight int,
    PRIMARY KEY (assessment_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE student_assessment (
    student_id int NOT NULL,
    assessment_id int NOT NULL,
    score int,
    date_submitted int,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (assessment_id) REFERENCES assessment(assessment_id)
);
