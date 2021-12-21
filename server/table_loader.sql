-- If the tables are created already, This is to only load data to our tables
INSERT INTO course (course_id)
SELECT concat(code_module, '_', code_presentation) as course_id,
code_module, code_presentation FROM courses;

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

INSERT INTO student_registration (student_id, course_id, is_registered, num_of_prev_attempts, final_result) 
SELECT studentRegistration.id_student, concat(studentRegistration.code_module, '_', studentRegistration.code_presentation) AS course_id, 
(date_unregistration IS NULL) AS is_registered, num_of_prev_attempts, final_result 
FROM ( 
    studentInfo INNER JOIN studentRegistration on  
    (studentInfo.id_student = studentRegistration.id_student 
    AND studentInfo.code_module = studentRegistration.code_module 
    AND studentInfo.code_presentation = studentRegistration.code_presentation) 
);