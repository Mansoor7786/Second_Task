import argparse
import unittest
from unittest.suite import TestSuite
from runner import execute
import subprocess

#creating the argument parser
parser = argparse.ArgumentParser()

parser.add_argument("--fs", help = "filesystem to mount")
parser.add_argument("--disk",nargs='+', help = "disk name")
parser.add_argument('--lvname', help="name of the logical volume")
parser.add_argument('--size', help="size of the lv")
parser.add_argument('--vgname', help="volume group name to allocate lv")
args = parser.parse_args()

#getting the values from argument parser
fs = args.fs
disk_name = args.disk
lvname = args.lvname
size = args.size
vgname = args.vgname


#loader to run the tests
if __name__ == '__main__':
    import test_file
    suite = TestSuite()
    loader = unittest.TestLoader()
    
    suite.addTests(loader.loadTestsFromName("test_file.Task.test_xlvcreate"))

    runner = unittest.TextTestRunner()
    runner.run(suite)


