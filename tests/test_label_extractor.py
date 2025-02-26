import unittest
from src.label_extractor import extract_label_from_name, extract_label_from_subfolder

class TestLabelExtractor(unittest.TestCase):

    def test_extract_label_from_name(self):
        self.assertEqual(extract_label_from_name("2023_report_final.txt"), "2023_report")
        self.assertEqual(extract_label_from_name("project_alpha_v1.docx"), "project_alpha")
        self.assertEqual(extract_label_from_name("summary_2022.pdf"), "summary_2022")

    def test_extract_label_from_subfolder(self):
        self.assertEqual(extract_label_from_subfolder("2023/January/meeting_notes.txt"), "January")
        self.assertEqual(extract_label_from_subfolder("projects/alpha_v1/overview.txt"), "alpha_v1")
        self.assertEqual(extract_label_from_subfolder("reports/2022/summary.pdf"), "2022") 

if __name__ == '__main__':
    unittest.main()