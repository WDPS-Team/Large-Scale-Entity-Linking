#!/bin/bash

echo "loading hadoop binaries"
module load hadoop

if [ $? -eq 0 ]
then
  echo "all done"
else
  echo "something went wrong"
exit 1

