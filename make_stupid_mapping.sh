#!/bin/bash

# This script prepares a list of packages mapping for using in gen-PKGBUILD.py

# get list of deb-metapackages:
cat Packages-extracted | grep -vE "Filename|Size|MD5sum|SHA1|SHA256|Priority|Maintainer|Version|Description|^ +" | grep -B4 "Section: metapackages" | grep -vE "Depends:|Section:" > tmp_Packages.txt
echo > deb_metapackages_list

while read line; do
    if [[ $line =~ ^Package* ]]; then pkg=$(echo $line | sed "s/^Package: //"); continue; fi
    if [[ $line =~ ^Architecture* ]]; then
        arch=$(echo $line | sed "s/^Architecture: //")
        if [[ $arch == i386 ]]; then arch=":i386"; else arch=""; fi
        echo "$pkg$arch" >> tmp_deb_metapackages_list.txt; continue;
    fi
done < tmp_Packages.txt
rm tmp_Packages.txt


cat Packages-extracted | grep Package | cut -f2 -d " " > tmp_all_presented_debian_packages.txt
prev=""; for line in $(cat tmp_all_presented_debian_packages.txt); do if [[ $prev != $line ]]; then echo $line; else echo $line:i386; fi; prev=$line; done > tmp_renamed_deb_32bit_packages.txt
echo > tmp_non_hwe_list.txt
if grep amdgpu-hwe tmp_renamed_deb_32bit_packages.txt > /dev/null; then # hwe version presented
    grep hwe tmp_renamed_deb_32bit_packages.txt | sed 's/-hwe//' > tmp_non_hwe_list.txt
fi

shopt -s extglob # needed for expanding syntax in case patterns
for line in $(cat tmp_renamed_deb_32bit_packages.txt); do
    str="    '$line': "; comment="";
    if [[ $line != *"i386" ]]; then archpkg=$line; else archpkg="lib32-${line//:i386/}"; fi;
    ##if [[ $archpkg == *"-dev" ]]; then archpkg=${archpkg//-dev/}; fi; # disable for now, I will combine packages later, but now I will make 1:1 conversion

    if grep -Fx $line tmp_non_hwe_list.txt > /dev/null; then archpkg=None; comment="disabled_because_hwe_version_is_available"; fi;

    if [[ $archpkg == *"-hwe"* ]]; then archpkg=${archpkg//-hwe/}; fi;
 
    if grep $line tmp_deb_metapackages_list.txt > /dev/null && [[ $archpkg != None ]]; then archpkg="$archpkg-meta"; fi;
            case $line in
         amdgpu@(-dkms||:i386|-hwe|-hwe:i386|-lib32)\
        |amdgpu-lib@(|:i386|-hwe|-hwe:i386)\
        |gst-omx-amdgpu@(|:i386)\
        |libegl1-amdgpu-mesa@(|:i386|-dev|-dev:i386)\
        |libegl1-amdgpu-mesa-drivers@(|:i386)\
        |libgbm-amdgpu-dev@(|:i386)\
        |libgbm1-amdgpu@(|:i386)\
        |libgl1-amdgpu-mesa@(-dev|-dev:i386|-dri|-dri:i386|-glx|-glx:i386)\
        |libglapi-amdgpu-mesa@(|:i386)\
        |libgles1-amdgpu-mesa@(|:i386|-dev|-dev:i386)\
        |libgles2-amdgpu-mesa@(|:i386|-dev|-dev:i386)\
        |libllvm7.1-amdgpu@(|:i386)\
        |libosmesa6-amdgpu@(|:i386|-dev|-dev:i386)\
        |libwayland-amdgpu-egl1@(|:i386)\
        |libxatracker2-amdgpu@(|:i386)\
        |mesa-amdgpu-omx-drivers@(|:i386)\
        |mesa-amdgpu-va-drivers@(|:i386)\
        |mesa-amdgpu-vdpau-drivers@(|:i386)\
        |xserver-xorg-amdgpu-video-amdgpu@(|:i386)\
        |xserver-xorg-hwe-amdgpu-video-amdgpu@(|:i386)\
        |vulkan-amdgpu@(|:i386)\
        )
            archpkg=None; comment="unneeded_open_component"
            ;;
        "amdgpu-pro-pin")
            archpkg=None; comment="debian_specific_package,_not_needed"
            ;;
        "amdgpu-doc")
            archpkg=None; comment="arch_specific_instructions_will_be_covered_in_archwiki"
            ;;
    esac
    if [[ $archpkg == "None" ]]; then str="$str $archpkg, #$comment"; else str="$str '$archpkg',"; fi
    echo -e "$str";
done | column -t | sed 's/^/    /'
rm tmp_deb_metapackages_list.txt
rm tmp_non_hwe_list.txt
rm tmp_all_presented_debian_packages.txt
rm tmp_renamed_deb_32bit_packages.txt
#Then it's needed to carefully check pkgs mapping
