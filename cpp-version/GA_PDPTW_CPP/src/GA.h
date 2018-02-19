/*
 * GA.h
 *
 *  Created on: Feb 15, 2018
 *      Author: Worse2Worst
 */
#include <set>
#include <vector>

#ifndef GA_H_
#define GA_H_

using namespace std;



class Gene{
public:
	int num;
	set<int> reqs;
	vector<int> route;
};


class chromosome{
public:
	vector<Gene> genes;

};













#endif /* GA_H_ */
