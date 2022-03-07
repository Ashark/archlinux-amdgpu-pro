## Contributing

Please run `reposetup.sh` prior to committing. This will install a git hook
that will automatically re-generate `PKGBUILD` and `.SRCINFO` as needed
before the commit completes.

## Steps to do when new version is released
1. Go to http://repo.radeon.com/amdgpu/ and see if there is a new version available.
1. Change versions in `versions` file.
1. Change pkgrel, url_ref in `gen-PKGBUILD.py` file.
1. Install aptly if not done yet.
1. Update the local mirror
   Note that `latest` link is not actually latest version.
   ```
   #ver=latest
   ver=21.50.2
   aptly -ignore-signatures mirror create agpro-$ver http://repo.radeon.com/amdgpu/$ver/ubuntu focal proprietary 
   aptly -ignore-signatures mirror update agpro-$ver

   aptly publish drop focal
   aptly snapshot create snapshot-$(date +%F) from mirror agpro-$ver
   aptly publish snapshot snapshot-$(date +%F) # When it will ask a password, do not enter empty or it will fail
   ```

   Now in ~/.aptly/public/pool (not in ~/.aptly/pool/) there will be our packages.
1. Run `./unpack_all_deb_packages.sh`
1. Bring the "Packages" file to "Packages-extracted" with the following command:  
   `cat ~/.aptly/public/dists/focal/proprietary/binary-amd64/Packages ~/.aptly/public/dists/focal/proprietary/binary-i386/Packages > Packages-extracted`
   Do not forget to replace "focal" after new distibution is released. Note: bionic=18.04, focal=20.04.
   
   Manually remove duplicated entries. See more info in the gen_packages_map.sh in the beginning comment.

   There also could be such way: <s>`aptly package show "Name (~ .*)" > Packages-extracted`</s>. For some reason, this method shows filenames without relative path. So cannot use that until inversigate how to fix.
   
   Also files can be seen here (convenience links):
   http://repo.radeon.com/amdgpu/latest/ubuntu/dists/focal/proprietary/binary-amd64/Packages  
   http://repo.radeon.com/amdgpu/latest/ubuntu/dists/focal/proprietary/binary-i386/Packages
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
1. If you notice empty license in PKGBUILD, add its hash to the licenses_hashes_map in gen-PKGBUILD.py
1. Install from local repository and test it.
1. Commit to project repo (not the aur) with the tag.
    ```
    git tag $(source PKGBUILD; echo v${major}_${minor}-${pkgrel})
    git push origin $(source PKGBUILD; echo v${major}_${minor}-${pkgrel})
    ```
   Create a release on github pointing to the new tag.
1. Update AUR package: copy PKGBUILD, .SRCINFO and other files as needed.
