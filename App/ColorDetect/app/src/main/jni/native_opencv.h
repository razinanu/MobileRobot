#ifndef MOBILEROBOT_IMAGEPROCESSING_ANDROID_COLORDETECTOR_H
#define MOBILEROBOT_IMAGEPROCESSING_ANDROID_COLORDETECTOR_H

#include <jni.h>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/features2d/features2d.hpp>
#include <vector>

extern "C" {
JNIEXPORT void JNICALL Java_mobileRobot_imageProcessing_android_colorDetector_MainActivity_salt(
        JNIEnv *env, jobject instance,
        jlong matAddrGray,
        jint nbrElem);

}
#endif //MOBILEROBOT_IMAGEPROCESSING_ANDROID_COLORDETECTOR_H
