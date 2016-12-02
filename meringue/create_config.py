import os

class create_config:
    def __init__(self, meringue_path):
        with open(meringue_path + '/data/meringue_config.ini', 'w') as f_out:
            f_out.write('foreground=#ffffff\n')
            f_out.write('background=#000000\n')
            f_out.write('file_color=#00FF00\n')
            f_out.write('dir_color=#ff00ff\n')
            f_out.write('line_num_color=#ff0000\n')
            f_out.write('line_num_background_color=#333333\n')
            f_out.write('file_bar_color=#666666\n')
            f_out.write('file_bar_text_color=#ffffff\n')
            f_out.write('notebook_background=#333333\n')
            f_out.write('highlight_foreground=#ffff00\n')
            f_out.write('highlight_background=#0000ff\n')
            f_out.write('token_keyword=#ff0000\n')
            f_out.write('token_name=#ff7700\n')
            f_out.write('token_literal=#ffff00\n')
            f_out.write('token_string=#ff00ff\n')
            f_out.write('token_number=#0000ff\n')
            f_out.write('token_operators=#00ff00\n')
            f_out.write('token_punctuation=#00ffff\n')
            f_out.write('token_comments=#777777\n')
            f_out.write('token_generic=#77ffff\n')
            f_out.write('folder=\n')
