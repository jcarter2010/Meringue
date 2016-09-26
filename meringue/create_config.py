import os

class create_config:
    def __init__(self, meringue_path):
        #try:
        #    os.makedirs(os.environ['HOME'] + '/merengue')
        #except:
        #    pass
        with open(meringue_path + '/data/meringue_config.ini', 'w') as f_out:
            f_out.write('highlight_foreground=#FFFF00\n')
            f_out.write('highlight_background=#0000FF\n')
            f_out.write('highlight_keyword=#FF0000\n')
            f_out.write('highlight_function_name=#FFFF00\n')
            f_out.write('highlight_function=#FF8800\n')
            f_out.write('highlight_boolean=#ff6600\n')
            f_out.write('highlight_string=#FF00FF\n')
            f_out.write('highlight_number=#00FF00\n')
            f_out.write('highlight_operator=#00FFFF\n')
            f_out.write('highlight_comment=#888888\n')
            f_out.write('foreground=#ffffff\n')
            f_out.write('background=#000000\n')
            f_out.write('file_color=#00FF00\n')
            f_out.write('dir_color=#FF00FF\n')
            f_out.write('line_num_color=#FF00FF\n')
            f_out.write('line_num_background_color=#333333\n')
            f_out.write('file_bar_color=#666666\n')
            f_out.write('file_bar_text_color=#FFFFFF\n')
            f_out.write('notebook_background=#333333\n')
            f_out.write('folder=')
