#!/bin/bash
set -euo pipefail

# This script takes a Debian package name and outputs suggested Arch Linux package name

pkg_name="$1"

tmp_dir=$(mktemp -d -t deb_to_arch_${pkg_name}-$(date +%Y-%m-%d-%H-%M-%S)-XXX)
cd "$tmp_dir"

mkdir -p tmp-mapdeps-pkg/DEBIAN
cat << EOF > tmp-mapdeps-pkg/DEBIAN/control
Package: tmp-mapdeps-pkg
Version: 1.0-1
Section: base
Priority: optional
Architecture: amd64
Depends: $pkg_name
Maintainer: Your Name <you@email.com>
Description: Temporary package to workaround https://github.com/helixarch/debtap/issues/41
EOF

dpkg-deb --build tmp-mapdeps-pkg > /dev/null

debtap -P -Q tmp-mapdeps-pkg.deb 2>/dev/null > tmpfile

if grep -q "Warning: These dependencies" tmpfile; then
    echo could_not_translate
    rm tmp-mapdeps-pkg.deb tmpfile
    rm -rf tmp-mapdeps-pkg
    cd ..
    rm -rf "$tmp_dir"
    exit 1
fi

if [ ! -f tmp-mapdeps-pkg/PKGBUILD ]; then
    echo could_not_translate
    rm tmp-mapdeps-pkg.deb tmpfile
    rm -rf tmp-mapdeps-pkg
    cd ..
    rm -rf "$tmp_dir"
    exit 1
fi

grep depends tmp-mapdeps-pkg/PKGBUILD \
    | sed "s/depends=('//" \
    | sed "s/' '/\n/g" \
    | sed "s/')//g"

rm tmp-mapdeps-pkg.deb tmpfile
rm -rf tmp-mapdeps-pkg
cd ..
rm -rf "$tmp_dir"

