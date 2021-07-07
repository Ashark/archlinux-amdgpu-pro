## Contributing

Please run `reposetup.sh` prior to committing. This will install a git hook
that will automatically re-generate `PKGBUILD` and `.SRCINFO` as needed
before the commit completes.

## Steps to do when new version is released
1. Download an amd bundle archive and place it to root of the repository.
1. Change versions in `versions` file.
1. Change pkgrel, url_ref in `gen-PKGBUILD.py` file.
1. Run `./unpack_all_deb_packages.sh`
1. Copy the file archive_name_dir/"Packages" to "Packages_extracted" with the following command:  
   `. versions; cp amdgpu-pro-$pkgver_base-$pkgver_build-ubuntu-$ubuntu_ver/Packages Packages-extracted`
1. Run `./gen_packages_map.sh > packages_map.py`  
   See differences with `git diff -w packages_map.py`  
   If there are differences, then make adjustments to gen_packages_map.sh if needed. Especially, look for the new appeared packages (they will have empty comment) and removed packages. If there are new or removed packages, then use make_pkgbuild_pkgs_template.sh and edit gen-PKGBUILD.py
1. Run `sudo debtap -u`. Then run `./gen_replace_deps.sh > replace_deps.py`  
   See differences with `git diff -w replace_deps.py`  
   If there are differences, then make adjustments to gen_replace_deps.sh if needed.
1. Run `./extract_transaction_scripts_and_triggers.sh`.  
   Compare transaction scripts and triggers from current and previous driver version in opened meld window.
   If you see explicit version numbers in file names, add additional rename instructions in extract_transaction_scripts_and_triggers.sh. This will help you to compare contents of the files in meld.  
   If there are changes, see if it is needed to convert them to pacman .install files or hooks.
1. Create a local repository (if not done yet) by adding the following to your /etc/pacman.conf:
    ```
    [amdgpu-dev]
    SigLevel = Optional TrustAll
    Server = File:///home/andrew/Development/archlinux-amdgpu-pro/ # edit path to your development directory
    ```
1. Regenerate PKGBUILD with `./remake_all.sh`
1. If you notice empty licence in PKGBUILD, add its hash to the licenses_hashes_map in gen-PKGBUILD.py
1. Install from local repository and test it.
1. Update AUR package: copy PKGBUILD, .SRCINFO and other files as needed.
