#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import unittest
import string
import time
import util
import random

ad = util.Adb()
tb = util.TouchButton()
sm = util.SetMode() 

#Written by XuGuanjun

PACKAGE_NAME  = 'com.intel.camera22'
ACTIVITY_NAME = PACKAGE_NAME + '/.Camera'

#All setting info of camera could be cat in the folder
PATH_PREF_XML  = '/data/data/com.intel.camera22/shared_prefs/'

#FDFR / GEO / BACK&FROUNT xml file in com.intelcamera22_preferences_0.xml
PATH_0XML      = PATH_PREF_XML + 'com.intel.camera22_preferences_0.xml'

#PICSIZE / EXPROSURE / TIMER / WHITEBALANCE / ISO / HITS / VIDEOSIZE in com.intel.camera22_preferences_0_0.xml
PATH_0_0XML    = PATH_PREF_XML + 'com.intel.camera22_preferences_0_0.xml'

#####                                    #####
#### Below is the specific settings' info ####
###                                        ###
##                                          ##
#                                            #

#FD/FR states check point
FDFR_STATE      = PATH_0XML   + ' | grep pref_fdfr_key'

#Geo state check point
GEO_STATE       = PATH_0XML   + ' | grep pref_camera_geo_location_key'

#Pic size state check point
PICSIZE_STATE   = PATH_0_0XML + ' | grep pref_camera_picture_size_key'

#Exposure state check point 
EXPOSURE_STATE  = PATH_0_0XML + ' | grep pref_camera_exposure_key'

#Timer state check point
TIMER_STATE     = PATH_0_0XML + ' | grep pref_camera_delay_shooting_key'

#Video Size state check point
VIDEOSIZE_STATE = PATH_0_0XML + ' | grep pref_video_quality_key'

#White balance state check point
WBALANCE_STATE  = PATH_0_0XML + ' | grep pref_camera_whitebalance_key'

#Flash state check point
FLASH_STATE     = PATH_0_0XML + ' | grep pref_camera_video_flashmode_key'

#SCENE state check point
SCENE_STATE     = PATH_0_0XML + ' | grep pref_camera_scenemode_key'

SD                  =['4','false']
HD                  =['5','false']
HSD                 =['5','true']
HFD                 =['6','false']
HSFD                =['6','true']
CAMERAMODE_LIST     = ['single','smile','hdr','video','burstfast','burstslow','perfectshot','panorama']
FLASH_MODE          =['on','off','auto']
SCENE_MODE          =['barcode','night-portrait','portrait','landscape','night','sports','auto']
EXPOSURE_MODE       = ['-6','-3','0','3','6']
PICTURESIZE_MODE    =['WideScreen','StandardScreen']
VIDEOSIZE_MODE      = [SD,HD,HSD,HFD,HSFD]

# PATH
PATH ='/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml '
# key
PICTURE_SIZE_KEY ='| grep pref_camera_picture_size_key'

