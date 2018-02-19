/*
 * processing.cpp
 *
 *  Created on: Feb 14, 2018
 *      Author: Worse2Worst
 */

#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <streambuf>
#include <cstdlib>
#include <map>
#include "processing.h"
#include <math.h>
#include <set>
using namespace std;

float distance(const pair<int,int> &v1,const pair<int,int> &v2){
	float x1=v1.first;
	float y1=v1.second;
	float x2=v2.first;
	float y2=v2.second;
	float dist = (x1-x2)*(x1-x2)+ (y1-y2)*(y1-y2);
	dist = sqrt(dist);
	return dist;
}


Data::Data(string filePath){
	string str;
	ifstream infile;
	infile.open(filePath);
	infile>>numVehicles;
	infile>>loadCapacities;
	infile>>speed;
	if (speed<=0){
		speed=1;
	}
	int index,x,y,demand,ET,LT,serviceTime,pickupIndex,deliveryIndex;
	infile>>index>>x>>y>>demand>>ET>>LT>>serviceTime>>pickupIndex>>deliveryIndex;
	while (infile){
		//The data is right
		pair<int,int> coordination =make_pair(x,y);
		LOCATIONS.push_back(coordination);
		DEMANDS.push_back(demand);
		timeWindows.push_back(make_pair(ET,LT));
		serviceTimes.push_back(serviceTime);
		deliveryIndices.push_back(deliveryIndex);
		pickupIndices.push_back(pickupIndex);
		if (pickupIndex == 0){
					requestTypes.push_back("pickup");
				}else{
					requestTypes.push_back("delivery");
				}
		// load new line
		infile>>index>>x>>y>>demand>>ET>>LT>>serviceTime>>pickupIndex>>deliveryIndex;
		}
	DISTANCES = vector<vector<float>>(LOCATIONS.size(), std::vector<float>(LOCATIONS.size(), 0));
	DURATIONS = vector<vector<float>>(LOCATIONS.size(), std::vector<float>(LOCATIONS.size(), 0));
	infile.close();
	timeWindows[0] = make_pair(0,1147483647);
	requestTypes[0] = "DEPOT";

	//Making a DISTANCES table
	/*
	for (auto const &v1:LOCATIONS){
		for(auto const &v2:LOCATIONS){
			auto index = make_pair(v1,v2);
			DISTANCES[index] = distance(v1,v2);
		}
	}
	*/
	for (int i = 0;i<LOCATIONS.size();i++){
		for (int j = 0;j<LOCATIONS.size();j++){
			DISTANCES[i][j] = distance(LOCATIONS[i],LOCATIONS[j]);
		}
	}

	//Making a DURATIONS table
	for (int i = 0;i<LOCATIONS.size();i++){
		for (int j = 0;j<LOCATIONS.size();j++){
			DURATIONS[i][j] = (DISTANCES[i][j]/speed)+serviceTimes[i];
		}
	}

	//MAKING a REQUESTS
	for (int i = 0;i<LOCATIONS.size();i++){
		if(requestTypes[i].compare("pickup")==0){
			for (int j = 0;j<LOCATIONS.size();j++){
				if(i ==pickupIndices[j]){
					auto temp = make_pair(i,j);
					REQUESTS.insert(temp);
				}
			}
		}
		}
}


