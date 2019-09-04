#!/bin/bash

OLD_FLAG=false

for i in "$@"
do
case $i in
    --old)
    OLD_FLAG=true
    ;;
esac
done

if [ $OLD_FLAG = true ];
then
    echo "Installing MySQL user and database for Irrigation Program"
    mysql -u root -p < mysql/old_setup.sql
else
    mysql -u root -p < mysql/setup.sql
fi