class CameraTest(unittest.TestCase):
    def setUp(self):
        super(CameraTest,self).setUp()
        #Delete all image/video files captured before
        ad.cmd('rm','/sdcard/DCIM/*')
        #Refresh media after delete files
        ad.cmd('refresh','/sdcard/DCIM/*')
        #Launch social camera
        self._launchCamera()

    def tearDown(self):
        #ad.cmd('pm','com.intel.camera22') #Force reset the camera settings to default
        self._pressBack(4)
        super(CameraTest,self).tearDown()
    
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
            sm.switchcamera(mode)

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
            ad.cmd('launch','com.intel.camera22/.Camera')
            assert d(resourceId = 'com.intel.camera22:id/shutter_button').wait.exists(timeout=1000),'Launch camera failed!!'

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
            tb.switchBackOrFrontCamera('front')
            tb.switchBackOrFrontCamera('back')

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
            sm.setCameraSetting('single','flash',flash_mode)
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
            scene_mode = random.choice(SCENE_MODE)
            sm.setCameraSetting('single',5,SCENE_MODE.index(scene_mode)+1)
            self._confirmSettingMode('scenemode',scene_mode)
        sm.setCameraSetting('single',5,7)

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
            exposure_mode = random.choice(EXPOSURE_MODE)
            sm.setCameraSetting('single',6,EXPOSURE_MODE.index(exposure_mode)+1)
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
            size_mode = random.choice(PICTURESIZE_MODE)
            sm.setCameraSetting('single',4,PICTURESIZE_MODE.index(size_mode)+1)
            print size_mode
            self._confirmSettingMode('picture_size',size_mode)

    #Test case 8
    def testChangeVideoSizeMode100Times(self):
        """
        Summary:testChangevideosizemode100times: Change video size mode 100 times
        Steps:  
        1.Launch single capture activity
        2.Change video size 100 times
        3.Exit  activity
        """
        sm.switchcamera('video')
        for i in range(100):
            size_mode = random.choice(VIDEOSIZE_MODE)
            sm.setCameraSetting('video',3,VIDEOSIZE_MODE.index(size_mode)+1)
            self._confirmSettingMode('video_quality',size_mode[0])
            result2=ad.cmd('cat','/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep enable-hightspeed')
            if result2.find(size_mode[1]) == -1:
                self.fail('set video mode failed!')

    #case 9
    def testEnterGalleryFromGalleryPreviewThumbnail100times(self):
        '''
        Summary: enter gallery from gallery preview thumbnail 100times
        Steps  : 1.Launch single capture activity
                 2.enter gallery from gallery preview thumbnail 100times
                 3.Exit  activity
        '''
        tb.takePicture('single')
        time.sleep(100)
        for i in range(5):
            d(resourceId = 'com.intel.camera22:id/thumbnail').click.wait()
            d.click(300,300)
            time.sleep(2)
            assert d(resourceId = 'com.intel.android.gallery3d:id/cardpop').wait.exists(timeout = 3000)
            d.press('back')
            time.sleep(1)



    #case 10
    def testCaptureSingleImage500timesBackCamera(self):
        '''
        Summary: Capture single image 500 times
        Steps  : 1.Launch single capture activity
                 2.Capture single image 500 times
                 3.Exit  activity
        '''
        for i in range(500):
            self._captureAndCheckPicCount('single',2)

    #case 11
    def testCaptureSingleImage500timesFrontCamera(self):
        '''
        Summary: Capture single image 500 times
        Steps  : 1.Launch single capture activity
                 2.Capture single image 500 times
                 3.Exit  activity
        '''
        tb.switchBackOrFrontCamera('front') #Force set camera to front
        for i in range(500):
            self._captureAndCheckPicCount('single',2)
        tb.switchBackOrFrontCamera('back')
    #case 12
    def testCaptureHdrImage500timesBackCamera(self):
        '''
        Summary: Capture hdr image 500 times
        Steps  : 1.Launch hdr capture activity
                 2.Capture hdr image 500 times
                 3.Exit  activity
        '''
        sm.switchcamera('hdr')
        for i in range(500):
            self._captureAndCheckPicCount('single',2)

    #case 13
    def testCaptureSmileImage500timesBackCamera(self):
        '''
        Summary: Capture smile image 500 times
        Steps  : 1.Launch smile capture activity
                 2.Capture smile image 500 times
                 3.Exit  activity
        '''
        sm.switchcamera('smile')
        for i in range(500):
            self._captureAndCheckPicCount('smile',2)

    #case 14
    def testRecord1080PVideo500times(self):
        '''
        Summary: test Record 1080P video 500 times
        Steps  : 1.Launch video capture activity
                 2.Record 1080P video 500 times
                 3.Exit  activity
        '''
        sm.switchcamera('video')
        for i in range(500):
            self._takeVideoAndCheckCount(30,2)

    #case 15
    def testRecordVideo500timesFrontCamera(self):
        '''
        Summary: test Record video 500 times
        Steps  : 1.Launch video capture activity
                 2.Change to front camera
                 3.Record video 500 times
                 4.Exit  activity
        '''
        sm.switchcamera('video')
        tb.switchBackOrFrontCamera('front')
        for i in range(500):
            self._takeVideoAndCheckCount(30,2)
        tb.switchBackOrFrontCamera('back')

    # Test case 18
    def testCapturePerectshotImage200TimesBackCamera(self):
        """
        Summary:testCaptureperfectshotimage200times: Capture perfect shot image 200 times
        Steps:  1.Launch perfectshot capture activity
                2.Capture perfectshot image 200 times
                3.Exit  activity
        """
    #step 1
        sm.switchcamera('perfectshot')
    #step 2 
        for i in range(200):
            self._checkCapturedPic()
            time.sleep(2)


    # Test case 19
    def testCapturePanoramaImage200TimesBackCamera(self):
        """
        Summary:testCapturepanoramaimage200times: Capture panorama image 200 times
        Steps:  1.Launch panorama capture activity
                2.Capture panorama image 200 times
                3.Exit  activity
        """
    #step 1
        sm.switchcamera('panorama')
    #step 2
        for i in range(200):
            self._PanoramaCapturePic()
            time.sleep(1)



    # Test case 20
    def testCaptureSingleImage8M500TimesBackCamera(self):
        """
        capture single image 500 times
        8M pixels, back camera

        """
    #step 1    
        sm.setCameraSetting('single',4,2)
        assert bool(ad.cmd('cat',PATH + PICTURE_SIZE_KEY).find('StandardScreen')+1)
    #step 2
        tb.switchBackOrFrontCamera('back')
    #step 3
        for i in range(500):
            self._checkCapturedPic()
            time.sleep(1)
  


    # Test case 21
    def testcaseCaptureSmileImage8M500TimesBackCamera(self):
        """
        Capture Smile Image 8M 500 times back camera
        8M pixels, back camera
        """
    #step 1
        sm.switchcamera('smile')
        sm.setCameraSetting('smile',2,2)
        d.expect('smile.png')
    #step 2
        tb.switchBackOrFrontCamera('back')
    #step 3
        for i in range(500):
            self._PanoramaCapturePic()
            time.sleep(1)


    # Test Case 22
    def testcaseRecord720PVideo500Times(self):

        """
        Record 720P Video 500times
        Video size 720P
        """
    #step 1
        sm.switchcamera('video')
        sm.setCameraSetting('video',3,2)
        d.expect('video.png')
    #step 2 
        for i in range (500):
            tb.takeVideo(5)
            time.sleep(1)   


    # Test Case 23
    def testcaseRecord480PVideo500Times(self):
        """
        test case Record 480 Pvideo 500 times
        Video size 480P

        """
    #step 1
        sm.switchcamera('video')
        sm.setCameraSetting('video',3,1)
        d.expect('video.png')
    #step 2 
        for i in range (500):
            tb.takeVideo(5)
            time.sleep(1)   
        sm.setCameraSetting('video',3,2)

    # Test Case 24
    def testcaseBurstImage8M200Times(self):
        """
        test case Burst Image 200 times
        8M pixels, back camera
        """

    #step 1
        sm.switchcamera('burstfast')
        sm.setCameraSetting('burst',2,2)
        d.expect('burst.png') 
        assert bool(ad.cmd('cat',PATH + PICTURE_SIZE_KEY).find('StandardScreen')+1)
    #step 2 
        tb.switchBackOrFrontCamera('back')
    #step 3
        for i in range(200):
            self._checkCapturedPic()
            time.sleep(1)
