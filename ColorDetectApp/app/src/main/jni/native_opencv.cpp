#include "native_opencv.h"

using namespace std;
using namespace cv;

extern "C" {
JNIEXPORT void Java_mobileRobot_imageProcessing_android_colorDetector_MainActivity_salt(
        JNIEnv *env, jobject instance,
        jlong matAddrGray,
        jlong matAddrRGBA,
        jint nbrElem) {

    Mat &imgGray = *(Mat *) matAddrGray;
    Mat &mRGBA = *(Mat *) matAddrRGBA;
    Mat imgHSV;
    cvtColor(mRGBA, imgHSV, COLOR_RGB2HSV);


    Mat mask_blue;
    Mat mask_red;
    inRange(imgHSV, Scalar(100, 50, 50), Scalar(140, 255, 255), mask_blue);
    //morphological opening (remove small objects from the foreground)
    erode(mask_blue, mask_blue, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
    dilate(mask_blue, mask_blue,getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
    //morphological closing (fill small holes in the foreground)
    dilate(mask_blue, mask_blue,getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
    erode(mask_blue, mask_blue,getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));


      inRange(imgHSV, Scalar(170, 50, 50), Scalar(179, 255, 255), mask_red);
     //morphological opening (remove small objects from the foreground)
     erode(mask_red, mask_red,getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
     dilate(mask_red, mask_red,getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
     //morphological closing (fill small holes in the foreground)
     dilate(mask_red, mask_red,getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
     erode(mask_red, mask_red,getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));


    // Kreiserkennung auf dem Graustufenbild
 /*   medianBlur(imgGray, imgGray, 5);
    //vector < Vec3f > circles;
    //HoughCircles(imgGray, circles, CV_HOUGH_GRADIENT, 1, 50, 50, 30, 20, 100);

    vector<Vec3f> circles;
    HoughCircles(imgGray, circles, CV_HOUGH_GRADIENT,
                 1,   // accumulator resolution (size of the image / 2)
                 50,  // minimum distance between two circles
                 50, // Canny high threshold
                 30, // minimum number of votes
                 20, 100);*/

    /*string message= "no ball!";
    if (!circles.empty()) {
        for (size_t i = 0; i < circles.size(); i++) {
            Mat mask(Mat::zeros(imgGray.rows, imgGray.cols, CV_8UC1));
            int radius = cvRound(circles[i][2]);
            Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
            circle(mask, center, radius / 3, Scalar(255, 255, 255), radius / 2, 1);


            if (mean(mask_blue, mask)[0] > 130) {
                // blauen Ball gefunden
                cout << "blauen Ball gefunden" << endl;
                message = "Blue ball has been found";
            }
            else if (mean(mask_red, mask)[0] > 130) {
                // roten Ball gefunden
                cout << "roten Ball gefunden" << endl;
                message = "Red ball has been found";
            }
            else {
                // anderes rundes Objekt gefunden
                cout << "anderes rundes Objekt gefunden" << endl;
                message = "Another ball has been found";


                //					Point center(cvRound (circles[i][0]), cvRound (circles[i][1]));
                //					int radius = cvRound(circles[i][2]);
                //					// circle center
                //					circle(imgOriginal, center, 3, Scalar(0, 255, 0), -1, 8, 0);
                //					// circle outline
                //					circle(imgOriginal, center, radius, Scalar(0, 0, 255), 3, 8, 0);
            }


            //				Point center(cvRound (circles[i][0]), cvRound (circles[i][1]));
            //				int radius = cvRound(circles[i][2]);
            //				// circle center
            //				circle(src, center, 3, Scalar(0, 255, 0), -1, 8, 0);
            //				// circle outline
            //				circle(src, center, radius, Scalar(0, 0, 255), 3, 8, 0);
        }
    }*/

//	if (!circles.empty())
//	{
//		for (size_t i = 0; i < circles.size(); i)
//		{
//////			Mat mask(Mat::zeros(mGr.rows, mGr.cols, CV_8UC1));
//////			int radius = cvRound(circles[i][2]);
//			Point center(cvRound (circles[i][0]), cvRound (circles[i][1]));
//			int radius = cvRound(circles[i][2]);
////			// circle center
//			circle(mGr, center, 3, Scalar(255, 255, 255), -1, 8, 0);
////			// circle outline
//			circle(mGr, center, radius, Scalar(0, 0, 0), 3, 8, 0);
////
//		}
////
//	}
    //return message;
}


}

