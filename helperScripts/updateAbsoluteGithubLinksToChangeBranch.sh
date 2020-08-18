#!/bin/bash

set -e

usage="

\e[91mMissing argument!\e[39m

\e[97mHelp\e[39m

$(basename "$0") - This script aids to help change the GitHub branch absoulte path easily through a semi-automated way.
The script requires two arguments. One is the current branch [\e[94mbranch_name\e[39m] and the second argument is the target branch [\e[94mbranch_name\e[39m].



\e[97mCommon uses:\e[39m

./$(basename "$0") master devel
./$(basename "$0") devel master



\e[97m The searching location path:\e[39m

../sphinx/source/*.rst
../tutorials/

"

if [ -z "$1" ] || [ -z "$2" ]; then
        echo -e "$usage"
        exit 0
fi

header="


##########################################
\e[93m$(basename "$0")\e[39m
##########################################


"
echo -e "$header"

echo -e "Changing tutorial branch from: \e[31m$1\e[39m to: \e[32m$2\e[39m"
echo ''


no_file=0

grep -r "https://raw.githubusercontent.com/occopus/docs/$1/tutorials/" ../sphinx/source/*.rst > /dev/null || no_file="1" &&
grep -r "https://raw.githubusercontent.com/occopus/docs/$1/tutorials/" ../tutorials/ > /dev/null && no_file="0"|| no_file="1"

if [ $no_file -eq 1 ]
then
    echo ''
    echo -e "\e[91mI've not found \e[93m$1\e[91m branch in the docs... Exiting\e[39m"
    echo ''
    exit 0
fi

files=`grep -r "https://raw.githubusercontent.com/occopus/docs/$1/tutorials/" ../sphinx/source/*.rst | cut -d ":" -f1 | uniq &&
grep -r "https://raw.githubusercontent.com/occopus/docs/$1/tutorials/" ../tutorials/ | cut -d ":" -f1 | uniq ||
grep -r "https://raw.githubusercontent.com/occopus/docs/$1/tutorials/" ../tutorials/ | cut -d ":" -f1 | uniq`

echo -e '\e[94mFound document(s):\e[39m'
echo "$files"
echo ''

function proceed (){
    echo ''
    for t in ${files[@]}; do
        sed -i "s/https:\/\/raw.githubusercontent.com\/occopus\/docs\/$1\/tutorials\//https:\/\/raw.githubusercontent.com\/occopus\/docs\/$2\/tutorials\//g" $t
        echo -e "\e[92m $t Done"
    done

    echo ''
    echo -e 'All file(s) changed! Exiting...\e[39m'
    echo ''
}

while true; do
    read -p "Are you sure you want to continue? (y/n)" yn
    case $yn in
        [Yy]* ) proceed $1 $2; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

