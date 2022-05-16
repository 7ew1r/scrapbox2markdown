import os


def create_filename(title, ext):
    replace_chars = {
        '/': '_',
        '\\': '_',
        ':': '_',
        '*': '_',
        '?': '_',
        '"': '_',
        '<': '_',
        '>': '_',
        '|': '_',
    }
    trans = str.maketrans(replace_chars)
    return title.translate(trans) + ext


def export_file(file_name, page_content, output_dir):
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, 'w') as f:
        for line in page_content:
            f.write(line.line + '\n')
