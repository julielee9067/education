## Set up
`secret_constant.py` file must be in client folder
```
SSH_HOST = "eceUbuntu.uwaterloo.ca"
SSH_USERNAME = "{USERNAME}"
SSH_PASSWORD = "{PASSWORD}"
DB_USERNAME = "{DB USERNAME}"
DB_PASSWORD = "{DB PASSWORD}"
DB_NAME = "{DB NAME}"
HOST = "marmoset04.shoshin.uwaterloo.ca"
```

## Questions
### From students’ perspective
- Get the number of assessments they need to complete for a specific course
- Post a review for a course if they took the course
- Get average rating for a course
- Show reviews for a course
- Get instructor for a course

### From professors’ perspective
- Change student’s grade for a assessment
- Change student's status for a course
- Get average grade for an assessment

### From admin’s perspective
- Register/unregister students from a course
- Show the number of students registered/unregistered from a course

## Example commands
- Register a student for a course
  - `python client/main.py --register --course_id AAA_2013J --student_id 62487`
  - `python client/main.py --register --course_id AAA_2013J --student_id 6516`
- Unregister a student for a course
  - `python client/main.py --unregister --course_id AAA_2013J --student_id 62487`
- Post a review for a course
  - `python client/main.py --post_review --course_id AAA_2013J --student_id 62487 --review 'good course' --rating 4`
- Get average grade for an assessment
  - `python client/main.py --average_assessment --assessment_id 1752`
- Get number of registered student for a course
  - `python client/main.py --get_num_registered --course_id AAA_2013J`
- Get number of unregistered student for a course
  - `python client/main.py --get_num_unregistered --course_id AAA_2013J`
- Get number of assessment for a course
  - `python client/main.py --get_num_assessments --course_id AAA_2013J`
- Modify grade:
  - `python client/main.py --modify_grade --assessment_id 1752 --student_id 11391 --grade 100`
  - `python client/main.py --modify_grade --assessment_id 1752 --student_id 11391 --grade 50`
- Modify status:
  - `python client/main.py --modify_status --course_id AAA_2013J --student_id 62487 --status Fail`
  - `python client/main.py --modify_status --course_id AAA_2013J --student_id 62487 --status Pass`
- Get average rating for a course
  - `python client/main.py --average_rating --course_id AAA_2013J`
- Get review for a course
  - `python client/main.py --show_review --course_id AAA_2013J`
- Get instructor name for a course
  - `python client/main.py --get_instructor --course_id AAA_2013J`
