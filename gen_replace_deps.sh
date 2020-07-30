#!/bin/bash
# This script generates a dependencies map of debian packages to arch linux packages dict for using in gen-PKGBUILD.py

cat Packages-extracted | egrep "Depends|Suggests|Recommends" | sed 's/Depends: //' | sed 's/Suggests: //' | sed 's/Recommends: //'| sed 's/, /\n/g' | sort -u | grep -v "amdgpu" | sed "s/ | /\n/g" > tmp_extra_deps_in_debian.txt
cat tmp_extra_deps_in_debian.txt | cut -f1 -d" " | sort -u > tmp_extra_deps_in_debian_removed_versions.txt # removed versions

# Detecting dependencies, named with amdgpu (and their alternatives), that are not provided in bundled amd archive
cat Packages-extracted | egrep "Depends|Suggests|Recommends" | sed 's/Pre-Depends: //' | sed 's/Depends: //' | sed 's/Suggests: //' | sed 's/Recommends: //'| sed 's/, /\n/g' | sort -u | grep "amdgpu" | sed "s/ | /\n/g" > tmp_deps_in_debian_amdgpu.txt
cat tmp_deps_in_debian_amdgpu.txt | cut -f1 -d" " | sort -u > tmp_removed_versions_amdgpu.txt # removed versions
cat tmp_removed_versions_amdgpu.txt | sed "s/:i386$//g" | sort -u > tmp_amdgpu_deps_in_debian.txt
> tmp_extra_deps_in_debian_amdgpu.txt # clear file
for line in $(cat tmp_amdgpu_deps_in_debian.txt); do
    if grep -q "Package: $line" Packages-extracted; then continue; fi
    echo $line >> tmp_extra_deps_in_debian_amdgpu.txt
done

sed -i 's/-hwe//g' tmp_extra_deps_in_debian_amdgpu.txt


echo > tmp_translated_deps.txt # clear file

for line in $(cat tmp_extra_deps_in_debian_removed_versions.txt tmp_extra_deps_in_debian_amdgpu.txt); do
    echo now processing $line >&2;
    case $line in

        libc6) arch_str="None, #manually_mapped" ;; # It maps to 'glibc', which is required by base, so no need to explicitly depend on it
        libgcc-s1) arch_str="None, #manually_mapped" ;; # It maps to 'gcc', but I doubt it depends on gcc, the compiler
        libgl1) arch_str="'libglvnd', #manually_mapped" ;;
        libjs-jquery) arch_str="'jquery', #manually_mapped" ;;
        libjs-underscore) arch_str="'underscorejs', #manually_mapped" ;;
        libstdc++6) arch_str="None, #manually_mapped" ;; # It maps to 'gcc-libs', which is required by base, so no need to explicitly depend on it
        libtxc-dxtn-s2tc0) arch_str="'libtxc_dxtn', #manually_mapped" ;;
        libtxc-dxtn0) arch_str="None, #manually_mapped" ;; # have alternative libtxc-dxtn-s2tc0
        libtinfo5) arch_str="'ncurses5-compat-libs', #manually_mapped" ;;
        libtinfo-dev) arch_str="'ncurses', #manually_mapped" ;;
        libudev0) arch_str="None, #manually_mapped" ;; # have alternative libudev1
        linux-firmware) arch_str="'linux-firmware', #manually_mapped" ;; # debtap takes very long time and finally faulty auto translates to None.
        xserver-xorg-hwe-18.04) arch_str="None, #manually_disabled" ;;
        #---) arch_str="'---', #manually_mapped" ;; # templpate
        
        *)
            arch_dep=`bash ./translate_deb_to_arch_dependency.sh $line`; # https://github.com/helixarch/debtap/issues/41#issuecomment-489166020
            if [[ $arch_dep == "could_not_translate" ]]; then arch_str="'$line', #could_not_auto_translate";
            elif [[ $arch_dep == "" ]]; then arch_str="None, #auto_translated";
            else arch_str="'$arch_dep', #auto_translated"
            fi
    esac
    str="'$line': "; str="$str $arch_str"; echo $str >> tmp_translated_deps.txt;
done
cat tmp_translated_deps.txt | column -t | sed 's/^'\''/    '\''/' > tmp_prepared_columns.txt 

echo -e "# Generated with ./gen_replace_deps.sh > replace_deps.py\n\
# for driver version `sed -n 2p Packages-extracted | cut -f 2 -d " "`\n"
echo "replace_deps = {"
cat tmp_prepared_columns.txt
echo "}"

rm tmp_amdgpu_deps_in_debian.txt
rm tmp_deps_in_debian_amdgpu.txt
rm tmp_extra_deps_in_debian_amdgpu.txt
rm tmp_extra_deps_in_debian_removed_versions.txt
rm tmp_extra_deps_in_debian.txt
rm tmp_prepared_columns.txt
rm tmp_removed_versions_amdgpu.txt
rm tmp_translated_deps.txt
