from app import generate_ticket

def test_ticket_has_3_rows():
    ticket = generate_ticket()
    assert len(ticket) == 3

def test_ticket_numbers_in_range():
    ticket = generate_ticket()
    for row in ticket:
        for num in row:
            if num != 0:
                assert 1 <= num <= 90

def test_ticket_has_9_columns():
    ticket = generate_ticket()
    for row in ticket:
        assert len(row) == 9
