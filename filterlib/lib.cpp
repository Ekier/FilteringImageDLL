#include "lib.h"

double * test(int x, int y, double * pixels, double * newPixels, double * mask)
{
	double sum = 0;
	for(int i = 0; i < 9; ++i)
		sum += mask[i];

		for (int i = 1; i < y-1; ++i){
			for (int j = 1; j < x-1; ++j){
				newPixels[i*x+j] = (pixels[(i-1)*x+j-1]*mask[0] + pixels[(i-1)*x+j]*mask[1] + pixels[(i-1)*x+j+1]*mask[2] + pixels[i*x+j-1]*mask[3] + pixels[i*x+j]*mask[4] + pixels[i*x+j+1]*mask[5] + pixels[(i+1)*x+j-1]*mask[6] + pixels[(i+1)*x+j]*mask[7] + pixels[(i+1)*x+j+1]*mask[8]);	
			}
		}

	// gorny rzad:
	for(int j = 1; j < x - 1; ++j){
		newPixels[j] = (pixels[(y-1)*x+j-1]*mask[0] + pixels[(y-1)*x+j]*mask[1] + pixels[(y-1)*x+j+1]*mask[2] + pixels[j-1]*mask[3] + pixels[j]*mask[4] + pixels[j+1]*mask[5] + pixels[x+j-1]*mask[6] + pixels[x+j]*mask[7] + pixels[x+j+1]*mask[8]);
	}

	// dolny rzad:
	for(int j = 1; j < x - 1; ++j){
		newPixels[(y-1)*x+j] = (pixels[(y-2)*x+j-1]*mask[0] + pixels[(y-2)*x+j]*mask[1] + pixels[(y-2)*x+j+1]*mask[2] + pixels[(y-1)*x+j-1]*mask[3] + pixels[(y-1)*x+j]*mask[4] + pixels[(y-1)*x+j+1]*mask[5] + pixels[j-1]*mask[6] + pixels[j]*mask[7] + pixels[j+1]*mask[8]);
	}

	// lewa kolumna: j = 0
	for(int i = 1; i < y - 1; ++i){
		newPixels[i*x] = (pixels[(i-1)*x+x-1]*mask[0] + pixels[(i-1)*x]*mask[1] + pixels[(i-1)*x+1]*mask[2] + pixels[i*x+x-1]*mask[3] + pixels[i*x]*mask[4] + pixels[i*x+1]*mask[5] + pixels[(i+1)*x+x-1]*mask[6] + pixels[(i+1)*x]*mask[7] + pixels[(i+1)*x+1]*mask[8]);	
	}

	// prawa kolumna: j = x-1
	for(int i = 1; i < y - 1; ++i){
		newPixels[i*x+x-1] = (pixels[(i-1)*x+x-2]*mask[0] + pixels[(i-1)*x+x-1]*mask[1] + pixels[(i-1)*x]*mask[2] + pixels[i*x+x-2]*mask[3] + pixels[i*x+x-1]*mask[4] + pixels[i*x]*mask[5] + pixels[(i+1)*x+x-2]*mask[6] + pixels[(i+1)*x+x-1]*mask[7] + pixels[(i+1)*x]*mask[8]);	
	}

	// lewy gorny rog:
	newPixels[0] = (pixels[(y-1)*x+x-1]*mask[0] + pixels[(y-1)*x]*mask[1] + pixels[(y-1)*x+1]*mask[2] + pixels[x-1]*mask[3] + pixels[0]*mask[4] + pixels[1]*mask[5] + pixels[x+y-1]*mask[6] + pixels[x]*mask[7] + pixels[x+1]*mask[8]);	

	// prawy gorny rog:
	newPixels[x-1] = (pixels[(y-1)*x+x-2]*mask[0] + pixels[(y-1)*x+x-1]*mask[1] + pixels[(y-1)*x]*mask[2] + pixels[x-2]*mask[3] + pixels[x-1]*mask[4] + pixels[0]*mask[5] + pixels[x+x-2]*mask[6] + pixels[x+x-1]*mask[7] + pixels[x]*mask[8]);	

	// lewy dolny rog:
	newPixels[(y-1)*x] = (pixels[(y-2)*x+x-1]*mask[0] + pixels[(y-2)*x]*mask[1] + pixels[(y-2)*x+1]*mask[2] + pixels[(y-1)*x+x-1]*mask[3] + pixels[(y-1)*x]*mask[4] + pixels[(y-1)*x+1]*mask[5] + pixels[x-1]*mask[6] + pixels[0]*mask[7] + pixels[1]*mask[8]);	

	// prawy dolny rog:
	newPixels[(y-1)*x+x-1] = (pixels[(y-2)*x+x-2]*mask[0] + pixels[(y-2)*x+x-1]*mask[1] + pixels[(y-2)*x]*mask[2] + pixels[(y-1)*x+x-2]*mask[3] + pixels[(y-1)*x+x-1]*mask[4] + pixels[(y-1)*x]*mask[5] + pixels[x-2]*mask[6] + pixels[x-1]*mask[7] + pixels[0]*mask[8]);	

	if(sum != 0){
		for (int i = 0; i < y; ++i){
			for (int j = 0; j < x; ++j){
				newPixels[i*x+j] /= sum;
			}
		}
	}
	return newPixels;
}