############################################################################################################
##############################################################################################################
    def _confirmSettingMode(self,sub_mode,option):
        if sub_mode == 'location':
            result = ad.cmd('cat','/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0.xml | grep '+ sub_mode)
            if result.find(option) == -1:
                self.fail('set camera setting ' + sub_mode + ' to ' + option + ' failed')
        else:
            result = ad.cmd('cat','/data/data/com.intel.camera22/shared_prefs/com.intel.camera22_preferences_0_0.xml | grep ' + sub_mode)
            if result.find(option) == -1:
                self.fail('set camera setting ' + sub_mode + ' to ' + option + ' failed')

    def _captureAndCheckPicCount(self,capturemode,delaytime):
        beforeNo = ad.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        tb.takePicture(capturemode)
        time.sleep(delaytime) #Sleep a few seconds for file saving
        afterNo = ad.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo != afterNo - 1: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')

    def _launchCamera(self):
        d.start_activity(component = ACTIVITY_NAME)
        #When it is the first time to launch camera there will be a dialog to ask user 'remember location', so need to check
        if d(text = 'OK').wait.exists(timeout = 2000):
            d(text = 'OK').click.wait()
        assert d(resourceId = 'com.intel.camera22:id/mode_button').wait.exists(timeout = 3000), 'Launch camera failed in 3s'

    def _pressBack(self,touchtimes=1):
        for i in range(touchtimes):
            d.press('back')

    def _takeVideoAndCheckCount(self,recordtime,delaytime,capturetimes=0):
        beforeNo = ad.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        tb.takeVideo(recordtime)
        time.sleep(delaytime) #Sleep a few seconds for file saving
        afterNo = ad.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo != afterNo - capturetimes - 1: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')

    def _checkCapturedPic(self):
        beforeNo = ad.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        tb.takePicture('single')
        afterNo = ad.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo == afterNo: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')

    def _PanoramaCapturePic(self):
        beforeNo = ad.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        tb.takePicture('smile')
        afterNo = ad.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo == afterNo: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')