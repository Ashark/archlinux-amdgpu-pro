#!/bin/bash

pkgs_existing=$(pacman -Qg Radeon_Software_for_Linux | cut -f2 -d" ")

echo Removing: $pkgs_existing
sudo pacman -Rdd $pkgs_existing
