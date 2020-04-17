def remove_empty_elements(input_data):
    assert type(input_data) != list()

    try:
        while True:
            input_data.remove('')
    except ValueError:
        pass
    return input_data
