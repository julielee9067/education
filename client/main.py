import argparse
from typing import List

from client.education import EducationClient


def create_parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

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

    group.add_argument(
        "--modify_status",
        action="store_true",
        help="Modify status for a course"
    )

    group.add_argument(
        "--show_review",
        action="store_true",
        help="Show reviews for a course"
    )

    group.add_argument(
        "--get_instructor",
        action="store_true",
        help="Get instructor for a course"
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

    parser.add_argument(
        "--new",
        dest="is_new_student",
        type=bool,
        default=False,
        help="Indicate if the student is new to the course"
    )

    return parser


def check_arg(args: List) -> None:
    if None in args:
        raise Exception("Valid arguments are required for this operation.")


def main():
    parser = create_parser()
    args = parser.parse_args()
    client = EducationClient()
    if args.register:
        check_arg([args.student_id, args.course_id])
        client.register_student_for_course(
            student_id=args.student_id,
            course_id=args.course_id,
            is_new_student=args.is_new_student
        )

    if args.unregister:
        check_arg([args.student_id, args.course_id])
        client.unregister_student_from_course(student_id=args.student_id, course_id=args.course_id)

    if args.post_review:
        check_arg([args.student_id, args.course_id, args.rating])
        client.post_review(
            course_id=args.course_id,
            review_content=args.review,
            student_id=args.student_id,
            rating=args.rating
        )

    if args.average_assessment:
        check_arg([args.assessment_id])
        client.get_average_grade_for_assessment(assessment_id=args.assessment_id)

    if args.get_num_registered:
        check_arg([args.course_id])
        client.get_num_student_registered(course_id=args.course_id)

    if args.get_num_unregistered:
        check_arg([args.course_id])
        client.get_num_student_unregistered(course_id=args.course_id)

    if args.get_num_assessments:
        check_arg([args.course_id])
        client.get_num_assessment_for_course(course_id=args.course_id)

    if args.modify_grade:
        check_arg([args.assessment_id, args.student_id, args.new_grade])
        client.modify_grade_for_assessment(
            assessment_id=args.assessment_id,
            student_id=args.student_id,
            new_grade=args.new_grade
        )

    if args.modify_status:
        check_arg([args.course_id, args.student_id, args.new_status])
        client.modify_status_for_course(
            course_id=args.course_id,
            student_id=args.student_id,
            new_status=args.new_status
        )

    if args.average_rating:
        check_arg([args.course_id])
        client.get_average_rating_for_course(course_id=args.course_id)

    if args.show_review:
        check_arg([args.course_id])
        client.show_review_for_course(course_id=args.course_id)

    if args.get_instructor:
        check_arg([args.course_id])
        client.get_instructor_info_for_course(course_id=args.course_id)


if __name__ == "__main__":
    main()
