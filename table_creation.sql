CREATE TABLE course (
    course_id int NOT NULL AUTO_INCREMENT,
    code_module varchar(45) NOT NULL,
    code_presentation varchar(45) NOT NULL,
    PRIMARY KEY (course_id)
);

CREATE TABLE student (
    student_id int NOT NULL,
    course_id int NOT NULL,
    num_of_prev_attempts int,
    final_result varchar(45),
    PRIMARY KEY (student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE student_registration (
    student_id int NOT NULL,
    course_id int NOT NULL,
    is_registered bool NOT NULL DEFAULT FALSE,
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
