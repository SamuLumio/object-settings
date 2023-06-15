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


def test_mappedmultichoice():
    # Example from MappedMultichoice documentation
    filetypes = settings.MappedMultichoice(
		"Select file types", 
		{'.mp4': "Video", '.mp3': "Audio", '.vtt': "Subtitles"}, 
		default_choices=["Video", "Audio"]
	)
    filetypes.set(["Video", "Audio"])
    assert filetypes.get_internal() == ['.mp4', '.mp3']
    assert filetypes.internal_value == ['.mp4', '.mp3']
    filetypes.set(["Subtitles"])
    assert filetypes.get_internal() == ['.vtt']
    assert filetypes.internal_value == ['.vtt']
