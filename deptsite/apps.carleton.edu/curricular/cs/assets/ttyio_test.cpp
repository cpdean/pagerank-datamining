/*
    ttyio_test.cpp:   a simple program that tests the locally written
        ttyiofunction library.  For more information about the
        Carleton ttyiofunction library contact mtie@carleton.edu.
        For information about how to build your own ttyiofunctions
        refer to the book

            "Advanced C Programming for Displays"
                by
            Marc J. Rochkind

    to compile ttyio_test.cpp:
        g++ -o ttyio_test ttyio_test.cpp -lttyiofunctions

    -mtie 3/27/01
*/

#include <ttyiofunctions.h>
#include <iostream.h>

void main()
{
    char c='z';

    //initializes the screen and sets it up to break
    inittty();
    ttycbreak();

    while(c != 'q')  //this is the event loop
    {
        //if there is a keypress
        if( kbhit() )
        {
            //grab the character
            cin >> c;

            //display the character
            cout << "the character entered was -" << c << "-"<< endl;
        }
    }

    //restore the terminal to normal mode
    ttynorm();
}