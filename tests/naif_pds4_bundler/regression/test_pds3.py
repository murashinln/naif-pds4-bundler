"""Regression Test Family for PDS3 archives."""
import os
import shutil
import sys
import unittest
from unittest import TestCase

from pds.naif_pds4_bundler.__main__ import main
from pds.naif_pds4_bundler.utils import extract_comment


class TestPDS3(TestCase):
    """Regression Test Family Class for PDS3 archives.

    Note that EOL, label checksum tags and checksum files are not tested.
    """

    @classmethod
    def setUpClass(cls):
        """Constructor.

        Method that will be executed once for this test case class.
        It will execute before all tests methods.

        Clears up the functional tests directory.
        """
        print(f"NPB - Regression Tests - {cls.__name__}")

        os.chdir(os.path.dirname(__file__))

        dirs = ["working", "staging", "kernels", "msl-m-spice-6-v1.0"]
        for dir in dirs:
            shutil.rmtree(dir, ignore_errors=True)

        cls.silent = True
        cls.log = True

    def setUp(self):
        """Setup Test.

        This method will be executed before each test function.
        """
        unittest.TestCase.setUp(self)
        print(f"    * {self._testMethodName}")

        dirs = ["working", "staging", "kernels"]
        for dir in dirs:
            shutil.rmtree(dir, ignore_errors=True)

    def tearDown(self):
        """Clean-up Test.

        This method will be executed after each test function.
        """
        unittest.TestCase.tearDown(self)
        mis = self.pds3_dir

        all_files = []
        files = []
        with open(f"working/{self.mission}_release_{self.release}.file_list", 'r') as f:
            for line in f:
                if '.kernel_list' not in line:
                    files.append(f'{self.pds3_dir}/{self.volid}/{line[:-1]}')

        #
        # Extract comments to check label insertion.
        #
        for file in files:
            if any(x in file.split('.')[-1] for x in ['bc','bsp','bds']):
                cmt = extract_comment(file)
                with open(file.split('.b')[0] + '.cmt', 'w') as c:
                    for line in cmt:
                        c.write(line + '\n')
                all_files.append(file.split('.b')[0] + '.cmt')
            elif not any(x in file.split('.')[-1] for x in ['tab']):
                all_files.append(file)

        #
        # Compare the files.
        #
        for product in all_files:
            if os.path.isfile(product):
                test_product = product.replace(f"{mis}/", "../data/regression/")

                with open(product) as ff:
                    fromlines = ff.read().splitlines()
                    fromlines = [
                        item
                        for item in fromlines
                        if ("PRODUCT_CREATION_TIME" not in item)
                    ]
                with open(test_product) as tf:
                    tolines = tf.read().splitlines()
                    tolines = [
                        item
                        for item in tolines
                        if ("PRODUCT_CREATION_TIME" not in item)
                    ]

                if fromlines != tolines:
                    print(f"Assertion False for: {product}")
                    self.assertTrue(False)
        dirs = ["working", "staging", "kernels", mis]
        for dir in dirs:
            shutil.rmtree(dir, ignore_errors=True)
            pass

    def post_setup(self):
        """Ensures release and creation date time is fixed for the test."""
        self.config = f"../config/{self.mission}.xml"

        dirs = ["working", "staging", "staging/mslsp_1000",
                "staging/mslsp_1000/catalog", self.pds3_dir]
        for dir in dirs:
            os.makedirs(dir, 0o766, exist_ok=True)
        #
        # Use the appropriate endianness for the system.
        #
        #if sys.byteorder == 'little':
        #    print('LTL-IEEE')

    def test_msl(self):
        """Test to generate a MSL data set increment."""
        self.mission = "msl"
        self.pds3_dir = "msl-m-spice-6-v1.0"
        self.volid = "mslsp_1000"
        self.release = "29"
        self.post_setup()

        plan = "working/msl_release_29.plan"

        shutil.copy2(f"../data/spiceds_{self.mission}.cat",
                     f"staging/{self.volid}/catalog/spiceds.cat"
        )
        shutil.copy2(f"../data/release_{self.mission}.cat",
                     f"staging/{self.volid}/catalog/release.cat"
        )
        shutil.copy2("../data/msl_release_28.kernel_list",
                     "working/msl_release_28.kernel_list"
        )
        shutil.copy2(
            "../data/msl_release_00.plan",
            f"working/msl_release_{self.release}.plan"
        )

        shutil.copytree("../data/msl/mslsp_1000",
                        f"{self.pds3_dir}/{self.volid}")

        main(self.config, plan, silent=True, log=self.log)

if __name__ == "__main__":
    unittest.main()
