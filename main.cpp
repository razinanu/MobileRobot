#include <iostream>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

using namespace cv;
using namespace std;

int main(int argc, char** argv) {



	VideoCapture cap(0); //capture the video from web cam

	if (!cap.isOpened())  // if not success, exit program
	{
		cout << "Cannot open the web cam" << endl;
		return -1;
	}

	namedWindow("Control", CV_WINDOW_AUTOSIZE); //create a window called "Control"

	while (true) {
		Mat imgOriginal;

		bool bSuccess = cap.read(imgOriginal); // read a new frame from video

		if (!bSuccess) //if not success, break loop
		{
			cout << "Cannot read a frame from video stream" << endl;
			break;
		}


		Mat imgHSV;
		Mat imgGray;

		cvtColor(imgOriginal, imgHSV, COLOR_BGR2HSV); //Convert the captured frame from BGR to HSV
		cvtColor(imgOriginal, imgGray, COLOR_BGR2GRAY);

		Mat mask_blue;
		Mat mask_red;

		inRange(imgHSV, Scalar(100, 50, 50), Scalar(140, 255, 255), mask_blue); //Threshold the image
		inRange(imgHSV, Scalar(170, 50, 50), Scalar(179, 255, 255), mask_red); //Threshold the image

		//morphological opening (remove small objects from the foreground)
		erode(mask_blue, mask_blue,
				getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		dilate(mask_blue, mask_blue,
				getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		//morphological opening (remove small objects from the foreground)
		erode(mask_red, mask_red,
				getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		dilate(mask_red, mask_red,
				getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));

		//morphological closing (fill small holes in the foreground)
		dilate(mask_blue, mask_blue,
				getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		erode(mask_blue, mask_blue,
				getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		//morphological closing (fill small holes in the foreground)
		dilate(mask_red, mask_red,
				getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		erode(mask_red, mask_red,
				getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));



		// Kreiserkennung auf dem Graustufenbild
		medianBlur(imgGray, imgGray, 5);
//		vector < Vec3f > circles;
//		HoughCircles(imgGray, circles, CV_HOUGH_GRADIENT, 1, 50, 50, 30, 20,
//				100);

		vector<Vec3f> circles;
	    HoughCircles(imgGray, circles, CV_HOUGH_GRADIENT,
	          1,   // accumulator resolution (size of the image / 2)
	          50,  // minimum distance between two circles
	          50, // Canny high threshold
	          30, // minimum number of votes
	          20, 100); // min and max radius



		if (!circles.empty())
		{
			for (size_t i = 0; i < circles.size(); i++)
			{
				Mat mask(Mat::zeros(imgGray.rows, imgGray.cols, CV_8UC1));
				int radius = cvRound(circles[i][2]);
				Point center(cvRound (circles[i][0]), cvRound (circles[i][1]));
				circle(mask, center, radius/3, Scalar(255, 255, 255), radius/2, 1);


				if (mean(mask_blue,mask)[0] > 130)
				{
					// blauen Ball gefunden
					cout << "blauen Ball gefunden" << endl;
				}
				else if (mean(mask_red,mask)[0] > 130)
				{
					// roten Ball gefunden
					cout << "roten Ball gefunden" << endl;
				}
				else
				{
					// anderes rundes Objekt gefunden
					cout << "anderes rundes Objekt gefunden" << endl;

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
		}


		//imshow("Thresholded Image", imgThresholded); //show the thresholded image
		imshow("Original", imgOriginal); //show the original image
		imshow("mask_red", mask_red);
		imshow("mask_blue", mask_blue);


		if (waitKey(30) == 27) //wait for 'esc' key press for 30ms. If 'esc' key is pressed, break loop
		{
			cout << "esc key is pressed by user" << endl;
			break;
		}
	}



	return 0;

}
