#!/bin/bash 

bash uninstall_packages_group.sh && \
echo "Removing *pkg.tar.zst files"; rm -f *.pkg.tar.zst && \
echo "Generating PKGBUILD..."; ./build.sh && \
echo "Invoking makepkg..."; makepkg && \
echo "Updating local repository..."; bash update-local-repo.sh 1>/dev/null
