#!/bin/bash

all_pkgs_in_repo=$(pacman -Sl amdgpu-dev | cut -f2 -d" ")
if [ "$all_pkgs_in_repo" != "" ]; then
    repo-remove amdgpu-dev.db.tar.gz $all_pkgs_in_repo
fi

repo-add amdgpu-dev.db.tar.gz  *.pkg.tar

sudo pacman -Sy
