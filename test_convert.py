import unittest
from convert import Page, AnnotatedLine


class FirstTest(unittest.TestCase):
    def test_annotated_lines(self):
        input_list = [
            '1line',
            'code:hoge',
            ' 2line',
            ' 3line',
            '4line',
        ]
        expect_list = [
            AnnotatedLine('1line', False),
            AnnotatedLine('code:hoge', False),
            AnnotatedLine(' 2line', True),
            AnnotatedLine(' 3line', True),
            AnnotatedLine('4line', False),
        ]
        output = Page.annotated_lines(self, input_list)
        for i, expect in enumerate(expect_list):
            self.assertEqual(output[i].line, expect.line)
            self.assertEqual(output[i].is_codeblock,
                             expect.is_codeblock)

    def test_convert_unordered_list(self):
        input_list = [
            AnnotatedLine('\tリスト', False),
            AnnotatedLine('\t\tリスト', False),
            AnnotatedLine('\t\t\tリスト', False),
            AnnotatedLine('\t\t\t\tリスト', False)]
        expect_list = [AnnotatedLine('- リスト', False),
                       AnnotatedLine('\t- リスト', False),
                       AnnotatedLine('\t\t- リスト', False),
                       AnnotatedLine('\t\t\t- リスト', False)]
        output = Page.convert_unordered_list(self, input_list)
        for i, expect in enumerate(expect_list):
            self.assertEqual(output[i].line, expect.line)

    def test_convert_header(self):
        self.assertEqual(Page.convert_header(self, '[* test]'), '### test')
        self.assertEqual(Page.convert_header(self, '[** test]'), '## test')
        self.assertEqual(Page.convert_header(self, '[*** test]'), '# test')
        self.assertEqual(Page.convert_header(self, '[**** test]'), '# test')

    def test_convert_image_link(self):
        self.assertEqual(Page.convert_image_link(
            self, '[http://hoge.jpg]'), '![](http://hoge.jpg)')

    def test_convert_link(self):
        self.assertEqual(Page.convert_link(self,
                                           '[hoge http://hoge.com]'), '[hoge](http://hoge.com)')
        self.assertEqual(Page.convert_link(self,
                                           '[https://hoge.com hoge]'), '[hoge](https://hoge.com)')


if __name__ == "__main__":
    unittest.main()
