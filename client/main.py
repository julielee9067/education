import argparse

from education import EducationClient


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    #
    # parser.add_argument(
    #     "-a",
    #     dest="action",
    #     type=str,
    #     help="The action a user can take"
    # )

    group.add_argument(
        "--register",
        action="store_true",
        help="Register student to a open university course"
    )

    group.add_argument(
        "--unregister",
        action="store_true",
        help="Unregister student to a open university course"
    )

    group.add_argument(
        "--average_rating",
        action="store_true",
        help="Get average review rating for a course"
    )

    group.add_argument(
        "--average_assessment",
        action="store_true",
        help="Get average grade for an assessment"
    )

    group.add_argument(
        "--get_num_registered",
        action="store_true",
        help="Get number of registered students for a course"
    )

    group.add_argument(
        "--get_num_unregistered",
        action="store_true",
        help="Get number of unregistered students for a course"
    )

    group.add_argument(
        "--get_num_assessments",
        action="store_true",
        help="Get number of assessments for a course"
    )

    group.add_argument(
        "--post_review",
        action="store_true",
        help="Post a review for a course"
    )

    group.add_argument(
        "--modify_grade",
        action="store_true",
        help="Modify grade for an assessment"
    )

    parser.add_argument(
        "--rating",
        dest="rating",
        type=int,
        help="Retrieving rating for a review"
    )

    parser.add_argument(
        "--student_id",
        dest="student_id",
        type=int,
        help="Retrieving student ID"
    )

    parser.add_argument(
        "--course_id",
        dest="course_id",
        type=str,
        help="Retrieving course ID"
    )

    parser.add_argument(
        "--assessment_id",
        dest="assessment_id",
        type=int,
        help="Retrieving assessment ID"
    )

    parser.add_argument(
        "--review",
        dest="review",
        type=str,
        help="Insert review content for a course review"
    )

    parser.add_argument(
        "--grade",
        dest="new_grade",
        type=int,
        help="Insert new grade for a student's assessment"
    )

    parser.add_argument(
        "--status",
        dest="new_status",
        type=str,
        help="Insert new status for a student's course"
    )

    args = parser.parse_args()
    client = EducationClient()
    if args.register:
        if args.student_id is None or args.course_id is None:
            raise ValueError("Valid student ID and course ID are required for this operation.")
        client.register_student_for_course(student_id=args.student_id, course_id=args.course_id)

    if args.unregister:
        if args.student_id is None or args.course_id is None:
            raise ValueError("Valid student ID and course ID are required for this operation.")
        client.unregister_student_from_course(student_id=args.student_id, course_id=args.course_id)

    if args.post_review:
        if args.student_id is None or args.course_id is None or args.review is None or args.rating is None:
            raise ValueError("Valid student ID, course ID, review content, and rating are required for this operation.")
        client.post_review(
            course_id=args.course_id,
            review_content=args.review,
            student_id=args.student_id,
            rating=args.rating
        )

    if args.average_assessment:
        if args.assessment_id is None:
            raise ValueError("Valid assessment ID is required for this operation.")
        client.get_average_grade_for_assessment(assessment_id=args.assessment_id)

    if args.get_num_registered:
        if args.course_id is None:
            raise ValueError("Valid course ID is required for this operation.")
        client.get_num_student_registered(course_id=args.course_id)

    if args.get_num_unregistered:
        if args.coures_id is None:
            raise ValueError("Valid course ID is required for this operation.")
        client.get_num_student_unregistered(course_id=args.course_id)

    if args.get_num_assessments:
        if args.course_id is None:
            raise ValueError("Valid course ID is required for this operation.")
        client.get_num_assessment_for_course(course_id=args.course_id)

    if args.modify_grade:
        if args.assessment_id is None or args.student_id is None or args.new_grade is None:
            raise ValueError("Valid assessment ID, student ID, and new grade is required for this operation.")
        client.modify_grade_for_assessment(
            assessment_id=args.assessment_id,
            student_id=args.student_id,
            new_grade=args.new_grade
        )

    if args.modify_status:
        if args.course_id is None or args.student_id is None or args.new_status is None:
            raise ValueError("Valid course ID, student ID, and new status is required for this operation.")
        client.modify_status_for_course(
            course_id=args.course_id,
            student_id=args.student_id,
            new_status=args.new_status
        )

    if args.average_rating:
        if args.course_id is None:
            raise ValueError("Valid course ID is required for this operation.")
        client.get_average_rating_for_course(course_id=args.course_id)


if __name__ == "__main__":
    main()
