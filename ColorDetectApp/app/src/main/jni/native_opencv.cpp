#include "native_opencv.h"

using namespace std;
using namespace cv;



extern "C" {
JNIEXPORT jobjectArray Java_mobileRobot_imageProcessing_android_colorDetector_MainActivity_salt(
        JNIEnv *env, jobject instance,
        jlong matAddrGray,
        jlong matAddrRGBA) {
    //1280×720 Pixel resolution
    Mat &imgGray = *(Mat *) matAddrGray;
    Mat &mRGBA = *(Mat *) matAddrRGBA;
    Mat imgHSV;
    cvtColor(mRGBA, imgHSV, COLOR_RGB2HSV);
    Mat mask_blue;
    Mat mask_red;
    inRange(imgHSV, Scalar(100, 50, 50), Scalar(140, 255, 255), mask_blue);
    //morphological opening (remove small objects from the foreground) 
    erode(mask_blue, mask_blue, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
    dilate(mask_blue, mask_blue, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
    //morphological closing (fill small holes in the foreground) 
    dilate(mask_blue, mask_blue, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
    erode(mask_blue, mask_blue, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));

    inRange(imgHSV, Scalar(170, 50, 50), Scalar(179, 255, 255), mask_red);
    //morphological opening (remove small objects from the foreground) 
    erode(mask_red, mask_red, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
    dilate(mask_red, mask_red, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
    //morphological closing (fill small holes in the foreground) 
    dilate(mask_red, mask_red, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
    erode(mask_red, mask_red, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
    // Kreiserkennung auf dem Graustufenbild 
    medianBlur(imgGray, imgGray, 5);
    vector<Vec3f> circles;
    HoughCircles(imgGray, circles, CV_HOUGH_GRADIENT,
                 1, // accumulator resolution (size of the image / 2)
                 50,  // minimum distance between two circles
                 50, // Canny high threshold
                 30, // minimum number of votes
                 20, 100);


    jobjectArray ret;
    int i;

    char *data[]={"", "", "", "", "","","","","","","","","","","",""}; //= {"A", "B", "C", "D"};


    int s = sizeof(data) / sizeof(char);
    //char c = itoa(s);
    ostringstream intShiftStrX;
    ostringstream intShiftStrY;

    string intToStringX;
    string intToStringY;


    bool blue, red, color=false;
    int index = 0;
    for (size_t i = 0; i < circles.size(); i++) {
        Mat mask(Mat::zeros(imgGray.rows, imgGray.cols, CV_8UC1));
        int radius = cvRound(circles[i][2]);
        Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
        circle(mask, center, radius / 3, Scalar(255, 255, 255),
               radius / 2, 1);
        if (mean(mask_blue, mask)[0] > 130) {
            //blue ball
            if(index<16){
            int coordinateX = cvRound(circles[i][1]);
            int coordinateY = cvRound(circles[i][0]);
            intShiftStrX<< coordinateX;
            string intToStringX = intShiftStrX.str();
            intShiftStrY<< coordinateY;
            string intToStringY = intShiftStrY.str();
            intToStringX.append("$");
            intToStringX.append(intToStringY);
            intToStringX.append("$");
            intToStringX.append("B");
            intToStringX.append("#");
            char *copyX =new char [intToStringX.length()+1];
            strcpy(copyX, intToStringX.c_str());
            data[index++]=copyX;}
            //   circle center
            circle(mRGBA, center, 3, Scalar(0, 0, 0), -1, 8, 0);
            // circle outline
            circle(mRGBA, center, radius, Scalar(255, 255, 255), 0, 8, 0);
        }
        else if (mean(mask_red, mask)[0] > 130) {
            //red ball
            // circle center
            circle(mRGBA, center, 3, Scalar(0, 0, 0), -1, 8, 0);
            // circle outline
            circle(mRGBA, center, radius, Scalar(255, 255, 255), 0, 8, 0);
        }
        else {
            //no ball
            // circle center
            circle(mRGBA, center, 3, Scalar(0, 0, 0), -1, 8, 0);
            // circle outline
            circle(mRGBA, center, radius, Scalar(255, 255, 255), 0, 8, 0);
        }

    }

    ret = (jobjectArray) env->NewObjectArray(sizeof(&data), env->FindClass("java/lang/String"),
                                             env->NewStringUTF(""));


    for (i = 0; i < sizeof(&data); i++)
        env->SetObjectArrayElement(ret, i, env->NewStringUTF(data[i]));

    return (ret);


}


}
