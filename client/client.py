import argparse


def main():
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
        "--average_review",
        action="store_true",
        help="Get average review rating for a course"
    )

    group.add_argument(
        "--post_review",
        action="store_true",
        help="Post a review for a course"
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
        type=str,
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
        "--reviewer",
        dest="reviewer",
        type=str,
        help="Insert reviewer name for a course review"
    )

    args = parser.parse_args()


if __name__ == "__main__":
    main()
