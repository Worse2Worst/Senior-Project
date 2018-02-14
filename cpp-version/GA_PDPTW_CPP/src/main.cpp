//============================================================================
// Name        : GA_PDPTW_CPP.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <string>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "processing.h"
using namespace std;

int main() {
	const clock_t begin_time = clock();
	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!

	int a[] = {1,2,3,4,5};

	for (auto x:a){
		cout << x;
	}
	cout << float( clock () - begin_time ) /  CLOCKS_PER_SEC <<endl;
	return 0;
}
