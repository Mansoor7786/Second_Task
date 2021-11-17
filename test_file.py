import unittest
import cli
from runner import execute,fio
import subprocess

class Task(unittest.TestCase):
    disk = " ".join(cli.disk_name)
    
    def tearDown(self):
        #destroying pv ater running the test
        disk = " ".join(cli.disk_name)
        
        self.vgpath = "/dev/{}/{}".format(cli.vgname,cli.lvname)
        print("Step 13: Unmounting /data directory")
        execute("umount /data")

        print("Step 14: Removing /data directory")
        execute("rmdir /data")

        print("Step 15: Wiping the filesystem from the Logical Volume")
        execute("wipefs -a {}".format(self.vgpath))

        print("Step 16: Removing the Logical Volume {}".format(cli.lvname))
        execute("lvremove -f {}" .format(cli.vgname), inp="y\n")

        print("Step 17: Removing the Volume Group {}".format(cli.vgname))
        execute("vgremove {}".format(cli.vgname))
        
        print("Step 18: Removing the Physical Volume {}".format(Task.disk))
        execute("pvremove {}" .format(disk))


    def test_xlvcreate(self):
        print("Step 1: Creating Physical Volume {}".format(Task.disk))
        execute("pvcreate {}" .format(Task.disk))

        print("Step 2: Creating Volume group {}".format(cli.vgname))
        execute("vgcreate {} {}" .format(cli.vgname, Task.disk))

        print("Step 3: Creating Logical Volume {}" .format(cli.lvname))
        execute("lvcreate --size {} --name {} {}".format(cli.size,cli.lvname,cli.vgname))
        
        self.lvpath = "/dev/{}/{}" .format(cli.vgname, cli.lvname)
        
        print("Step 4: Creating an {} filesystem on the Logical Volume {}" .format(cli.fs,cli.lvname))
        execute("sudo mkfs -t {} {}" .format(cli.fs, self.lvpath))

        print("Step 5: Creating a directory named data under root directory for mounting the logical volume")
        execute("mkdir /data")

        print("Step 6: Mounting the /data directory")
        execute("mount {} /data" .format(self.lvpath))
        
        print("Step 7: Performing IO using fio")
        self.fio_fun = fio("fio --filename={} --direct=1 --size=1G --rw=randrw --bs=4k --ioengine=libaio --iodepth=256 --runtime=5 --numjobs=32 --time_based --group_reporting --name=iops-test-job --allow_mounted_write=1".format(self.lvpath))
        self.fspath = "dev/mapper/{}-{}" .format(cli.vgname, cli.lvname)
        self.outpv = execute("pvdisplay")
        self.outvg = execute("vgdisplay")
        self.output = execute("lvdisplay")
        self.outmnt = execute("findmnt")

        print("Step 8: Verifying if the Physical Volume is present")
        for i in cli.disk_name:
            self.assertRegex(self.outpv,i)
        print("---------------Success---------------")

        print("Step 9: Verifying if the Volume Group is present")
        self.assertRegex(self.outvg,cli.vgname)
        print("---------------Success---------------")
        
        print("Step 10: Verifying if the Logical Volume is present")
        self.assertRegex(self.output,cli.lvname)
        print("---------------Success---------------")
        
        print("Step 11: Verifying if the Filesystem is mounted")
        self.assertRegex(self.outmnt,self.fspath)
        print("---------------Success--OK-------------")
        
        print("Step 12: Verifying whether IO is successful")
        self.assertRegex(self.fio_fun,"Run status")
        print("-------------Success---OK------------")

