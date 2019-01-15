if [[ `pacman -Q python-debian 2>&1` == "error: package 'python-debian' was not found" ]]; then
    echo "You need to install python-debian package"
    exit 1
else
    python gen-PKGBUILD.py > PKGBUILD
fi
