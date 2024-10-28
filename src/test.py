from app import process_query


def test_knows_larger_numbers():
    assert (process_query("Which of the following numbers" +
                          "is the largest: 47, 32, 58?")
            == str(58))
