//////////////////////////////////////////////////////////////////
//
//	mycalctester.cpp
//
//	mtie 1-7-99
//
//	simple program to test Calculator class
//
//	compile: 
//		g++ -o mycalctester mycalctester.cpp calculator.o
//	
//	compile output:  
//		mycalctester
//
//////////////////////////////////////////////////////////////////

#include <iostream.h>
#include "calculator.h"

void main (void)
{
	float x, y;
	float result;
	
	Calculator mycalc;
	
	x = 10;
	y = 10;
	
	cout << " x = " << x << endl;
	cout << " y = " << y << endl;
	cout << endl;
	
	result = mycalc.calculator_Add (x, y);
	cout << " x + y = " << result << endl;
	cout << endl;

	result = mycalc.calculator_Multiply (x, y);
	cout << " x * y = " << result << endl;}
	