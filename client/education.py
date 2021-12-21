from datetime import date

import mysql.connector
import sshtunnel

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
        self.cursor = self.education.cursor(buffered=True)

    def register_student_for_course(self, student_id: int, course_id: str) -> None:
        num_prev_attempt_query = f"""
            SELECT num_of_prev_attempts FROM student_registration 
            WHERE student_id = {student_id} AND course_id = '{course_id}';
        """
        self.cursor.execute(num_prev_attempt_query)
        num_prev_attempt = self.cursor.fetchone()
        self.education.commit()
        num_prev_attempt = num_prev_attempt[0] if num_prev_attempt is not None else 0
        print(f"Student found with number of previous attempt: {num_prev_attempt}")
        query = f"""
            INSERT INTO student_registration (student_id, course_id, is_registered, num_of_prev_attempts, final_result)
            VALUES ({student_id}, '{course_id}', TRUE, {num_prev_attempt}, NULL);
        """
        self.cursor.execute(query)
        self.education.commit()
        print(f"Successfully registered student {student_id} for a course {course_id}")

    def unregister_student_from_course(self, student_id: int, course_id: str) -> None:
        query = f"""
            UPDATE student_registration SET is_registered=FALSE 
            WHERE course_id='{course_id}' AND student_id={student_id};
        """
        self.cursor.execute(query)
        self.education.commit()
        print(f"Successfully unregistered student {student_id} for a course {course_id}")

    def post_review(self, course_id: str, review_content: str, student_id: int, rating: int) -> None:
        student_query = f"""
            SELECT student_id FROM student_registration WHERE course_id = '{course_id}' AND student_id = {student_id};
        """
        self.cursor.execute(student_query)
        student = self.cursor.fetchone()
        self.education.commit()

        if student is not None:
            query = f"""
                INSERT INTO review (review, course_id, student_id, date, rating)
                VALUE ('{review_content}', '{course_id}', {student_id}, '{date.today()}', {rating});
            """
            self.cursor.execute(query)
            self.education.commit()
            print(f"Successfully posted review for a course {course_id} with rating {rating}")

        else:
            print("You can only post a review after taking the course.")

    def get_average_grade_for_assessment(self, assessment_id: int) -> float:
        query = f"""
            SELECT AVG(score) AS average_score FROM student_assessment WHERE assessment_id = {assessment_id};
        """
        self.cursor.execute(query)
        average = self.cursor.fetchone()
        self.education.commit()
        print(f"The average grade is {average[0]}% for an assessment: {assessment_id}")
        return average[0]

    def get_num_student_registered(self, course_id: str) -> int:
        query = f"""
            SELECT COUNT(student_id) FROM student_registration WHERE course_id='{course_id}' AND IS_REGISTERED=TRUE;
        """
        self.cursor.execute(query)
        count = self.cursor.fetchone()
        self.education.commit()
        print(f"Total of {count[0]} registered students found for a course: {course_id}")
        return count[0]

    def get_num_student_unregistered(self, course_id: str) -> int:
        query = f"""
            SELECT COUNT(student_id) FROM student_registration WHERE course_id='{course_id}' AND IS_REGISTERED=FALSE;
        """
        self.cursor.execute(query)
        count = self.cursor.fetchone()
        self.education.commit()
        print(f"Total of {count[0]} unregistered students found for a course: {course_id}")
        return count[0]

    def get_num_assessment_for_course(self, course_id: str) -> int:
        query = f"""
            SELECT COUNT(assessment_id) FROM assessment WHERE course_id='{course_id}';
        """
        self.cursor.execute(query)
        count = self.cursor.fetchone()
        self.education.commit()
        print(f"Total of {count[0]} assessments found for a course: {course_id}")
        return count[0]

    def modify_grade_for_assessment(self, assessment_id: int, student_id: int, new_grade: int) -> None:
        query = f"""
            UPDATE student_assessment SET score={new_grade} 
            WHERE assessment_id={assessment_id} AND student_id={student_id};
        """
        self.cursor.execute(query)
        self.education.commit()
        print(f"Successfully modified an assessment grade to {new_grade} for student {student_id}, for assessment: {assessment_id}")

    def modify_status_for_course(self, course_id: str, student_id: int, new_status: str) -> None:
        query = f"""
            UPDATE student_registration SET final_result='{new_status}'
            WHERE course_id='{course_id}' AND student_id={student_id};
        """
        self.cursor.execute(query)
        self.education.commit()
        print(f"Successfully modified a status to {new_status} for student {student_id}, for course: {course_id}")

    def get_average_rating_for_course(self, course_id: str) -> float:
        query = f"""
            SELECT AVG(rating) AS average_rating FROM review WHERE course_id = '{course_id}';
        """
        self.cursor.execute(query)
        average = self.cursor.fetchone()
        self.education.commit()
        print(f"The average rating is {average[0]} for a course: {course_id}")
        return average[0]
