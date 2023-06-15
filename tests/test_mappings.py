import settings


def test_mappedchoice():
    # Example from MappedChoice documentation
    log_level = settings.MappedChoice("Level of logging", {0: "Debug", 1: "Info", 2: "Error"}, "Info")
    log_level.set("Info")
    assert log_level.get_internal() == 1
    assert log_level.internal_value == 1
    log_level.set("Error")
    assert log_level.get_internal() == 2
    assert log_level.internal_value == 2
