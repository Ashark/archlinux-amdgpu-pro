## Contributing

Please run `reposetup.sh` prior to committing. This will install a git hook
that will automatically re-generate `PKGBUILD` and `.SRCINFO` as needed
before the commit completes.

## Steps to do when new version is released
1. Change pkgver_base and pkgver_build in gen-PKGBUILD.py
2. Change url_ref in gen-PKGBUILD.py
3. Download an amd bundle archive
4. Change version of archive name in unpack_all_deb_packages.sh and run it.
5. Copy the file archive_name_dir/"Packages" to "Packages_extracted".
6. Run ./gen_packages_map.sh > packages_map.py
   See differences and make adjustments to gen_packages_map.sh if needed. Especially, look for the new appeared packages (they will have empty comment) and removed packages. If noticed new/removed packages, then use make_pkgbuild_pkgs_template.sh and edit gen-PKGBUILD.py
7. Run ./gen_replace_deps.sh > replace_deps.py
   See differences and make adjustments to gen_replace_deps.sh if needed.
8. Change version of archive name in extract_transaction_scripts_and_triggers.sh and run it.
Compare transaction_scripts_and_triggers_md5sums.txt file from current and previous driver version. If there are changes, see if it is needed to convert them to pacman .install files or hooks.
9. Create a local repository if not done yet (see remake_all.sh)
10. Regenerate PKGBUILD with remake_all.sh
11. If you notice empty licence, add its hash to the licenses_hashes_map
12. Install from local repository and test it.
13. Update AUR package: copy PKGBUILD, .SRCINFO and other files as needed.
