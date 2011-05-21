#!/bin/bash
# Running this copies all your comment files to the appropiate return folders
# on Collab.
# This file should be run from the directory with your comments.  It should be
# executable.  To do this:
# >chmod u+x return.sh
# or whatever you name this file.
# It takes two arguments, the coursenumber and the assignment name.
# See below for examples.

# if length of args is less than two
if [ ${#@} -lt 2 ]; then
  echo "Usage: $(basename $0) coursenumber assignmentname"
  echo "coursenumber: the name and number of the course as appears in Collab."
  echo -e "\texample: cs227-00-w05"
  echo "assignmentname: the name you give to an assignment."
  echo -e "\texample: if all your text files are named like"
  echo -e "\tpurringk_hashtable.txt, then hashtable would be the assignment name."
  exit 1;
fi

course="$1"
assignment="$2"
srcdir=`pwd`
coursedir="$HOME/Collab/Courses/cs/$course/Student Work/"

# for each user name in the course, copy
for user in "$coursedir"/*; do
    user=`basename "$user"`
    user=`echo $user | tr '[:upper:]' '[:lower:]'`
    commentfile="$(echo "$srcdir/$user"\_"$assignment.txt")"
    
    if [ -e "$commentfile" ]; then
	cp "$commentfile" "$coursedir/$user/return/" &&
	echo "Copied `basename "$commentfile"` to $user/return/"
    fi
done
