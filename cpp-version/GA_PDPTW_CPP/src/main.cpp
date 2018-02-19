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
#include <fstream>
#include <streambuf>
#include "map"
#include <set>
using namespace std;

int main() {

	const clock_t begin_time = clock();
	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!

	Data data = Data("C:/Users/Worse2Worst/Desktop/Senior-Project/cpp-version/GA_PDPTW_CPP/TestInstances/LiLim/pdp_100/lc107.txt");

	int  numVehicles = data.numVehicles;
	int loadCapacities = data.loadCapacities;
	float speed = data.speed;
	vector<pair<int,int>> LOCATIONS = data.LOCATIONS;
	vector<int>DEMANDS = data.DEMANDS;
	vector<pair<int,int>> timeWindows = data.timeWindows;
	vector<int> serviceTimes = data.serviceTimes;
	vector<string> requestTypes= data.requestTypes;
	auto DISTANCES = data.DISTANCES;
	auto DURATIONS = data.DURATIONS;
	auto REQUESTS = data.REQUESTS;
	for (const auto &req : REQUESTS)
	  cout << req.first<<","<<req.second<<endl;


	/*
	for (int i = 0;i<LOCATIONS.size();i++){
		for (int j = 0;j<LOCATIONS.size();j++){
			cout <<DURATIONS[i][j] <<" ,";
		}
		cout<<endl;
	}
	 */


	// cout << timeWindows[0].second << ","<<endl;
	//vector<int> pickupSiblings = ;
	//vector<int> deliverySiblings =;
	//vector<string> requestTypes =;
	cout <<"-----used:" <<float( clock () - begin_time ) /  CLOCKS_PER_SEC <<" -----seconds"<<endl;
	return 0;
}
