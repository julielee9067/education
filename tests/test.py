import random
import unittest

from mysql.connector import ProgrammingError

from client.education import EducationClient


class TestClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client = EducationClient()
        self.course_id = "AAA_2013J"
        self.assessment_id = 1752
        self.unknown_course_id = "RANDOM"

    def get_one_new_student(self, course_id: str) -> int:
        query = f"""
            SELECT student_id FROM student_registration 
            WHERE student_id NOT IN 
            (SELECT student_id from student_registration WHERE course_id = '{course_id}') LIMIT 1;
        """
        self.client.cursor.execute(query)
        student_id = self.client.cursor.fetchone()
        self.client.education.commit()
        return student_id["student_id"]

    def get_one_registered_student(self, course_id: str) -> int:
        query = f"""
            SELECT student_id from student_registration 
            WHERE course_id = '{course_id}' AND is_registered = TRUE LIMIT 1;
        """
        self.client.cursor.execute(query)
        student_id = self.client.cursor.fetchone()
        self.client.education.commit()
        return student_id["student_id"]

    def get_one_unregistered_student(self, course_id: str) -> int:
        query = f"""
            SELECT student_id FROM student_registration 
            WHERE course_id = '{course_id}' AND is_registered != TRUE LIMIT 1;
        """
        self.client.cursor.execute(query)
        student_id = self.client.cursor.fetchone()
        self.client.education.commit()
        return student_id["student_id"]

    def get_one_student_with_assessment(self, assessment_id: int) -> int:
        query = f"""
            SELECT student_id from student_assessment
            WHERE assessment_id = {assessment_id} LIMIT 1;
        """
        self.client.cursor.execute(query)
        student_id = self.client.cursor.fetchone()
        self.client.education.commit()
        return student_id["student_id"]

    def get_one_student_without_assessment(self, assessment_id: int) -> int:
        query = f"""
            SELECT student_id from student_assessment
            WHERE student_id NOT IN
            (SELECT student_id FROM student_assessment WHERE assessment_id = {assessment_id}) LIMIT 1;
        """
        self.client.cursor.execute(query)
        student_id = self.client.cursor.fetchone()
        self.client.education.commit()
        return student_id["student_id"]

    def get_num_review(self, student_id: int, course_id: str) -> int:
        query = f"""
            SELECT COUNT(review_id) AS count FROM review
            WHERE student_id = {student_id} AND course_id = '{course_id}';
        """
        self.client.cursor.execute(query)
        result = self.client.cursor.fetchone()
        self.client.education.commit()
        return result["count"]

    def test_register_student_for_course(self):
        # Test registering invalid student ID
        with self.assertRaises(Exception):
            self.client.register_student_for_course(student_id=-1, course_id=self.course_id)

        # Test registering new valid student
        student_id = self.get_one_new_student(course_id=self.course_id)
        num_student_before = self.client.get_num_student_registered(course_id=self.course_id)
        self.client.register_student_for_course(student_id=student_id, course_id=self.course_id, is_new_student=True)
        num_student_after = self.client.get_num_student_registered(course_id=self.course_id)
        self.assertEqual(num_student_before + 1, num_student_after)

        # Test registering existing student
        student_id = self.get_one_registered_student(course_id=self.course_id)
        num_student_before = self.client.get_num_student_registered(course_id=self.course_id)
        with self.assertRaises(Exception):
            self.client.register_student_for_course(student_id=student_id, course_id=self.course_id)
        num_student_after = self.client.get_num_student_registered(course_id=self.course_id)
        self.assertEqual(num_student_before, num_student_after)

    def test_unregister_student_from_course(self):
        # Test unregistering invalid student ID
        with self.assertRaises(Exception):
            self.client.unregister_student_from_course(student_id=-1, course_id=self.course_id)

        # Test unregistering registered student
        student_id = self.get_one_registered_student(course_id=self.course_id)
        num_student_before = self.client.get_num_student_unregistered(course_id=self.course_id)
        self.client.unregister_student_from_course(student_id=student_id, course_id=self.course_id)
        num_student_after = self.client.get_num_student_unregistered(course_id=self.course_id)
        self.assertEqual(num_student_before + 1, num_student_after)

        # Test unregistering already unregistered student
        student_id = self.get_one_unregistered_student(course_id=self.course_id)
        num_student_before = self.client.get_num_student_unregistered(course_id=self.course_id)
        self.client.unregister_student_from_course(student_id=student_id, course_id=self.course_id)
        num_student_after = self.client.get_num_student_unregistered(course_id=self.course_id)
        self.assertEqual(num_student_before, num_student_after)

    def test_post_review(self):
        student_id = self.get_one_registered_student(course_id=self.course_id)
        review_content = "test review"
        review_rating = 3

        # Test posting a valid review
        num_review_before = self.get_num_review(student_id=student_id, course_id=self.course_id)
        self.client.post_review(
            course_id=self.course_id,
            student_id=student_id,
            review_content=review_content,
            rating=review_rating
        )
        num_review_after = self.get_num_review(student_id=student_id, course_id=self.course_id)
        self.assertEqual(num_review_before + 1, num_review_after)

        # Test posting a review without rating
        with self.assertRaises(ProgrammingError):
            self.client.post_review(
                course_id=self.course_id,
                student_id=student_id,
                review_content=review_content,
                rating=None
            )

        # Test posting a review without review content
        num_review_before = self.get_num_review(student_id=student_id, course_id=self.course_id)
        self.client.post_review(
            course_id=self.course_id,
            student_id=student_id,
            review_content=None,
            rating=review_rating
        )
        num_review_after = self.get_num_review(student_id=student_id, course_id=self.course_id)
        self.assertEqual(num_review_before + 1, num_review_after)

        # Test posting a review without taking the course
        student_id = self.get_one_new_student(course_id=self.course_id)
        review_content = "test review new student"
        review_rating = 4
        num_review_before = self.get_num_review(student_id=student_id, course_id=self.course_id)
        with self.assertRaises(Exception):
            self.client.post_review(
                course_id=self.course_id,
                student_id=student_id,
                review_content=review_content,
                rating=review_rating
            )
        num_review_after = self.get_num_review(student_id=student_id, course_id=self.course_id)
        self.assertEqual(num_review_before, num_review_after)

    def test_get_num_student_registered(self):
        # Test getting number of student registered for unknown course
        with self.assertRaises(Exception):
            self.client.get_num_student_registered(course_id=self.unknown_course_id)

    def test_get_num_student_unregistered(self):
        # Test getting number of student unregistered for unknown course
        with self.assertRaises(Exception):
            self.client.get_num_student_unregistered(course_id=self.unknown_course_id)

    def test_get_num_assessment_for_course(self):
        # Test getting number of assessment for unknown course
        with self.assertRaises(Exception):
            self.client.get_num_assessment_for_course(course_id=self.unknown_course_id)

    def test_modify_grade_for_assessment(self):
        student_id = self.get_one_registered_student(course_id=self.course_id)
        new_grade = 70
        # Test modifying unknown assessment
        with self.assertRaises(Exception):
            self.client.modify_grade_for_assessment(assessment_id=0, student_id=student_id, new_grade=new_grade)

        # Test modifying grade for unregistered student
        student_id = self.get_one_student_without_assessment(assessment_id=self.assessment_id)
        with self.assertRaises(Exception):
            self.client.modify_grade_for_assessment(assessment_id=self.assessment_id, student_id=student_id, new_grade=new_grade)

        # Test modifying grade for registered student
        student_id = self.get_one_student_with_assessment(assessment_id=self.assessment_id)
        original_grade = self.client.get_student_grade_for_assessment(
            student_id=student_id,
            assessment_id=self.assessment_id
        )
        new_grade = random.choice(list(range(0, original_grade)) + list(range(original_grade + 1, 100)))
        self.client.modify_grade_for_assessment(
            assessment_id=self.assessment_id,
            student_id=student_id,
            new_grade=new_grade
        )
        changed_grade = self.client.get_student_grade_for_assessment(
            student_id=student_id,
            assessment_id=self.assessment_id
        )
        self.assertEqual(new_grade, changed_grade)
        self.assertNotEqual(original_grade, changed_grade)

    def test_modify_status_for_course(self):
        student_id = self.get_one_registered_student(course_id=self.course_id)
        new_status = "Fail"
        # Test modifying unknown assessment
        with self.assertRaises(Exception):
            self.client.modify_status_for_course(
                course_id=self.unknown_course_id,
                student_id=student_id,
                new_status=new_status
            )

        # Test modifying grade for unregistered student
        student_id = self.get_one_new_student(course_id=self.course_id)
        with self.assertRaises(Exception):
            self.client.modify_status_for_course(
                course_id=self.course_id,
                student_id=student_id,
                new_status=new_status
            )

        # Test modifying grade for registered student
        student_id = self.get_one_registered_student(course_id=self.course_id)
        new_status = random.choice(["Fail, Pass, Withdrawn"])
        self.client.modify_status_for_course(
            course_id=self.course_id,
            student_id=student_id,
            new_status=new_status
        )
        changed_status = self.client.get_student_status_for_course(
            student_id=student_id,
            course_id=self.course_id
        )
        self.assertEqual(new_status, changed_status)

    def test_get_average_rating_for_course(self):
        # Test getting average rating for unknown course
        with self.assertRaises(Exception):
            self.client.get_average_rating_for_course(course_id=self.unknown_course_id)

    def test_show_review_for_course(self):
        # Test getting review for unknown course
        with self.assertRaises(Exception):
            self.client.show_review_for_course(course_id=self.unknown_course_id)

    def test_get_instructor_info_for_course(self):
        # Test getting instructor information for unknown course
        with self.assertRaises(Exception):
            self.client.get_instructor_info_for_course(course_id=self.unknown_course_id)

        # Test getting valid instructor
        instructor_info = self.client.get_instructor_info_for_course(course_id=self.course_id)
        self.assertEqual("John", instructor_info["first_name"])
        self.assertEqual("Smith", instructor_info["last_name"])
