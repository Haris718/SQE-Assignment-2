import pytest
from registration import (
    Student, Course, check_credit_limit, prerequisites_satisfied,
    registration_decision, register_course, withdraw_course
)

def student(**kw):
    data = dict(student_id="W001", completed_courses=set(), current_credits=0,
                outstanding_dues=0, registered_courses=set())
    data.update(kw)
    return Student(**data)

def course(**kw):
    data = dict(code="WB101", credit_hours=2, capacity=2, enrolled=0,
                prerequisites=set(), waitlist=[])
    data.update(kw)
    return Course(**data)

# White-box focus: execute true/false and exceptional outcomes of conditions.
def test_credit_limit_true_branch():
    assert check_credit_limit(10, 2) is True

def test_credit_limit_false_branch():
    assert check_credit_limit(17, 2) is False

@pytest.mark.parametrize("current,new,error", [
    (-1, 2, "Invalid current credits"),
    (19, 2, "Invalid current credits"),
    (10, 0, "Invalid course credits"),
    (10, 5, "Invalid course credits"),
])
def test_credit_limit_validation_branches(current, new, error):
    with pytest.raises(ValueError, match=f"^{error}$"):
        check_credit_limit(current, new)

def test_prerequisite_empty_required_branch():
    assert prerequisites_satisfied(set(), set()) is True

def test_prerequisite_overlap_branch():
    assert prerequisites_satisfied({"A", "B"}, {"A"}) is True

def test_prerequisite_partial_overlap_branch():
    assert prerequisites_satisfied({"A"}, {"A", "B"}) is False

def test_prerequisite_no_overlap_branch():
    assert prerequisites_satisfied({"X"}, {"A", "B"}) is False

def test_decision_dues_exception_branch():
    with pytest.raises(ValueError, match="^Invalid dues$"):
        registration_decision(student(outstanding_dues=-1), course())

def test_decision_capacity_exception_branch():
    with pytest.raises(ValueError, match="^Invalid capacity or enrollment$"):
        registration_decision(student(), course(capacity=0))

def test_decision_dues_block_branch():
    assert registration_decision(student(outstanding_dues=1), course()) == "DUES_BLOCK"

def test_decision_already_registered_branch():
    assert registration_decision(student(registered_courses={"WB101"}), course()) == "ALREADY_REGISTERED"

def test_decision_missing_prerequisite_branch():
    assert registration_decision(student(), course(prerequisites={"A"})) == "PREREQUISITES_MISSING"

def test_decision_credit_limit_branch():
    assert registration_decision(student(current_credits=17), course(credit_hours=2)) == "CREDIT_LIMIT"

def test_decision_waitlist_branch():
    assert registration_decision(student(), course(enrolled=2)) == "WAITLISTED"

def test_decision_registered_branch():
    assert registration_decision(student(), course(enrolled=1)) == "REGISTERED"

def test_register_course_success_branch():
    s, c = student(), course()
    assert register_course(s, c) == "REGISTERED"
    assert s.registered_courses == {"WB101"}
    assert s.current_credits == 2
    assert c.enrolled == 1

def test_register_course_waitlist_branch():
    s, c = student(), course(enrolled=2)
    assert register_course(s, c) == "WAITLISTED"
    assert c.waitlist == ["W001"]

def test_register_course_existing_waitlist_branch():
    s, c = student(), course(enrolled=2, waitlist=["W001"])
    assert register_course(s, c) == "WAITLISTED"
    assert c.waitlist == ["W001"]

def test_register_course_unsuccessful_noop_branch():
    s, c = student(outstanding_dues=1), course()
    before = (set(s.registered_courses), s.current_credits, c.enrolled, list(c.waitlist))
    assert register_course(s, c) == "DUES_BLOCK"
    assert (s.registered_courses, s.current_credits, c.enrolled, c.waitlist) == before

def test_withdraw_course_true_branch():
    s, c = student(current_credits=2, registered_courses={"WB101"}), course(enrolled=1)
    assert withdraw_course(s, c) is True
    assert s.registered_courses == set()
    assert s.current_credits == 0
    assert c.enrolled == 0

def test_withdraw_course_false_branch():
    s, c = student(current_credits=2), course(enrolled=1)
    assert withdraw_course(s, c) is False
    assert s.current_credits == 2
    assert c.enrolled == 1
