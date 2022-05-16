import unittest
import export_file


class ExportFileTest(unittest.TestCase):
    def test_create_filename(self):
        input = 'タイトル/タイトル\\タイトル:タイトル*タイトル?タイトル"タイトル<タイトル>タイトル|タイトル'
        expect = 'タイトル_タイトル_タイトル_タイトル_タイトル_タイトル_タイトル_タイトル_タイトル_タイトル.md'
        self.assertEqual(export_file.create_filename(input, '.md'), expect)


if __name__ == "__main__":
    unittest.main()
