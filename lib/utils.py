def remove_empty_elements(input_data):
    assert type(input_data) != list()

    try:
        while True:
            input_data.remove('')
    except ValueError:
        pass
    return input_data


def color_print(color, input_data):
    available_colors = {
        'white': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'megenta': 35,
        'cyan': 36,
    }
    assert color in available_colors.keys()

    print(f'\x1b[{available_colors[color]}m{input_data}\x1b[0m')
