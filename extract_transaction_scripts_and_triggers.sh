#!/bin/bash

# This script extracts transaction scripts of deb packages to a file, so it is possible to read it and compare with previous version.
# After that its needed to carefully convert them to pacman .install files or hooks if needed

. ./versions

majornew=$pkgver_base
minornew=$pkgver_build
ubuntuvernew=$ubuntu_ver

majorold=$old_pkgver_base
minorold=$old_pkgver_build
ubuntuverold=$old_ubuntu_ver

function extract_them() {
    major="$1"
    minor="$2"
    
    FOLDER=amdgpu-pro-$major-$minor-ubuntu-20.04
    cd $FOLDER
    cd unpacked_debs
    rm -f *.install_scripts.sh
    rm -rf ../install_scripts_"$major"-"$minor"
    rm -rf ../install_scripts
    mkdir -p ../install_scripts
    > transaction_scripts_and_triggers_md5sums.txt # clear file
    echo -e "md5sums of transaction scripts and triggers of deb packages from archive ${ARCHIVE}\n" > transaction_scripts_and_triggers_md5sums.txt
    for dir in $(ls); do
        for file in postinst preinst prerm; do
            if [ -f $dir/$file ]; then
                file_md5=$(md5sum $dir/$file)
                # echo -e "# $file_md5"  >> $dir.install_scripts.sh
                echo -e "$file_md5"  >> transaction_scripts_and_triggers_md5sums.txt
                #cat $dir/$file >> $dir.install_scripts.sh
                cat $dir/$file > ../install_scripts/"$dir"_"$file".txt
            fi
        done
    done
    cd ..

    # As of 19.30-934563, all (except two) libs debian packages have just ldconfig awaiting trigger. It is done automatically by pacman, so we skip them.
    # Two exceptions are:
        #libgl1-amdgpu-mesa-dri_18.3.0-812932_amd64.deb
        #interest /usr/lib/x86_64-linux-gnu/dri
        #libgl1-amdgpu-mesa-dri_18.3.0-812932_i386.deb
        #interest /usr/lib/i386-linux-gnu/dri
    # They are triggered when files are changed in interest path. I (Ashark) created corresponding alpm hooks.

    cd unpacked_debs
    for dir in $(ls -d *deb);
    do
        if [ -f "$dir"/triggers ]; then
            if [[ $(cat "$dir"/triggers) == "# Triggers added by dh_makeshlibs/11.1.6ubuntu2
    activate-noawait ldconfig" ]];
            then continue; fi
            file_md5=$(md5sum $dir/triggers)
            echo -e "$file_md5" >> transaction_scripts_and_triggers_md5sums.txt
            cat $dir/triggers > ../install_scripts/"$dir"_"triggers".txt
        fi
    done

    sed -i -e "1 ! s/$major/XX.XX/g" -e "1 ! s/$minor/XXXXXX/g" transaction_scripts_and_triggers_md5sums.txt
    cd ..

    rename "$major" "XX.XX" install_scripts/*.txt
    rename "$minor" "XXXXXX" install_scripts/*.txt

    rename "_2.1.0" "_C.C.C" install_scripts/*.txt # new comgr version
    rename "_2.0.0" "_C.C.C" install_scripts/*.txt # old comgr version

    rename "1.2.0" "_H.H.H" install_scripts/*.txt # old hsa-runtime-rocr-amdgpu version
    rename "1.3.0" "_H.H.H" install_scripts/*.txt # new hsa-runtime-rocr-amdgpu version

    rename "21.1.0" "YY.Y.Y" install_scripts/*.txt # new mesa version
    rename "20.3.4" "YY.Y.Y" install_scripts/*.txt # old mesa version

    rename "5.11.19.98" "Y.Y.Y.YY" install_scripts/*.txt # new amdgpu-dkms version
    rename "5.11.5.26" "Y.Y.Y.YY" install_scripts/*.txt # old amdgpu-dkms version

    rename "rocm_13.0" "rocm_RR.R" install_scripts/*.txt # new libllvm-amdgpu-pro-rocm
    rename "rocm_12.0" "rocm_RR.R" install_scripts/*.txt # old libllvm-amdgpu-pro-rocm

    rename "libllvm12.0-amdgpu_12.0" "libllvmZZ.Z-amdgpu_ZZ.Z" install_scripts/*.txt # new llvm-amdgpu version
    rename "libllvm11.0-amdgpu_11.0" "libllvmZZ.Z-amdgpu_ZZ.Z" install_scripts/*.txt # old llvm-amdgpu version
    
    rename "12.0-runtime_12.0" "LL.L-runtime_LL.L" install_scripts/*.txt # new llvm-amdgpu-XX.X-runtime_XX.X
    rename "11.0-runtime_11.0" "LL.L-runtime_LL.L" install_scripts/*.txt # old llvm-amdgpu-XX.X-runtime_XX.X
    
    rename "dev_12.0" "dev_DD.D" install_scripts/*.txt # new llvm-amdgpu-dev_XX.X
    rename "dev_11.0" "dev_DD.D" install_scripts/*.txt # old llvm-amdgpu-dev_XX.X

    mv install_scripts install_scripts_"$major"-"$minor"
    cd ..
}

# Specify the versions to run for (comment one of them if you want to disable running for it).
# extract_them $majorold $minorold # Run for old version
extract_them $majornew $minornew # Run for new version

echo "Opening meld for comparison..."
pwd
meld amdgpu-pro-$majorold-$minorold-ubuntu-$ubuntuverold/install_scripts_"$majorold"-"$minorold" amdgpu-pro-$majornew-$minornew-ubuntu-$ubuntuvernew/install_scripts_"$majornew"-"$minornew"
