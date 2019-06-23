#!/bin/bash 

# Add the following to your /etc/pacman.conf:
# [amdgpu-dev]
# SigLevel = Optional TrustAll
# Server = File:///home/andrew/Development/amdgpu-19.20/archlinux-amdgpu/ # fix path to your development directory

bash uninstall_packages_group.sh && \
echo "Removing *pkg.tar files"; rm -f *.pkg.tar && \
echo "Generating PKGBUILD..."; ./build.sh && \
echo "Invoking makepkg..."; makepkg && \
echo "Updating local repository..."; bash update-local-repo.sh 1>/dev/null
