from app import process_query


def test_knows__about_your_name():
    assert process_query("What is your name?") == "turtle"


def test_knows_about_dinosaurs():
    dino = "Dinosaurs ruled the Earth 200 million years ago"
    assert process_query("dinosaurs") == dino


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_sum():
    assert process_query("What is 60 plus 84?") == "144"
