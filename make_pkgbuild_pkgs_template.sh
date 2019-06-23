#!/bin/bash

# This script prepares a template for pkgbuild_packages in gen-PKGBUILD.py

bash make_stupid_mapping.sh > tmp_stupid_mapping.txt

cat tmp_stupid_mapping.txt | cut -f4 -d"'" > tmp_arch_packages.txt
echo "" > tmp_already_used.txt
for line in $(cat tmp_arch_packages.txt); do
    if grep -Fxq "$line" tmp_already_used.txt; then continue;
    else
        echo $line >> tmp_already_used.txt
        echo -e "        '$line': Package(  ),";
    fi
done
rm tmp_already_used.txt
rm tmp_stupid_mapping.txt
