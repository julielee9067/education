LOAD DATA INFILE '/var/lib/mysql-files/26-Education/OU/assessments.csv'
INTO TABLE assessments
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(code_module, code_presentation, id_assessment, assessment_type, @date, @weight)
SET date = NULLIF(@date, ''),
    weight = NULLIF(@weight, '');

LOAD DATA INFILE '/var/lib/mysql-files/26-Education/OU/courses.csv'
INTO TABLE courses
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA INFILE '/var/lib/mysql-files/26-Education/OU/studentRegistration.csv'
INTO TABLE studentRegistration
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(code_module, code_presentation, id_student, @date_registration, @date_unregistration)
SET date_registration = NULLIF(@date_registration, ''),
    date_unregistration = NULLIF(@date_unregistration, '');

LOAD DATA INFILE '/var/lib/mysql-files/26-Education/OU/studentAssessment.csv'
INTO TABLE studentAssessment
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(id_assessment, id_student, date_submitted, is_banked, @score)
SET score = NULLIF(@score, '');

LOAD DATA INFILE '/var/lib/mysql-files/26-Education/OU/studentInfo.csv'
INTO TABLE studentInfo
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(code_module, code_presentation, id_student, gender, region, highest_education, imd_band, age_band, num_of_prev_attempts, studied_credits, disability, final_result);

LOAD DATA INFILE '/var/lib/mysql-files/26-Education/OU/studentVle.csv'
INTO TABLE studentVle
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(code_module, code_presentation, id_student, id_site, @date, sum_click)
SET date = NULLIF(@date, '');

LOAD DATA INFILE '/var/lib/mysql-files/26-Education/OU/vle.csv'
INTO TABLE vle
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(id_site, code_module, code_presentation, activity_type, @week_from, @week_to)
SET week_from = NULLIF(@week_from, ''),
    week_to = NULLIF(@week_to, '');
