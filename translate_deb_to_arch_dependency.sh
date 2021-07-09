#!/bin/bash

# This script takes a name of debian package name and outputs suggested arch linux package name

# Making it in individual folder to support multi processing
tmp_dir=$(mktemp -d -t deb_to_arch_${line}-$(date +%Y-%m-%d-%H-%M-%S)-XXX)
cd $tmp_dir

rm -rf tmp-mapdeps-pkg
mkdir -p tmp-mapdeps-pkg/DEBIAN
cat << EOF  > tmp-mapdeps-pkg/DEBIAN/control
Package: tmp-mapdeps-pkg
Version: 1.0-1
Section: base
Priority: optional
Architecture: amd64
Depends: $1
Maintainer: Your Name <you@email.com>
Description: Temporary package to workaround https://github.com/helixarch/debtap/issues/41
EOF

dpkg-deb --build tmp-mapdeps-pkg > /dev/null

debtap -P -Q tmp-mapdeps-pkg.deb 2>/dev/null > tmpfile
if grep "Warning: These dependencies" tmpfile > /dev/null; then
    echo could_not_translate
    rm tmp-mapdeps-pkg.deb tmpfile
    rm -rf tmp-mapdeps-pkg
    exit 1
fi

cat tmp-mapdeps-pkg/PKGBUILD | grep depends | sed 's/depends=('\''//' | sed 's/'\'' '\''/\n/g' | sed 's/'\'')//g'
rm tmp-mapdeps-pkg.deb tmpfile
rm -rf tmp-mapdeps-pkg 

cd ..
rm -rf $tmp_dir
