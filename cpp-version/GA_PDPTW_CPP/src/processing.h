/*
 * processing.h
 *
 *  Created on: Feb 14, 2018
 *      Author: Worse2Worst
 */

#ifndef PROCESSING_H_
#define PROCESSING_H_
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <streambuf>
#include <cstdlib>
#include <map>
#include <set>
using namespace std;


class Data{
public:
	int  numVehicles, loadCapacities;
	float speed;
	vector<pair<int,int>>LOCATIONS;
	vector<int>DEMANDS;
	vector<pair<int,int>> timeWindows;
	vector<int> serviceTimes;
	vector<int> pickupSiblings;
	vector<int> deliverySiblings;
	vector<string> requestTypes;
	vector<vector<float>> DISTANCES;
	vector<vector<float>> DURATIONS;
	vector<int> deliveryIndices;
	vector<int> pickupIndices;
	set<pair<int,int>> REQUESTS;

public:
		Data(string filePath);


/*
	const vector<int>& getDeliverySiblings() const {
		return deliverySiblings;
	}

	const vector<int>& getDemands() const {
		return DEMANDS;
	}

	int getLoadCapacities() const {
		return loadCapacities;
	}

	const vector<pair<int, int> >& getLocations() const {
		return LOCATIONS;
	}

	int getNumVehicles() const {
		return numVehicles;
	}

	const vector<int>& getPickupSiblings() const {
		return pickupSiblings;
	}

	const vector<string>& getRequestTypes() const {
		return requestTypes;
	}

	const vector<int>& getServiceTimes() const {
		return serviceTimes;
	}

	float getSpeed() const {
		return speed;
	}

	const vector<pair<int, int> >& getTimeWindows() const {
		return timeWindows;
	}
	*/
};




#endif /* PROCESSING_H_ */
