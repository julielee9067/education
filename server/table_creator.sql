drop table if exists student_assessment;
drop table if exists assessment;
drop table if exists student_registration;
drop table if exists review;
drop table if exists student;
drop table if exists course;
drop table if exists instructor;

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

INSERT INTO course (course_id)
SELECT concat(code_module, '_', code_presentation) as course_id FROM courses;

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

ALTER TABLE studentInfo ADD id_order INT NOT NULL AUTO_INCREMENT, ADD PRIMARY KEY (id_order);

DELETE FROM studentInfo WHERE id_order NOT IN ( 
        SELECT MaxOrder FROM (
            SELECT MAX(id_order) AS MaxOrder
            FROM studentInfo INNER JOIN studentRegistration on 
            (studentInfo.id_student = studentRegistration.id_student 
            AND studentInfo.code_module = studentRegistration.code_module 
            AND studentInfo.code_presentation = studentRegistration.code_presentation)
            GROUP BY studentInfo.id_student 
            ORDER BY studentInfo.id_student
        ) AS o 
);

INSERT INTO student (student_id, gender, region, highest_education, imd_band, age_band, studied_credits, disability)
SELECT id_student, gender, region, highest_education, imd_band, age_band, studied_credits, disability FROM studentInfo;

CREATE TABLE review (
    review_id int AUTO_INCREMENT,
    student_id int NOT NULL,
    review varchar(1000),
    course_id varchar(100),
    date date,
    rating int,
    PRIMARY KEY (review_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE student_registration (
    student_id int NOT NULL,
    course_id varchar(100) NOT NULL,
    is_registered bool NOT NULL DEFAULT TRUE,
    num_of_prev_attempts int,
    final_result varchar(45),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

INSERT INTO student_registration (student_id, course_id, is_registered, num_of_prev_attempts, final_result) 
SELECT studentRegistration.id_student, concat(studentRegistration.code_module, '_', studentRegistration.code_presentation) AS course_id, 
(date_unregistration IS NULL) AS is_registered, num_of_prev_attempts, final_result 
FROM ( 
    studentInfo INNER JOIN studentRegistration on  
    (studentInfo.id_student = studentRegistration.id_student 
    AND studentInfo.code_module = studentRegistration.code_module 
    AND studentInfo.code_presentation = studentRegistration.code_presentation) 
);

CREATE TABLE assessment (
    assessment_id int NOT NULL,
    course_id varchar(100) NOT NULL,
    assessment_type varchar(45),
    date int,
    weight int,
    PRIMARY KEY (assessment_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

INSERT INTO assessment (assessment_id, course_id, assessment_type, date, weight)
SELECT id_assessment, concat(code_module, '_', code_presentation) AS course_id, assessment_type, date, weight FROM assessments;

CREATE TABLE student_assessment (
    student_id int NOT NULL,
    assessment_id int NOT NULL,
    score int,
    date_submitted int,
    PRIMARY KEY (student_id, assessment_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (assessment_id) REFERENCES assessment(assessment_id)
);

INSERT INTO student_assessment (student_id, assessment_id, score, date_submitted)
SELECT id_student, id_assessment, score, date_submitted FROM studentAssessment;
