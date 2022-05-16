import json
import convert
import export_file
import sys
import os


def main():
    if len(sys.argv) != 2:
        exit()

    jsone_file_name = sys.argv[1]

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(jsone_file_name) as f:
        data = json.load(f)

        for entry in data['pages']:
            content = entry["lines"]
            title = entry["title"].replace('/', '-')
            file_name = export_file.create_filename(entry['title'], '.md')
            page = convert.Page(title, content)
            export_file.export_file(
                file_name, page.annotated_content, output_dir)


if __name__ == '__main__':
    main()
