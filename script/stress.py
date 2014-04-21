#!/usr/bin/env python
from devicewrapper.android import device as d
import unittest
import string
import os
import commands
import time
import random
import util

"""
@author:Xiao Bowen
@Note:Feature test for intel camera2.2
"""
CAMERAMODE_LIST = ('single','smile','hdr','video','burstfast','burstslow','perfectshot','panorama')
A  = util.Adb()
SM = util.SetMode()
TB = util.TouchButton()

SD=['4',None]
HD=['5','false']
HSD=['5','true']
HFD=['6','false']
HSFD=['6','true']


FLASH_MODE=['on','off','auto']

SCENE_MODE ={'barcode':1,
            'night-portrait':2,
            'portrait':3,
            'landscape':4,
            'night':5,
            'sports':6,
            'auto':7}
EXPOSURE_MODE = {'-6':1,
                '-3':2,
                '0',3,
                '3',4,
                '6',5
                }
PICTURESIZE_MODE   ={'WideScreen':1,
                    'StandardScreen':2
                    }

VIDEOSIZE_MODE     ={SD:1,
                    HD:2,
                    HSD:3,
                    HFD:4,
                    HSFD:5
                    }

class MyTest(unittest.TestCase):
    def setUp(self):
        # rm DCIM folder and refresh from adb shell
        A.cmd('rm','/sdcard/DCIM/100ANDRO')
        A.cmd('refresh','/sdcard/DCIM/100ANDRO')
        # Launch camera (Default is single mode)
        A.cmd('launch','com.intel.camera22/.Camera')
        time.sleep(2)
        try:
            assert d(text = 'OK').wait.exists(timeout = 3000)
            d(text = 'OK').click.wait()
        except:
            pass
        assert d(resourceId = 'com.intel.camera22:id/shutter_button'),'Launch camera failed!!'
        super(MyTest,self).setUp()

    def tearDown(self):
        #4.Exit  activity
        self._pressBack(4)
        # A.cmd('pm','com.intel.camera22')
        super(MyTest,self).tearDown()

    # Test case 1
    def testSwitchMode50Times(self):
        """
        Summary:testswitchmode50times: test switch mode 50 times
        Steps:  
        1.Launch single capture activity
        2.Switch camera mode 50 times
        3.Exit  activity
        """
        for i in range(50):
            mode = random.choice(CAMERAMODE_LIST)
            SM.switchcamera(mode)

        # Test case 2
    def testLaunchCamera50Times(self):
        """
        Summary:testlaunchcamera50times: Launch camera 50 times
        Steps:  
        1.Launch single capture activity
        2.Repeat 50 times
        3.Exit  activity
        """
        for i in range(50):
            self._pressBack(4)
            A.cmd('launch','com.intel.camera22/.Camera')
            assert d(resourceId = 'com.intel.camera22:id/shutter_button'),'Launch camera failed!!'

    # Test case 3
    def testSwitchBackFrontCameraInSingleMode30Times(self):
        """
        Summary:SwitchBack/Frontcamerainsinglemode30times: Switch Back/Front camera in each mode 30 times
        Steps:  
        1.Launch single capture activity
        2.Switch Back/Front camera in single mode 30 times
        3.Exit  activity
        """
        for i in range(30):
            TB.switchBackOrFrontCamera('front')
            TB.switchBackOrFrontCamera('back')

    # Test case 4
    def testChangeFlashMode100Times(self):
        """
        Summary:testChangeflashmode100times: Change flash mode 100 times
        Steps:  
        1.Launch single capture activity
        2.Change flash mode 100 times
        3.Exit  activity
        """
        for i in range(100):
            flash_mode = random.choice(FLASH_MODE)
            SM.setCameraSetting('single','flash',flash_mode)
            self._confirmSettingMode('flash',flash_mode)

    # Test case 5
    def testChangeSceneMode100Times(self):
        """
        Summary:testChangescenemode100times: Change scene mode 100 times
        Steps:  
        1.Launch single capture activity
        2.Change scene mode 100 times
        3.Exit  activity
        """
        for i in range(100):
            scene_mode = random.choice(SCENE_MODE.keys())
            SM.setCameraSetting('single',5,SCENE_MODE[scene_mode])
            self._confirmSettingMode('scenemode',scene_mode)

    # Test case 6
    def testChangeExposureMode100Times(self):
        """
        Summary:testChangeexposuremode100times: Change exposure mode 100 times
        Steps:  
        1.Launch single capture activity
        2.Change exposure mode 100 times
        3.Exit  activity
        """
        for i in range(100):
            exposure_mode = random.choice(EXPOSURE_MODE.keys())
            SM.setCameraSetting('single',5,EXPOSURE_MODE[exposure_mode])
            self._confirmSettingMode('exposure',exposure_mode)

    # Test case 7
    def testChangePictureSizeMode100Times(self):
        """
        Summary:testChangepicturesizemode100times: Change picture size mode 100 times
        Steps:  
        1.Launch single capture activity
        2.Change picture size 100 times
        3.Exit  activity
        """
        for i in range(100):
            size_mode = random.choice(PICTURESIZE_MODE.keys())
            SM.setCameraSetting('single',4,PICTURESIZE_MODE[size_mode])
            self._confirmSettingMode('picturesize',size_mode)

    # Test case 8
    def testChangeVideoSizeMode100Times(self):
        """
        Summary:testChangevideosizemode100times: Change video size mode 100 times
        Steps:  
        1.Launch single capture activity
        2.Change video size 100 times
        3.Exit  activity
        """
        SM.switchcamera('video')      
        for i in range(100):
            size_mode = random.choice(VIDEOSIZE_MODE.keys())
            SM.setCameraSetting('video',3,VIDEOSIZE_MODE[size_mode])
            self._confirmSettingMode('video_quality',size_mode[0])
            result2=A.cmd('cat','/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep enable-hightspeed')
            if result2.find(size_mode[1]) == -1:
                self.fail('set video mode failed!')


    def _confirmSettingMode(self,sub_mode,option):
        if sub_mode == 'location':
            result = A.cmd('cat','/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep '+ sub_mode)
            if result.find(option) == -1:
                self.fail('set camera setting ' + sub_mode + ' to ' + option + ' failed')
        else:
            result = A.cmd('cat','/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep ' + sub_mode)
            if result.find(option) == -1:
                self.fail('set camera setting ' + sub_mode + ' to ' + option + ' failed')

    def _pressBack(self,touchtimes):
        for i in range(1,touchtimes+1):
            d.press('back')