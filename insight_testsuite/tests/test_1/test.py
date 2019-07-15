"""
These are quick tests to see that the output is correctly produced
and the test_output is the same as the source_of truth output
"""

import unittest
import subprocess


class TestPurchaseAnalytics(unittest.TestCase):
    def test_script(self):
        """calls purchase_analytics.py on test files"""
        subprocess.check_call(['python', '../../../src/purchase_analytics.py', 'input/order_products.csv',
                               'input/products.csv', 'output/report_generated.csv'])

    def test_cvs(self):
        """ tests if the generated test_file is the same like the (source of truth) output file"""
        with open('output/report.csv', 'r') as file1, open('output/report_generated.csv', 'r') as file2:
            truth = file1.readline()
            compare = file2.readline()

        for row in truth:
            self.assertTrue(row in compare)

        for row in compare:
            self.assertTrue(row in truth)


if __name__ == "__main__":
        unittest.main()
