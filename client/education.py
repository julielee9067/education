from datetime import date

import mysql.connector
import sshtunnel

from secret_constants import SSH_HOST, SSH_USERNAME, SSH_PASSWORD, LOCALHOST, DB_USERNAME, DB_PASSWORD, DB_NAME


def open_ssh_tunnel():
    global tunnel

    tunnel = sshtunnel.SSHTunnelForwarder(
        (SSH_HOST, 22),
        ssh_username=SSH_USERNAME,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(LOCALHOST, 3306)
    )

    tunnel.start()


class EducationClient:
    def __init__(self):
        self.education = mysql.connector.connect(
            host=LOCALHOST,
            user=DB_USERNAME,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.education.cursor(buffered=True)

    def register_student_for_ou_course(self, student_id: str, course_id: str) -> None:
        num_prev_attempt_query = f"""
            SELECT num_of_prev_attempts FROM student_registration 
            WHERE student_id = {student_id} AND course_id = {course_id};
        """
        self.cursor.execute(num_prev_attempt_query)
        num_prev_attempt = self.cursor.fetchone() if self.cursor.fetchone() else 0

        query = f"""
            INSERT INTO student_registration (student_id, course_id, is_registered, num_of_prev_attempts, final_result)
            VALUES ({student_id}, {course_id}, TRUE, {num_prev_attempt}, NULL);
        """
        self.cursor.execute(query)

    def unregister_student_from_ou_course(self, student_id: str, course_id: str) -> None:
        query = f"""
            DELETE FROM student_registration WHERE student_id = {student_id} AND course_id = {course_id};
        """
        self.cursor.execute(query)

    def post_review(self, course_id: str, review_content: str, reviewer: str, rating: int) -> None:
        query = f"""
            INSERT INTO review (review, course_id, reviewer, date, rating)
            VALUE ({review_content}, {course_id}, {reviewer}, {date.today()}, {rating});
        """
        self.cursor.execute(query)

    def get_average_grade_for_assessment(self, assessment_id: int) -> float:
        query = f"""
            
        """
        self.cursor.execute(query)
