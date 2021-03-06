-- Manual Tests

-------------------- Table Creation: check PK and FK constraints ---------------------------
INSERT INTO instructor(first_name) VALUES ('First'); -- missing PK instructor_id
INSERT INTO instructor(first_name, last_name) VALUES ('First', 'Last'); -- missing PK instructor_id

INSERT INTO course VALUES ('newCourseId', 10); -- invalid FK to instructor_id
INSERT INTO course(instructor_id) VALUES (10); -- missing PK course_id

INSERT INTO student(first_name, last_name) VALUES ('Student', 'One'); -- missing PK student_id

INSERT INTO review(review) VALUES ('the review for this course'); -- missing course_id and student_id
INSERT INTO review(review, course_id) VALUES ('the review for this course', 'AAA_2013J'); -- course_id NOT NULL 
INSERT INTO review(student_id, review) VALUES (8462, 'the review for this course'); -- student_id NOT NULL
INSERT INTO review(student_id, review, course_id) VALUES (8462, 'the review for this course', 'AAAInvalid'); -- invalid FK course_id 
INSERT INTO review(student_id, review) VALUES (846200000, 'the review for this course'); -- invalid FK student_id

INSERT INTO student_registration(final_result) VALUES ('95'); -- missing PK
INSERT INTO student_registration(course_id, final_result) VALUES ('AAA_2013J', '95'); -- missing PK student_id
INSERT INTO student_registration(student_id, final_result) VALUES (8462, '95'); -- missing PK course_id
INSERT INTO student_registration(student_id, course_id, final_result) VALUES (8462, 'AAAInvalid', '95'); -- invalid FK course_id
INSERT INTO student_registration(student_id, course_id, final_result) VALUES (84620000, 'AAA_2013J', '95'); -- invalid FK student_id

INSERT INTO assessment(weight) VALUES (20); -- missing PK
INSERT INTO assessment(course_id, weight) VALUES ('AAA_2013J', 20); -- missing PK
INSERT INTO assessment(assessment_id, course_id, weight) VALUES (10000, 'invalid' 20); -- invalid FK course_id

INSERT INTO student_assessment(score) VALUES (95); -- missing PK
INSERT INTO student_assessment(assessment_id, score) VALUES (10000, 96); -- missing PK student_id
INSERT INTO student_assessment(student_id, score) VALUES (8462, 97); -- missing PK assessment_id
INSERT INTO student_assessment(student_id, assessment_id, score) VALUES (84620000, 1757, 97); -- invalid FK student_id
INSERT INTO student_assessment(student_id, assessment_id, score) VALUES (8462, 1, 97); -- invalid FK assessment_id
-- none of the above queries should pass

-------------------------- Data Loading Tests ---------------------------
-- if duplicate student information has been removed successfully
SELECT count(*) from studentInfo;
SELECT count(DISTINCT id_student) from studentInfo;
-- check all the tables
SELECT * from instructor limit 10;
SELECT * from course limit 10;
SELECT * from student limit 10;
SELECT * from review limit 10;
SELECT * from student_registration limit 10;
SELECT * from assessment limit 10;
SELECT * from student_assessment limit 10;







