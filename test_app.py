from app import students

def test_student_narks():
    for student in students:
        assert student["marks"] >= 0
        assert student["marks"] <= 100
    print("ALL TEST PASSED!")

