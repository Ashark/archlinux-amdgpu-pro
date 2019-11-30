#!/bin/bash

# This script prepares a template for pkgbuild_packages in gen-PKGBUILD.py

cat packages_map.py | cut -s -f4 -d"'" > tmp_arch_packages.txt
echo "" > tmp_already_used.txt
for line in $(cat tmp_arch_packages.txt); do
    if grep -Fxq "$line" tmp_already_used.txt; then continue;
    else
        echo $line >> tmp_already_used.txt
        echo -e "        '$line': Package(  ),";
    fi
done
rm tmp_already_used.txt
rm tmp_arch_packages.txt

