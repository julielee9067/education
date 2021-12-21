from datetime import date
from typing import Dict

import mysql.connector
import sshtunnel
from mysql.connector import IntegrityError

from client.secret_constants import SSH_HOST, SSH_USERNAME, SSH_PASSWORD, HOST, DB_USERNAME, DB_PASSWORD, DB_NAME


def open_ssh_tunnel():
    global tunnel

    tunnel = sshtunnel.SSHTunnelForwarder(
        (SSH_HOST, 22),
        ssh_username=SSH_USERNAME,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(HOST, 3306)
    )

    tunnel.start()


class EducationClient:
    def __init__(self):
        self.education = mysql.connector.connect(
            host=HOST,
            user=DB_USERNAME,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.education.cursor(buffered=True, dictionary=True)

    def get_student_info_for_course(self, student_id: int, course_id: str) -> Dict:
        self.get_course_info(course_id=course_id)
        query = f"""
            SELECT * FROM student_registration
            WHERE student_id = {student_id} AND course_id = '{course_id}';
        """
        self.cursor.execute(query)
        student_info = self.cursor.fetchone()
        self.education.commit()
        if student_info is None:
            raise Exception(f"Student info is not found for the course {course_id}")
        return student_info

    def get_student_info_for_assessment(self, student_id: int, assessment_id: int) -> Dict:
        self.get_assessment_info(assessment_id=assessment_id)
        query = f"""
            SELECT * FROM student_assessment
            WHERE student_id = {student_id} AND assessment_id = {assessment_id};
        """
        self.cursor.execute(query)
        student_info = self.cursor.fetchone()
        self.education.commit()
        print(student_info)
        if student_info is None:
            raise Exception(f"Student info is not found for the assessment {assessment_id}")

        return student_info

    def get_student_grade_for_assessment(self, student_id: int, assessment_id: int) -> int:
        grade = self.get_student_info_for_assessment(student_id=student_id, assessment_id=assessment_id)["score"]
        print(f"Student {student_id} has grade {grade} for assessment {assessment_id}")
        return grade

    def get_student_status_for_course(self, student_id: int, course_id: str) -> str:
        self.get_course_info(course_id=course_id)
        query = f"""
            SELECT final_result FROM student_registration
            WHERE student_id = {student_id} AND course_id = '{course_id}';
        """
        self.cursor.execute(query)
        status = self.cursor.fetchone()
        self.education.commit()
        if status is None:
            raise Exception(f"The student {student_id} did not take the course {course_id}")
        print(f"Student {student_id} has grade {status['final_result']} for course {course_id}")
        return status["final_result"]

    def get_course_info(self, course_id: str) -> Dict:
        check_course_query = f"""
            SELECT course_id FROM course WHERE course_id='{course_id}';
        """
        self.cursor.execute(check_course_query)
        course_info = self.cursor.fetchone()
        if course_info is None:
            raise Exception(f"The given course is not found: {course_id}")
        return course_info

    def get_assessment_info(self, assessment_id: int) -> Dict:
        check_course_query = f"""
            SELECT assessment_id FROM assessment WHERE assessment_id='{assessment_id}';
        """
        self.cursor.execute(check_course_query)
        assessment_info = self.cursor.fetchone()
        if assessment_info is None:
            raise Exception(f"The given assessment is not found: {assessment_id}")
        return assessment_info

    def register_student_for_course(self, student_id: int, course_id: str, is_new_student: bool = False) -> None:
        if not is_new_student:
            student_info = self.get_student_info_for_course(student_id=student_id, course_id=course_id)
            if student_info["is_registered"] == 1:
                raise Exception(f"Student is already registered to {course_id}")

            num_prev_attempt = student_info["num_of_prev_attempts"]
        else:
            num_prev_attempt = 0
        query = f"""
            INSERT INTO student_registration (student_id, course_id, is_registered, num_of_prev_attempts, final_result)
            VALUES ({student_id}, '{course_id}', TRUE, {num_prev_attempt}, NULL);
        """
        self.cursor.execute(query)
        self.education.commit()
        print(f"Successfully registered student {student_id} for a course {course_id}")

    def unregister_student_from_course(self, student_id: int, course_id: str) -> None:
        self.get_student_info_for_course(student_id=student_id, course_id=course_id)
        query = f"""
            UPDATE student_registration SET is_registered=FALSE 
            WHERE course_id='{course_id}' AND student_id={student_id};
        """
        self.cursor.execute(query)
        self.education.commit()
        print(f"Successfully unregistered student {student_id} for a course {course_id}")

    def post_review(self, course_id: str, review_content: str, student_id: int, rating: int) -> None:
        self.get_student_info_for_course(student_id=student_id, course_id=course_id)
        query = f"""
            INSERT INTO review (review, course_id, student_id, date, rating)
            VALUE ('{review_content}', '{course_id}', {student_id}, '{date.today()}', {rating});
        """
        self.cursor.execute(query)
        self.education.commit()
        print(f"Successfully posted review for a course {course_id} with rating {rating}")

    def get_average_grade_for_assessment(self, assessment_id: int) -> float:
        self.get_assessment_info(assessment_id=assessment_id)
        query = f"""
            SELECT AVG(score) AS average_score FROM student_assessment 
            WHERE assessment_id = {assessment_id};
        """
        self.cursor.execute(query)
        average = self.cursor.fetchone()
        self.education.commit()
        print(f"The average grade is {average['average']}% for an assessment: {assessment_id}")
        return average["average"]

    def get_num_student_registered(self, course_id: str) -> int:
        self.get_course_info(course_id=course_id)
        query = f"""
            SELECT COUNT(student_id) AS count FROM student_registration
            WHERE course_id='{course_id}' AND IS_REGISTERED=TRUE;
        """
        self.cursor.execute(query)
        count = self.cursor.fetchone()
        self.education.commit()
        print(f"Total of {count['count']} registered students found for a course: {course_id}")
        return count["count"]

    def get_num_student_unregistered(self, course_id: str) -> int:
        self.get_course_info(course_id=course_id)
        query = f"""
            SELECT COUNT(student_id) AS count FROM student_registration
            WHERE course_id='{course_id}' AND IS_REGISTERED=FALSE;
        """
        self.cursor.execute(query)
        count = self.cursor.fetchone()
        self.education.commit()
        print(f"Total of {count['count']} unregistered students found for a course: {course_id}")
        return count["count"]

    def get_num_assessment_for_course(self, course_id: str) -> int:
        self.get_course_info(course_id=course_id)
        query = f"""
            SELECT COUNT(assessment_id) AS count FROM assessment 
            WHERE course_id='{course_id}';
        """
        self.cursor.execute(query)
        count = self.cursor.fetchone()
        self.education.commit()
        print(f"Total of {count['count']} assessments found for a course: {course_id}")
        return count["count"]

    def modify_grade_for_assessment(self, assessment_id: int, student_id: int, new_grade: int) -> None:
        self.get_student_info_for_assessment(student_id=student_id, assessment_id=assessment_id)
        query = f"""
            UPDATE student_assessment SET score={new_grade} 
            WHERE assessment_id={assessment_id} AND student_id={student_id};
        """
        self.cursor.execute(query)
        self.education.commit()
        print(f"Successfully modified an assessment grade to {new_grade} for student {student_id}, for assessment: {assessment_id}")

    def modify_status_for_course(self, course_id: str, student_id: int, new_status: str) -> None:
        self.get_student_info_for_course(course_id=course_id, student_id=student_id)
        query = f"""
            UPDATE student_registration SET final_result='{new_status}'
            WHERE course_id='{course_id}' AND student_id={student_id};
        """
        self.cursor.execute(query)
        self.education.commit()
        print(f"Successfully modified a status to {new_status} for student {student_id}, for course: {course_id}")

    def get_average_rating_for_course(self, course_id: str) -> float:
        self.get_course_info(course_id=course_id)
        query = f"""
            SELECT AVG(rating) AS average_rating FROM review 
            WHERE course_id = '{course_id}';
        """
        self.cursor.execute(query)
        average = self.cursor.fetchone()
        self.education.commit()
        print(f"The average rating is {average['average_rating']} for a course: {course_id}")
        return average["average_rating"]


if __name__ == "__main__":
    client = EducationClient()
    info = client.get_student_info_for_course(student_id=123, course_id="AAA_2013J")
    print(info)
