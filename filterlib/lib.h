#pragma once  

#ifdef TESTLIB_EXPORTS  
#define LIB_API __declspec(dllexport)   
#else  
#define LIB_API __declspec(dllimport)   
#endif  

extern "C"
{
	double LIB_API * test(int x, int y, double * pixels, double * newPixels, double * mask);
}
