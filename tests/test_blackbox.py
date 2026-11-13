import copy
import pytest

from registration import (
    Student, Course, check_credit_limit, prerequisites_satisfied,
    registration_decision, register_course, withdraw_course
)

def make_student(**kwargs):
    values = dict(student_id="S001", completed_courses=set(),
                  current_credits=0, outstanding_dues=0,
                  registered_courses=set())
    values.update(kwargs)
    return Student(**values)

def make_course(**kwargs):
    values = dict(code="CS201", credit_hours=3, capacity=30,
                  enrolled=0, prerequisites=set(), waitlist=[])
    values.update(kwargs)
    return Course(**values)

# FR-01 and FR-02: credit limit and validation boundaries
@pytest.mark.parametrize("current,new,expected", [
    (0, 1, True), (14, 4, True), (15, 3, True),  # exactly 18 is allowed
    (16, 3, False), (18, 1, False),
])
def test_credit_limit_boundaries(current, new, expected):
    assert check_credit_limit(current, new) is expected

@pytest.mark.parametrize("current,new,message", [
    (-1, 3, "Invalid current credits"),
    (19, 3, "Invalid current credits"),
    (10, 0, "Invalid course credits"),
    (10, 5, "Invalid course credits"),
])
def test_credit_limit_invalid_values(current, new, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        check_credit_limit(current, new)

def test_credit_validation_order():
    with pytest.raises(ValueError, match="^Invalid current credits$"):
        check_credit_limit(-1, 5)

# FR-03: all required prerequisites must be completed
def test_no_prerequisites_are_satisfied():
    assert prerequisites_satisfied(set(), set()) is True

def test_all_prerequisites_completed():
    assert prerequisites_satisfied({"CS101", "MATH101"}, {"CS101", "MATH101"}) is True

def test_one_missing_prerequisite_means_not_satisfied():
    assert prerequisites_satisfied({"CS101"}, {"CS101", "MATH101"}) is False

def test_no_required_prerequisite_completed():
    assert prerequisites_satisfied({"ENG101"}, {"CS101", "MATH101"}) is False

# FR-04 to FR-10: decision outcomes, validation, and priority
def test_any_positive_dues_block_registration():
    student = make_student(outstanding_dues=1)
    assert registration_decision(student, make_course()) == "DUES_BLOCK"

def test_already_registered_has_priority_over_missing_prerequisites():
    student = make_student(registered_courses={"CS201"})
    course = make_course(prerequisites={"CS101"})
    assert registration_decision(student, course) == "ALREADY_REGISTERED"

def test_missing_prerequisite_blocks_registration():
    student = make_student(completed_courses={"CS101"})
    course = make_course(prerequisites={"CS101", "MATH101"})
    assert registration_decision(student, course) == "PREREQUISITES_MISSING"

def test_exactly_18_credits_is_allowed_in_decision():
    student = make_student(current_credits=15)
    assert registration_decision(student, make_course(credit_hours=3)) == "REGISTERED"

def test_exceeding_18_credits_is_blocked():
    student = make_student(current_credits=16)
    assert registration_decision(student, make_course(credit_hours=3)) == "CREDIT_LIMIT"

def test_available_seat_returns_registered():
    assert registration_decision(make_student(), make_course(capacity=2, enrolled=1)) == "REGISTERED"

def test_full_course_returns_waitlisted():
    assert registration_decision(make_student(), make_course(capacity=2, enrolled=2)) == "WAITLISTED"

def test_invalid_dues_validation():
    with pytest.raises(ValueError, match="^Invalid dues$"):
        registration_decision(make_student(outstanding_dues=-1), make_course())

def test_invalid_capacity_validation():
    with pytest.raises(ValueError, match="^Invalid capacity or enrollment$"):
        registration_decision(make_student(), make_course(capacity=0, enrolled=0))

def test_invalid_enrollment_validation():
    with pytest.raises(ValueError, match="^Invalid capacity or enrollment$"):
        registration_decision(make_student(), make_course(capacity=2, enrolled=3))

def test_dues_validation_has_priority_over_capacity_validation():
    student = make_student(outstanding_dues=-1)
    course = make_course(capacity=0)
    with pytest.raises(ValueError, match="^Invalid dues$"):
        registration_decision(student, course)

def test_registration_decision_does_not_mutate_objects():
    student = make_student(current_credits=3)
    course = make_course(enrolled=1)
    student_before, course_before = copy.deepcopy(student), copy.deepcopy(course)
    registration_decision(student, course)
    assert student == student_before
    assert course == course_before

# FR-11 and FR-12: applying decisions and state changes
def test_successful_registration_updates_all_required_state():
    student = make_student(current_credits=15)
    course = make_course(credit_hours=3, capacity=10, enrolled=2)
    result = register_course(student, course)
    assert result == "REGISTERED"
    assert "CS201" in student.registered_courses
    assert student.current_credits == 18
    assert course.enrolled == 3

def test_waitlisting_adds_student_once_without_other_mutations():
    student = make_student(student_id="S009")
    course = make_course(capacity=5, enrolled=5)
    result = register_course(student, course)
    assert result == "WAITLISTED"
    assert course.waitlist == ["S009"]
    assert student.current_credits == 0
    assert student.registered_courses == set()
    assert course.enrolled == 5

def test_existing_waitlist_entry_is_not_duplicated():
    student = make_student(student_id="S009")
    course = make_course(capacity=5, enrolled=5, waitlist=["S009"])
    assert register_course(student, course) == "WAITLISTED"
    assert course.waitlist == ["S009"]

def test_blocked_registration_does_not_change_state():
    student = make_student(outstanding_dues=1)
    course = make_course()
    student_before, course_before = copy.deepcopy(student), copy.deepcopy(course)
    assert register_course(student, course) == "DUES_BLOCK"
    assert student == student_before
    assert course == course_before

# FR-13 and FR-14: withdrawal
def test_withdrawal_updates_student_and_course():
    student = make_student(current_credits=6, registered_courses={"CS201"})
    course = make_course(credit_hours=3, enrolled=4)
    assert withdraw_course(student, course) is True
    assert student.registered_courses == set()
    assert student.current_credits == 3
    assert course.enrolled == 3

def test_withdrawal_of_unregistered_course_changes_nothing():
    student = make_student(current_credits=6)
    course = make_course(enrolled=4)
    student_before, course_before = copy.deepcopy(student), copy.deepcopy(course)
    assert withdraw_course(student, course) is False
    assert student == student_before
    assert course == course_before
