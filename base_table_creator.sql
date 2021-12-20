CREATE TABLE courses (
    code_module varchar(45),
    code_presentation varchar(45),
    module_presentation_length int
);

CREATE TABLE assessments (
    code_module varchar(45),
    code_presentation varchar(45),
    id_assessment int,
    assessment_type varchar(45),
    date int,
    weight int
);

CREATE TABLE studentRegistration (
    code_module varchar(45),
    code_presentation varchar(45),
    id_student int,
    date_registration int,
    date_unregistration int
);

CREATE TABLE studentAssessment (
    id_assessment int,
    id_student int,
    date_submitted int,
    is_banked tinyint,
    score int
);

CREATE TABLE studentInfo (
    code_module varchar(45),
    code_presentation varchar(45),
    id_student int,
    gender varchar(45),
    region varchar(45),
    highest_education varchar(45),
    imd_band varchar(45),
    age_band varchar(45),
    num_of_prev_attempts int,
    studied_credits int,
    disability varchar(45),
    final_result varchar(45)
);

CREATE TABLE studentVle (
    code_module varchar(45),
    code_presentation varchar(45),
    id_student int,
    id_site int,
    date int,
    sum_click int
);

CREATE TABLE vle (
    id_site int,
    code_module varchar(45),
    code_presentation varchar(45),
    activity_type varchar(45),
    week_from int,
    week_to int
);
