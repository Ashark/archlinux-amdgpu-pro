#!/bin/bash 

bash uninstall_packages_group.sh && \
echo "Removing *pkg.tar files"; rm -f *.pkg.tar && \
echo "Generating PKGBUILD..."; ./build.sh && \
echo "Invoking makepkg..."; makepkg && \
echo "Updating local repository..."; bash update-local-repo.sh 1>/dev/null
