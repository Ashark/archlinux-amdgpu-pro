#!/bin/bash

# This script unpacks all deb packages (control and data). It is for simplifying operations of checking preinst scripts, making list of licenses hashes and so on.

. ./versions
ARCHIVE=amdgpu-pro-$pkgver_base-$pkgver_build-ubuntu-$ubuntu_ver.tar.xz
tar -xf $ARCHIVE
cd ${ARCHIVE%.tar.xz}

# Распараллелить распаковку?
tmpdir=unpacked_debs; rm -rf "$tmpdir"; mkdir "$tmpdir";
for file in $(ls *deb);
do
    echo processing $file
    cd "$tmpdir"; mkdir $file; cd $file
    ar x ../../$file
    rm debian-binary
    tar -xf control.tar.xz; rm control.tar.xz;
    tar -xf data.tar.xz; rm data.tar.xz;

    find usr/share/doc -type f -name 'copyright' -exec mv {} . \;
    find usr/share/doc -type f -name "changelog.Debian.gz" -exec mv {} . \;

    find . -type d -empty -delete

    cd ../..
done
