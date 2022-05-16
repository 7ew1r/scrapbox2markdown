import re


class AnnotatedLine:
    def __init__(self, line, is_codeblock):
        self.line = line
        self.is_codeblock = is_codeblock


class Page:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.annotated_content = self.annotated_lines(content)
        self.converted_content = self.convert_content()

    def annotated_lines(self, content):
        annotated_lines = []
        for i, line in enumerate(content):
            if i == 0:
                annotated_lines.append(AnnotatedLine(line, False))
            else:
                # 直前が "code:~" もしくはコードブロックであり、スペースが1つ以上ある場合
                if (content[i - 1].startswith('code:') or
                    annotated_lines[i - 1].is_codeblock) and \
                        (line.startswith(' ') or line.startswith('\t')):
                    annotated_lines.append(AnnotatedLine(line, True))
                else:
                    annotated_lines.append(AnnotatedLine(line, False))
        return annotated_lines

    def convert_codeblock(self):
        def is_before_line_codeblock(index):
            if index == 0:
                return False
            return self.annotated_content[index - 1].is_codeblock

        is_insert_code_start_tag = False
        is_insert_code_end_tag = False
        for i, line in enumerate(self.annotated_content):
            if line.line.startswith('code:'):
                self.annotated_content[i].line = '```'
                is_insert_code_start_tag = True
            else:
                if line.is_codeblock:
                    self.annotated_content[i].line = line.line[1:]
                else:
                    if is_before_line_codeblock(i):
                        new_line = AnnotatedLine('```', False)
                        is_insert_code_end_tag = True
                        self.annotated_content.insert(i, new_line)

        # コードブロックの終わりがない場合追加する
        if is_insert_code_start_tag and not is_insert_code_end_tag:
            new_line = AnnotatedLine('```', False)
            self.annotated_content.append(new_line)

    def convert_unordered_list(self, annotated_content):
        converted = []
        for line in annotated_content:
            if line.is_codeblock:
                converted.append(line)
                pass
            else:
                if line.line.startswith('\t'):
                    pattern = r'(^\t+)'
                    tab_count = len(re.match(pattern, line.line).group(1))
                    new_line = '\t'*(tab_count-1) + '- ' + \
                        re.sub(pattern, '', line.line)
                    converted.append(AnnotatedLine(new_line, False))
                else:
                    converted.append(line)
        return converted

    # 見出し
    def convert_header(self, line):
        def header_level(asterisk_count):
            if asterisk_count == 1:
                return '###'
            elif asterisk_count == 2:
                return '##'
            else:
                return '#'

        pattern = r'\[(\*+) (.*?)\]'
        m = re.match(pattern, line)
        if m is None:
            return line

        header = header_level(len(m.group(1)))
        replace = header + r' \2'
        return re.sub(pattern, replace, line)

    # 画像
    # [http://hoge.jpg]
    # [http://hoge.png]
    def convert_image_link(self, line):
        pattern = r'\[(http.*?\.(?:jpg|png))\]'
        replace = r'![](\1)'
        return re.sub(pattern, replace, line)

    # リンク
    # [hoge http//hoge.com]
    # [http//hoge.com hoge]
    def convert_link(self, line):
        pattern1 = r'\[(.*?) (http.*?)\]'
        replace1 = r'[\1](\2)'
        new_line = re.sub(pattern1, replace1, line)
        pattern2 = r'\[(http.*?) (.*?)\]'
        replace2 = r'[\2](\1)'
        return re.sub(pattern2, replace2, new_line)

    # 太字
    def convert_bold(self, line):
        pattern = r'\[\[(.*?)\]\]'
        replace = r'**\1**'
        return re.sub(pattern, replace, line)

    # 打ち消し線
    def convert_strike_through(self, line):
        pattern = r'\[- (.*?)\]'
        replace = r'~~\1~~'
        return re.sub(pattern, replace, line)

    def convert_line(self, line):
        line = self.convert_header(line)
        line = self.convert_image_link(line)
        line = self.convert_link(line)
        line = self.convert_bold(line)
        line = self.convert_strike_through(line)
        return line

    def convert_first_line(self, line):
        return '# ' + line

    def convert_lines(self):
        for i, annotated_line in enumerate(self.annotated_content):
            if i == 0:
                self.annotated_content[i].line = self.convert_first_line(
                    annotated_line.line)
            else:
                if not annotated_line.is_codeblock:
                    self.annotated_content[i].line = self.convert_line(
                        annotated_line.line)
        self.convert_codeblock()
        self.annotated_content = self.convert_unordered_list(
            self.annotated_content)
        return [line.line for line in self.annotated_content]

    def convert_content(self):
        converted = self.convert_lines()
        return converted
