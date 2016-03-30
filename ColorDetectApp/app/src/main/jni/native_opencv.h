#ifndef MOBILEROBOT_IMAGEPROCESSING_ANDROID_COLORDETECTOR_H
#define MOBILEROBOT_IMAGEPROCESSING_ANDROID_COLORDETECTOR_H

#include <jni.h>
#include <opencv2/core/core.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <vector>
#include <iostream>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"



extern "C" {

JNIEXPORT int JNICALL Java_mobileRobot_imageProcessing_android_colorDetector_MainActivity_salt(
        JNIEnv *env, jobject instance,
        jlong matAddrGray,
        jlong matAddrRGBA);

}
#endif //MOBILEROBOT_IMAGEPROCESSING_ANDROID_COLORDETECTOR_H
