#!/bin/bash

pkgs_installed=$(pacman -Qg Radeon_Software_for_Linux | cut -f2 -d" ")
echo Uninstalling packages of Radeon_Software_for_Linux group...
if [[ $pkgs_installed != "" ]]; then
    echo Removing: $pkgs_installed
    sudo pacman -Rdd $pkgs_installed
else
    echo Nothing to uninstall.
fi

# remove cached packages, because they will be considered as currupted after newly created will be added to repo
echo Removing cached packages...
for file in $(expac -S %f $(pacman -Sg Radeon_Software_for_Linux | cut -f2 -d " ")); do
    if [ -f /var/cache/pacman/pkg/$file ]; then
        echo $file:
        sudo rm -v /var/cache/pacman/pkg/$file
    fi
done
