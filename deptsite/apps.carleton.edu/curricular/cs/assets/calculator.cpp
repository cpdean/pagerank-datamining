//////////////////////////////////////////////////////////////////
//
//	calculator.cpp
//
//	mtie 1-7-99
//
//	compile: 
//		g++ -c calculator.cpp
//	
//	compile output:  
//		calculator.o
//
//////////////////////////////////////////////////////////////////

#include "calculator.h"

float	Calculator::calculator_Add ( float a, float b )
{
	temp_var = a + b;
	return( temp_var );
}

float	Calculator::calculator_Multiply ( float a, float b )
{
	temp_var = a * b;
	return( temp_var );
}
