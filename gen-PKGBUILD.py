from debian import deb822
from debian import debfile
import re
import gzip
import lzma
import tarfile
import subprocess
import hashlib
import glob
from pathlib import Path

pkgver_base = "19.10"
pkgver_build = "785425"
pkgrel = 1

debugging = False

debug_pkgext = True #if debugging else False

url_ref = "https://www.amd.com/en/support/kb/release-notes/rn-rad-lin-19-10-unified"
dlagents = "https::/usr/bin/wget --referer {0} -N %u".format(url_ref)

source_url = "https://drivers.amd.com/drivers/linux/amdgpu-pro-${major}-${minor}-ubuntu-18.04.tar.xz"
source_url_resolved = "https://drivers.amd.com/drivers/linux/amdgpu-pro-{0}-{1}-ubuntu-18.04.tar.xz".format(pkgver_base, pkgver_build)
source_file = "amdgpu-pro-{0}-{1}-ubuntu-18.04.tar.xz".format(pkgver_base, pkgver_build)

def gen_arch_packages():
    pkgbuild_packages = {
        #'amdgpu-pro': Package(
            #desc = "The AMDGPU Pro driver package",
            #install = "amdgpu-pro-core.install",
            #extra_commands = [
                #"mv \"${pkgdir}\"/usr/lib/x86_64-linux-gnu/dri ${pkgdir}/usr/lib/",
                #"# This is needed because libglx.so has a hardcoded DRI_DRIVER_PATH",
                #"ln -s /usr/lib/dri ${pkgdir}/usr/lib/x86_64-linux-gnu/dri",
                #'mkdir -p "${pkgdir}/etc/ld.so.conf.d/"',
                #'echo "/opt/amdgpu-pro/lib/x86_64-linux-gnu/" > "${pkgdir}"/etc/ld.so.conf.d/amdgpu-pro.conf',
            #]
        #),

        #'amdgpu-pro-dkms': Package(
            #arch = ['any'],
            #descr = "The AMDGPU Pro kernel module",
            #extra_commands = [
                #"msg 'Applying patches...'",
                #"(cd ${pkgdir}/usr/src/amdgpu-${major}-${minor};",
                #"\tsed -i 's/\/extra/\/extramodules/' dkms.conf",
                #";\n".join(["\t\tmsg2 '{0}'\n\t\tpatch -p1 -i \"${{srcdir}}/{0}\"".format(patch) for patch in patches]),
                #")",
                #]
        #),

        #'amdgpu-pro-libgl': Package(
            #desc = "The AMDGPU Pro libgl library symlinks",
            #conflicts = ['libgl'],
            #provides  = ['libgl'],
        #),

        #'amdgpu-pro-opencl': Package(
            #desc = "The AMDGPU Pro OpenCL implementation",
            #provides  = ['opencl-driver']
        #),
        #'amdgpu-pro-libdrm': Package(
            #desc = "The AMDGPU Pro userspace interface to kernel DRM services",
            #conflicts = ['libdrm'],
            #provides = ['libdrm'],
        #),

        #'amdgpu-pro-vulkan': Package(
            #desc = "The AMDGPU Pro Vulkan driver",
            #provides = ['vulkan-driver'],
            #extra_commands = [
                #'mkdir -p "${pkgdir}"/usr/share/vulkan/icd.d/',
                #'mv "${pkgdir}"/etc/vulkan/icd.d/amd_icd64.json "${pkgdir}"/usr/share/vulkan/icd.d/',
                ## https://support.amd.com/en-us/kb-articles/Pages/AMDGPU-PRO-Driver-for-Linux-Release-Notes.aspx
                ## says you need version 1.0.61 of the vulkan sdk, so I'm guessing this is the correct version supported by this driver
                #'sed -i "s@abi_versions\(.*\)0.9.0\(.*\)@api_version\\11.0.61\\2@" "${pkgdir}"/usr/share/vulkan/icd.d/amd_icd64.json',
                #'rm -rf "${pkgdir}"/etc/vulkan/'
            #]
        #),

        #'amdgpu-pro-vdpau': Package(
            #desc = "The AMDGPU Pro VDPAU driver",
            #extra_commands = [
                #'mkdir -p "${pkgdir}"/usr/lib/',
                #'ln -s /opt/amdgpu-pro/lib/x86_64-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib/libvdpau_amdgpu.so.1.0.0',
                #'ln -s /opt/amdgpu-pro/lib/x86_64-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib/libvdpau_amdgpu.so.1',
                #'ln -s /opt/amdgpu-pro/lib/x86_64-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib/libvdpau_amdgpu.so',
            #]
        #),

        #'amdgpu-pro-mesa-omx': Package(
            #desc = "Mesa OpenMAX video drivers for AMDGPU Pro",
        #),

        #'amdgpu-pro-gst-omx': Package(
            #desc = "GStreamer OpenMAX plugins for AMDGPU Pro",
        #),

        #'lib32-amdgpu-pro': Package(
            #desc = "The AMDGPU Pro driver package (32bit libraries)",
            #extra_commands = [
                #'mkdir -p "${pkgdir}"/usr/lib32/',
                #'mv "${pkgdir}"/usr/lib/i386-linux-gnu/dri "${pkgdir}"/usr/lib32/',

                #'rm -rf "${pkgdir}"/etc',
                #'mkdir -p "${pkgdir}/etc/ld.so.conf.d/"',
                #'echo "/opt/amdgpu-pro/lib/i386-linux-gnu/" > "${pkgdir}"/etc/ld.so.conf.d/lib32-amdgpu-pro.conf'
            #]
        #),

        #'lib32-amdgpu-pro-opencl': Package(
            #desc = "The AMDGPU Pro OpenCL implementation",
            #provides  = ['lib32-opencl-driver']
        #),

        #'lib32-amdgpu-pro-vulkan': Package(
            #desc = "The AMDGPU Pro Vulkan driver (32bit libraries)",
            #provides = ['lib32-vulkan-driver'],
            #extra_commands = [
                #'mkdir -p "${pkgdir}"/usr/share/vulkan/icd.d/',
                #'mv "${pkgdir}"/etc/vulkan/icd.d/amd_icd32.json "${pkgdir}"/usr/share/vulkan/icd.d/',
                ## https://support.amd.com/en-us/kb-articles/Pages/AMDGPU-PRO-Driver-for-Linux-Release-Notes.aspx
                ## says you need version 1.0.61 of the vulkan sdk, so I'm guessing this is the correct version supported by this driver
                #'sed -i "s@abi_versions\(.*\)0.9.0\(.*\)@api_version\\11.0.61\\2@" "${pkgdir}"/usr/share/vulkan/icd.d/amd_icd32.json',
                #'rm -rf "${pkgdir}"/etc/vulkan/'
            #]
        #),

        #'lib32-amdgpu-pro-libdrm': Package(
            #desc = "The AMDGPU Pro userspace interface to kernel DRM services (32bit libraries)",
            #conflicts = ['lib32-libdrm'],
            #provides = ['lib32-libdrm'],
        #),

        #'lib32-amdgpu-pro-libgl': Package(
            #desc = "The AMDGPU Pro libgl library symlinks (32bit libraries)",
            #conflicts = ['lib32-libgl'],
            #provides  = ['lib32-libgl'],
            #extra_commands = [
                #'rm -rf "${pkgdir}"/etc',
            #]
        #),

        #'lib32-amdgpu-pro-vdpau': Package(
            #desc = "The AMDGPU Pro VDPAU driver (32bit libraries)",
            #extra_commands = [
                #'mkdir -p "${pkgdir}"/usr/lib32/',
                #'ln -s /opt/amdgpu-pro/lib/i386-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib32/libvdpau_amdgpu.so.1.0.0',
                #'ln -s /opt/amdgpu-pro/lib/i386-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib32/libvdpau_amdgpu.so.1',
                #'ln -s /opt/amdgpu-pro/lib/i386-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib32/libvdpau_amdgpu.so',
            #]
        #),

        #'lib32-amdgpu-pro-mesa-omx': Package(
            #desc = "Mesa OpenMAX video drivers for AMDGPU Pro (32bit libraries)",
            #extra_commands = [
                #'rm -f "${pkgdir}"/etc/xdg/gstomx.conf'
            #]
        #),

        #'lib32-amdgpu-pro-gst-omx': Package(
            #desc = "GStreamer OpenMAX plugins for AMDGPU Pro (32bit libraries)",
        #),

        #'xf86-video-amdgpu-pro': Package(
            #desc = "The AMDGPU Pro X.org video driver",
            #conflicts = ['xf86-video-amdgpu', 'xorg-server<1.19.0', 'X-ABI-VIDEODRV_VERSION<23', 'X-ABI-VIDEODRV_VERSION>=24'],
            #provides  = ['xf86-video-amdgpu'], # in case anything depends on that
            #groups = ['xorg-drivers'],
        #)

        # Further is made by me (Ashark)
        # To make a more human readable Packages file I used this:
        # cat Packages | grep -vE "Filename|Size|MD5sum|SHA1|SHA256|Priority|Maintainer|Version: 19.10-785425" >  Packages-short

        ## To generate this I used:
            #cat list_tmp3 | cut -f4 -d"'" > list_tmp4
            #echo "" > already_used.txt
            #for line in $(cat list_tmp4); do
                #if grep -Fxq "$line" already_used.txt; then continue;
                #else
                    #echo $line >> already_used.txt
                    #echo -e "        '$line': Package(  ),";
                #fi
            #done
            #rm already_used.txt

        # To show packages with their conffiles I used this:
        #for file in $(ls *deb);
        #do
            #tmpdir=tmpdir; rm -rf "$tmpdir"; mkdir "$tmpdir"; cd "$tmpdir"
            #ar x ../$file control.tar.xz
            #files=$(tar -tf control.tar.xz | grep -vE "control|md5sums|./$" | grep conffiles)
            #if [[ $files != "" ]]; then
                #echo -e "$file:\n           backup = ["
                #tar -xf control.tar.xz ./conffiles -O | sed 's/^\//              '\''/' | sed 's/$/'\'',/'
                #echo "           ],"
            #fi
            #files=""; cd ..
        #done
        #rm -rf tmpdir
        # They are added automatically, but you can override a backup array as shown in the example:

        # 'overriding-example': Package(
        #     desc = "This overrides original description",
        #     version = "555",
        #     license = "lic_name",
        #     arch = ["x86_64"],
        #     provides = ["one", "two"],
        #     conflicts = ["one", "two"],
        #     optdepends = ["one", "two"],
        #     install = "random_filename.install",
        #     backup = [ 'file/one', 'file/two'],
        #     depends = ["one", "two"],
        #     extra_commands = [
        #         "do_one",
        #         "do_two",
        #     ],
        # ),

        'amdgpu-core-meta': Package(  ),
        'amdgpu-dkms': Package(  ),
        'amdgpu-doc': Package(  ),
        'amdgpu-meta': Package(  ),
        'lib32-amdgpu-meta': Package(  ),
        'amdgpu-lib-meta': Package(  ),
        'lib32-amdgpu-lib-meta': Package(  ),
        'amdgpu-lib32-meta': Package(  ),
        'amdgpu-pro-core-meta': Package(  ),
        'amdgpu-pro-meta': Package(  ),
        'lib32-amdgpu-pro-meta': Package(  ),
        'amdgpu-pro-lib32-meta': Package(  ),
        'amf-amdgpu-pro': Package(  ),
        'clinfo-amdgpu-pro': Package(  ),
        'lib32-clinfo-amdgpu-pro': Package(  ),
        'glamor-amdgpu': Package(  ),
        'lib32-glamor-amdgpu': Package(  ),
        'gst-omx-amdgpu': Package(  ),
        'lib32-gst-omx-amdgpu': Package(  ),
        'libdrm-amdgpu-amdgpu1': Package(  ),
        'lib32-libdrm-amdgpu-amdgpu1': Package(  ),
        'libdrm-amdgpu-common': Package(  ),
        'libdrm-amdgpu': Package(  ),
        'lib32-libdrm-amdgpu': Package(  ),
        'libdrm-amdgpu-radeon1': Package(  ),
        'lib32-libdrm-amdgpu-radeon1': Package(  ),
        'libdrm-amdgpu-utils': Package(  ),
        'lib32-libdrm-amdgpu-utils': Package(  ),
        'libdrm2-amdgpu': Package(
            extra_commands = [
                "mv ${pkgdir}/lib/* ${pkgdir}/usr/lib",
                "rmdir ${pkgdir}/lib\n"
            ],
        ),
        'lib32-libdrm2-amdgpu': Package(
            extra_commands = [
                "mv ${pkgdir}/lib ${pkgdir}/usr\n"
            ],
        ),
        'libegl1-amdgpu-mesa': Package(  ),
        'lib32-libegl1-amdgpu-mesa': Package(  ),
        'libegl1-amdgpu-mesa-drivers': Package(  ),
        'lib32-libegl1-amdgpu-mesa-drivers': Package(  ),
        'libegl1-amdgpu-pro': Package(  ),
        'lib32-libegl1-amdgpu-pro': Package(  ),
        'libgbm-amdgpu': Package(  ),
        'lib32-libgbm-amdgpu': Package(  ),
        'libgbm1-amdgpu': Package(  ),
        'lib32-libgbm1-amdgpu': Package(  ),
        'libgbm1-amdgpu-pro': Package(  ),
        'lib32-libgbm1-amdgpu-pro': Package(  ),
        'libgbm1-amdgpu-pro-base': Package(  ),
        'libgl1-amdgpu-mesa': Package(  ),
        'lib32-libgl1-amdgpu-mesa': Package(  ),
        'libgl1-amdgpu-mesa-dri': Package(  ),
        'lib32-libgl1-amdgpu-mesa-dri': Package(  ),
        'libgl1-amdgpu-mesa-glx': Package(  ),
        'lib32-libgl1-amdgpu-mesa-glx': Package(  ),
        'libgl1-amdgpu-pro-appprofiles': Package(  ),
        'libgl1-amdgpu-pro-dri': Package(  ),
        'lib32-libgl1-amdgpu-pro-dri': Package(  ),
        'libgl1-amdgpu-pro-ext': Package(  ),
        'lib32-libgl1-amdgpu-pro-ext': Package(  ),
        'libgl1-amdgpu-pro-glx': Package(  ),
        'lib32-libgl1-amdgpu-pro-glx': Package(  ),
        'libglapi-amdgpu-mesa': Package(  ),
        'lib32-libglapi-amdgpu-mesa': Package(  ),
        'libglapi1-amdgpu-pro': Package(  ),
        'lib32-libglapi1-amdgpu-pro': Package(  ),
        'libgles1-amdgpu-mesa': Package(  ),
        'lib32-libgles1-amdgpu-mesa': Package(  ),
        'libgles2-amdgpu-mesa': Package(  ),
        'lib32-libgles2-amdgpu-mesa': Package(  ),
        'libgles2-amdgpu-pro': Package(  ),
        'lib32-libgles2-amdgpu-pro': Package(  ),
        'libllvm7.1-amdgpu': Package(  ),
        'lib32-libllvm7.1-amdgpu': Package(  ),
        'libopencl1-amdgpu-pro': Package(  ),
        'lib32-libopencl1-amdgpu-pro': Package(  ),
        'libosmesa6-amdgpu': Package(  ),
        'lib32-libosmesa6-amdgpu': Package(  ),
        'libwayland-amdgpu-client0': Package(  ),
        'lib32-libwayland-amdgpu-client0': Package(  ),
        'libwayland-amdgpu-cursor0': Package(  ),
        'lib32-libwayland-amdgpu-cursor0': Package(  ),
        'libwayland-amdgpu': Package(  ),
        'lib32-libwayland-amdgpu': Package(  ),
        'libwayland-amdgpu-doc': Package(  ),
        'libwayland-amdgpu-egl1': Package(  ),
        'lib32-libwayland-amdgpu-egl1': Package(  ),
        'libwayland-amdgpu-server0': Package(  ),
        'lib32-libwayland-amdgpu-server0': Package(  ),
        'libxatracker-amdgpu': Package(  ),
        'lib32-libxatracker-amdgpu': Package(  ),
        'libxatracker2-amdgpu': Package(  ),
        'lib32-libxatracker2-amdgpu': Package(  ),
        'llvm-amdgpu': Package(  ),
        'lib32-llvm-amdgpu': Package(  ),
        'llvm-amdgpu-7.1': Package(  ),
        'lib32-llvm-amdgpu-7.1': Package(  ),
        'llvm-amdgpu-7.1-doc': Package(  ),
        'llvm-amdgpu-7.1-runtime': Package(  ),
        'lib32-llvm-amdgpu-7.1-runtime': Package(  ),
        'llvm-amdgpu-runtime': Package(  ),
        'lib32-llvm-amdgpu-runtime': Package(  ),
        'mesa-amdgpu-common': Package(  ),
        'lib32-mesa-amdgpu-common': Package(  ),
        'mesa-amdgpu-omx-drivers': Package(  ),
        'lib32-mesa-amdgpu-omx-drivers': Package(  ),
        'mesa-amdgpu-va-drivers': Package(  ),
        'lib32-mesa-amdgpu-va-drivers': Package(  ),
        'mesa-amdgpu-vdpau-drivers': Package(  ),
        'lib32-mesa-amdgpu-vdpau-drivers': Package(  ),
        'opencl-amdgpu-pro-meta': Package(  ),
        'opencl-amdgpu-pro': Package(  ),
        'opencl-amdgpu-pro-icd': Package(  ),
        'opencl-orca-amdgpu-pro-icd': Package(  ),
        'lib32-opencl-orca-amdgpu-pro-icd': Package(  ),
        'roct-amdgpu-pro': Package(  ),
        'vulkan-amdgpu': Package(  ),
        'lib32-vulkan-amdgpu': Package(  ),
        'vulkan-amdgpu-pro': Package(  ),
        'lib32-vulkan-amdgpu-pro': Package(  ),
        'wayland-protocols-amdgpu': Package(  ),
        'wsa-amdgpu': Package(  ),
        'lib32-wsa-amdgpu': Package(  ),
        'xserver-xorg-amdgpu-video-amdgpu': Package(  ),
        'lib32-xserver-xorg-amdgpu-video-amdgpu': Package(  ),

        # Not yet checked manually, and not yet checked for preinst/postinst/etc files
    }
    for key in pkgbuild_packages:
        pkgbuild_packages[key].arch_pkg_name = key
    return pkgbuild_packages


# this maps which deb packages should go into specific arch package
packages_map = {
    #'amdgpu-pro':                       'amdgpu-pro',        # deb is metapackage
    #'amdgpu-pro-core':                  'amdgpu-pro',        # deb is metapackage
    #'libgbm1-amdgpu-pro':               'amdgpu-pro',
    #'libgbm1-amdgpu-pro-base':          'amdgpu-pro',
    #'libgbm1-amdgpu-pro-dev':           'amdgpu-pro',
    #'ids-amdgpu-pro':                   'amdgpu-pro',

    #'libllvm5.0-amdgpu-pro':            'amdgpu-pro',
    #'llvm-amdgpu-pro-5.0-dev':          'amdgpu-pro',
    #'llvm-amdgpu-pro-5.0':              'amdgpu-pro',
    #'llvm-amdgpu-pro-5.0-runtime':      'amdgpu-pro',
    #'llvm-amdgpu-pro-runtime':          'amdgpu-pro',
    #'llvm-amdgpu-pro-dev':              'amdgpu-pro',

    #'gst-omx-amdgpu-pro':               'amdgpu-pro-gst-omx',
    #'mesa-amdgpu-pro-omx-drivers':      'amdgpu-pro-mesa-omx',

    #'amdgpu-pro-dkms':                  'amdgpu-pro-dkms',

    #'clinfo-amdgpu-pro':                'amdgpu-pro-opencl',
    #'libopencl1-amdgpu-pro':            'amdgpu-pro-opencl',
    #'opencl-amdgpu-pro-icd':            'amdgpu-pro-opencl',
    #'rocm-amdgpu-pro':                  'amdgpu-pro-opencl',
    #'rocm-amdgpu-pro-icd':              'amdgpu-pro-opencl',
    #'rocm-amdgpu-pro-opencl':           'amdgpu-pro-opencl',
    #'rocm-amdgpu-pro-opencl-dev':       'amdgpu-pro-opencl',
    #'rocr-amdgpu-pro':                  'amdgpu-pro-opencl',
    #'rocr-amdgpu-pro-dev':              'amdgpu-pro-opencl',
    #'roct-amdgpu-pro':                  'amdgpu-pro-opencl',
    #'roct-amdgpu-pro-dev':              'amdgpu-pro-opencl',
    #'hsa-runtime-tools-amdgpu-pro':     'amdgpu-pro-opencl',
    #'hsa-runtime-tools-amdgpu-pro-dev': 'amdgpu-pro-opencl',
    #'hsa-ext-amdgpu-pro-finalize':      'amdgpu-pro-opencl',
    #'hsa-ext-amdgpu-pro-image':         'amdgpu-pro-opencl',

    #'vulkan-amdgpu-pro':                'amdgpu-pro-vulkan',

    #'libdrm-amdgpu-pro-amdgpu1':        'amdgpu-pro-libdrm',
    #'libdrm-amdgpu-pro-radeon1':        'amdgpu-pro-libdrm',
    #'libdrm-amdgpu-pro-dev':            'amdgpu-pro-libdrm',
    #'libdrm-amdgpu-pro-utils':          'amdgpu-pro-libdrm',
    #'libdrm2-amdgpu-pro':               'amdgpu-pro-libdrm',

    ## the following libs will be symlinked by amdgpu-pro-libgl, just like mesa-libgl and nvidia-libgl
    #'libegl1-amdgpu-pro':               'amdgpu-pro-libgl',
    #'libgl1-amdgpu-pro-appprofiles':    'amdgpu-pro-libgl',
    ### contents of this should probably go into /usr/lib/xorg/modules/dri/ instead of /usr/lib/dri ?
    #'libgl1-amdgpu-pro-dri':            'amdgpu-pro',
    #'libgl1-amdgpu-pro-ext':            'amdgpu-pro-libgl',
    #'libgl1-amdgpu-pro-glx':            'amdgpu-pro-libgl',
    #'libgles2-amdgpu-pro':              'amdgpu-pro-libgl',
    #'libglamor-amdgpu-pro-dev':         None, # disabled

    #'libvdpau-amdgpu-pro':              'amdgpu-pro-vdpau',
    #'xserver-xorg-video-amdgpu-pro':    'xf86-video-amdgpu-pro',
    #'xserver-xorg-video-glamoregl-amdgpu-pro':    None,
    #'xserver-xorg-video-modesetting-amdgpu-pro':    'xf86-video-amdgpu-pro',


    #'lib32-amdgpu-pro':                 'lib32-amdgpu-pro', # deb is a metapackage
    #'lib32-amdgpu-pro-lib32':           'lib32-amdgpu-pro', # deb is a metapackage
    #'lib32-libgbm1-amdgpu-pro':         'lib32-amdgpu-pro',
    #'lib32-libgbm1-amdgpu-pro-dev':     'lib32-amdgpu-pro',

    #'lib32-gst-omx-amdgpu-pro':         'lib32-amdgpu-pro-gst-omx',
    #'lib32-mesa-amdgpu-pro-omx-drivers':'lib32-amdgpu-pro-mesa-omx',

    #'lib32-opencl-amdgpu-pro-icd':      'lib32-amdgpu-pro-opencl',
    #'lib32-libopencl1-amdgpu-pro':      'lib32-amdgpu-pro-opencl',
    #'lib32-rocm-amdgpu-pro':            'lib32-amdgpu-pro-opencl',
    #'lib32-rocm-amdgpu-pro-icd':        'lib32-amdgpu-pro-opencl',
    #'lib32-rocm-amdgpu-pro-opencl':     'lib32-amdgpu-pro-opencl',
    #'lib32-rocm-amdgpu-pro-opencl-dev': 'lib32-amdgpu-pro-opencl',
    #'lib32-rocr-amdgpu-pro':            'lib32-amdgpu-pro-opencl',
    #'lib32-rocr-amdgpu-pro-dev':        'lib32-amdgpu-pro-opencl',
    #'lib32-roct-amdgpu-pro':            'lib32-amdgpu-pro-opencl',
    #'lib32-roct-amdgpu-pro-dev':        'lib32-amdgpu-pro-opencl',

    #'lib32-vulkan-amdgpu-pro':          'lib32-amdgpu-pro-vulkan',

    #'lib32-libdrm-amdgpu-pro-amdgpu1':  'lib32-amdgpu-pro-libdrm',
    #'lib32-libdrm-amdgpu-pro-radeon1':  'lib32-amdgpu-pro-libdrm',
    #'lib32-libdrm-amdgpu-pro-dev':      'lib32-amdgpu-pro-libdrm',
    #'lib32-libdrm2-amdgpu-pro':         'lib32-amdgpu-pro-libdrm',


    #'lib32-libegl1-amdgpu-pro':         'lib32-amdgpu-pro-libgl',
    #'lib32-libgl1-amdgpu-pro-dri':      'lib32-amdgpu-pro',
    #'lib32-libgl1-amdgpu-pro-ext':      'lib32-amdgpu-pro-libgl',
    #'lib32-libgl1-amdgpu-pro-glx':      'lib32-amdgpu-pro-libgl',
    #'lib32-libgles2-amdgpu-pro':        'lib32-amdgpu-pro-libgl',
    #'lib32-libglamor-amdgpu-pro-dev':   None,

    #'lib32-libvdpau-amdgpu-pro':        'lib32-amdgpu-pro-vdpau',

    ## the following are not needed and should be discarded:
    #'lib32-xserver-xorg-video-amdgpu-pro':              None,
    #'lib32-xserver-xorg-video-glamoregl-amdgpu-pro':    None,
    #'lib32-xserver-xorg-video-modesetting-amdgpu-pro':  None,
    #'lib32-clinfo-amdgpu-pro': None,
    #'lib32-libdrm-amdgpu-pro-utils': None,
    
    ## Further is made by me (Ashark)
    ## get list of deb-metapackages:
    #cat Packages | grep -vE "Filename|Size|MD5sum|SHA1|SHA256|Priority|Maintainer|Version: 19.10-785425|Description|^ +" | grep -B4 "Section: metapackages" | grep -vE "Depends:|Section:" > list_tmp
    #echo > deb_metapackages_list

    #while read line; do
        #if [[ $line =~ ^Package* ]]; then pkg=$(echo $line | sed "s/^Package: //"); continue; fi
        #if [[ $line =~ ^Architecture* ]]; then
            #arch=$(echo $line | sed "s/^Architecture: //")
            #if [[ $arch == i386 ]]; then arch=":i386"; else arch=""; fi
            #echo "$pkg$arch" >> deb_metapackages_list;continue;
        #fi
    #done < list_tmp

    ##To make this list I used:
    #cat Packages | grep Package | cut -f2 -d " " > list_tmp # all presented debian packages
    #prev=""; for line in $(cat list_tmp); do if [[ $prev != $line ]]; then echo $line; else echo $line:i386; fi; prev=$line; done > list_tmp2 # rename 32bit debian packages
    #echo > non_hwe_list
    #if grep amdgpu-hwe list_tmp2 > /dev/null; then # hwe version presented
        #grep hwe list_tmp2 | sed 's/-hwe//' > non_hwe_list
    #fi
    #for line in $(cat list_tmp2); do
        #str="    '$line': "; comment="";
        #if [[ $line != *"i386" ]]; then archpkg=$line; else archpkg="lib32-${line//:i386/}"; fi;
        #if [[ $archpkg == *"-dev" ]]; then archpkg=${archpkg//-dev/}; fi;
        #if [[ $line == "amdgpu-pro-pin" ]]; then archpkg=None; comment="debian_specific_package,_not_needed"; fi;
        #if grep -Fx $line non_hwe_list > /dev/null; then archpkg=None; comment="disabled_because_hwe_version_is_available"; fi;
        #if [[ $archpkg == *"-hwe"* ]]; then archpkg=${archpkg//-hwe/}; fi;
        #if grep $line deb_metapackages_list > /dev/null && [[ $archpkg != None ]]; then archpkg="$archpkg-meta"; fi;
        #if [[ $archpkg == "None" ]]; then str="$str $archpkg, #$comment"; else str="$str '$archpkg',"; fi
        #echo -e "$str";
    #done | column -t | sed 's/^/    /' > list_tmp3 # stupid mapping
    ##Then it's needed to carefully check pkgs mapping manually.

    'amdgpu':                                     None,                                      #disabled_because_hwe_version_is_available
    'amdgpu:i386':                                None,                                      #disabled_because_hwe_version_is_available
    'amdgpu-core':                                'amdgpu-core-meta',                        
    'amdgpu-dkms':                                'amdgpu-dkms',                             
    'amdgpu-doc':                                 'amdgpu-doc',                              
    'amdgpu-hwe':                                 'amdgpu-meta',                             
    'amdgpu-hwe:i386':                            'lib32-amdgpu-meta',                       
    'amdgpu-lib':                                 None,                                      #disabled_because_hwe_version_is_available
    'amdgpu-lib:i386':                            None,                                      #disabled_because_hwe_version_is_available
    'amdgpu-lib-hwe':                             'amdgpu-lib-meta',                         
    'amdgpu-lib-hwe:i386':                        'lib32-amdgpu-lib-meta',                   
    'amdgpu-lib32':                               'amdgpu-lib32-meta',                       
    'amdgpu-pro':                                 None,                                      #disabled_because_hwe_version_is_available
    'amdgpu-pro:i386':                            None,                                      #disabled_because_hwe_version_is_available
    'amdgpu-pro-core':                            'amdgpu-pro-core-meta',                    
    'amdgpu-pro-hwe':                             'amdgpu-pro-meta',                         
    'amdgpu-pro-hwe:i386':                        'lib32-amdgpu-pro-meta',                   
    'amdgpu-pro-lib32':                           'amdgpu-pro-lib32-meta',                   
    'amdgpu-pro-pin':                             None,                                      #debian_specific_package,_not_needed
    'amf-amdgpu-pro':                             'amf-amdgpu-pro',                          
    'clinfo-amdgpu-pro':                          'clinfo-amdgpu-pro',                       
    'clinfo-amdgpu-pro:i386':                     'lib32-clinfo-amdgpu-pro',                 
    'glamor-amdgpu':                              'glamor-amdgpu',                           
    'glamor-amdgpu:i386':                         'lib32-glamor-amdgpu',                     
    'glamor-amdgpu-dev':                          'glamor-amdgpu',                           
    'glamor-amdgpu-dev:i386':                     'lib32-glamor-amdgpu',                     
    'gst-omx-amdgpu':                             'gst-omx-amdgpu',                          
    'gst-omx-amdgpu:i386':                        'lib32-gst-omx-amdgpu',                    
    'libdrm-amdgpu-amdgpu1':                      'libdrm-amdgpu-amdgpu1',                   
    'libdrm-amdgpu-amdgpu1:i386':                 'lib32-libdrm-amdgpu-amdgpu1',             
    'libdrm-amdgpu-common':                       'libdrm-amdgpu-common',                    
    'libdrm-amdgpu-dev':                          'libdrm-amdgpu',                           
    'libdrm-amdgpu-dev:i386':                     'lib32-libdrm-amdgpu',                     
    'libdrm-amdgpu-radeon1':                      'libdrm-amdgpu-radeon1',                   
    'libdrm-amdgpu-radeon1:i386':                 'lib32-libdrm-amdgpu-radeon1',             
    'libdrm-amdgpu-utils':                        'libdrm-amdgpu-utils',                     
    'libdrm-amdgpu-utils:i386':                   'lib32-libdrm-amdgpu-utils',               
    'libdrm2-amdgpu':                             'libdrm2-amdgpu',                          
    'libdrm2-amdgpu:i386':                        'lib32-libdrm2-amdgpu',                    
    'libegl1-amdgpu-mesa':                        'libegl1-amdgpu-mesa',                     
    'libegl1-amdgpu-mesa:i386':                   'lib32-libegl1-amdgpu-mesa',               
    'libegl1-amdgpu-mesa-dev':                    'libegl1-amdgpu-mesa',                     
    'libegl1-amdgpu-mesa-dev:i386':               'lib32-libegl1-amdgpu-mesa',               
    'libegl1-amdgpu-mesa-drivers':                'libegl1-amdgpu-mesa-drivers',             
    'libegl1-amdgpu-mesa-drivers:i386':           'lib32-libegl1-amdgpu-mesa-drivers',       
    'libegl1-amdgpu-pro':                         'libegl1-amdgpu-pro',                      
    'libegl1-amdgpu-pro:i386':                    'lib32-libegl1-amdgpu-pro',                
    'libgbm-amdgpu-dev':                          'libgbm-amdgpu',                           
    'libgbm-amdgpu-dev:i386':                     'lib32-libgbm-amdgpu',                     
    'libgbm1-amdgpu':                             'libgbm1-amdgpu',                          
    'libgbm1-amdgpu:i386':                        'lib32-libgbm1-amdgpu',                    
    'libgbm1-amdgpu-pro':                         'libgbm1-amdgpu-pro',                      
    'libgbm1-amdgpu-pro:i386':                    'lib32-libgbm1-amdgpu-pro',                
    'libgbm1-amdgpu-pro-base':                    'libgbm1-amdgpu-pro-base',                 
    'libgbm1-amdgpu-pro-dev':                     'libgbm1-amdgpu-pro',                      
    'libgbm1-amdgpu-pro-dev:i386':                'lib32-libgbm1-amdgpu-pro',                
    'libgl1-amdgpu-mesa-dev':                     'libgl1-amdgpu-mesa',                      
    'libgl1-amdgpu-mesa-dev:i386':                'lib32-libgl1-amdgpu-mesa',                
    'libgl1-amdgpu-mesa-dri':                     'libgl1-amdgpu-mesa-dri',                  
    'libgl1-amdgpu-mesa-dri:i386':                'lib32-libgl1-amdgpu-mesa-dri',            
    'libgl1-amdgpu-mesa-glx':                     'libgl1-amdgpu-mesa-glx',                  
    'libgl1-amdgpu-mesa-glx:i386':                'lib32-libgl1-amdgpu-mesa-glx',            
    'libgl1-amdgpu-pro-appprofiles':              'libgl1-amdgpu-pro-appprofiles',           
    'libgl1-amdgpu-pro-dri':                      'libgl1-amdgpu-pro-dri',                   
    'libgl1-amdgpu-pro-dri:i386':                 'lib32-libgl1-amdgpu-pro-dri',             
    'libgl1-amdgpu-pro-ext':                      None,                                      #disabled_because_hwe_version_is_available
    'libgl1-amdgpu-pro-ext:i386':                 None,                                      #disabled_because_hwe_version_is_available
    'libgl1-amdgpu-pro-ext-hwe':                  'libgl1-amdgpu-pro-ext',                   
    'libgl1-amdgpu-pro-ext-hwe:i386':             'lib32-libgl1-amdgpu-pro-ext',             
    'libgl1-amdgpu-pro-glx':                      'libgl1-amdgpu-pro-glx',                   
    'libgl1-amdgpu-pro-glx:i386':                 'lib32-libgl1-amdgpu-pro-glx',             
    'libglapi-amdgpu-mesa':                       'libglapi-amdgpu-mesa',                    
    'libglapi-amdgpu-mesa:i386':                  'lib32-libglapi-amdgpu-mesa',              
    'libglapi1-amdgpu-pro':                       'libglapi1-amdgpu-pro',                    
    'libglapi1-amdgpu-pro:i386':                  'lib32-libglapi1-amdgpu-pro',              
    'libgles1-amdgpu-mesa':                       'libgles1-amdgpu-mesa',                    
    'libgles1-amdgpu-mesa:i386':                  'lib32-libgles1-amdgpu-mesa',              
    'libgles1-amdgpu-mesa-dev':                   'libgles1-amdgpu-mesa',                    
    'libgles1-amdgpu-mesa-dev:i386':              'lib32-libgles1-amdgpu-mesa',              
    'libgles2-amdgpu-mesa':                       'libgles2-amdgpu-mesa',                    
    'libgles2-amdgpu-mesa:i386':                  'lib32-libgles2-amdgpu-mesa',              
    'libgles2-amdgpu-mesa-dev':                   'libgles2-amdgpu-mesa',                    
    'libgles2-amdgpu-mesa-dev:i386':              'lib32-libgles2-amdgpu-mesa',              
    'libgles2-amdgpu-pro':                        'libgles2-amdgpu-pro',                     
    'libgles2-amdgpu-pro:i386':                   'lib32-libgles2-amdgpu-pro',               
    'libllvm7.1-amdgpu':                          'libllvm7.1-amdgpu',                       
    'libllvm7.1-amdgpu:i386':                     'lib32-libllvm7.1-amdgpu',                 
    'libopencl1-amdgpu-pro':                      'libopencl1-amdgpu-pro',                   
    'libopencl1-amdgpu-pro:i386':                 'lib32-libopencl1-amdgpu-pro',             
    'libosmesa6-amdgpu':                          'libosmesa6-amdgpu',                       
    'libosmesa6-amdgpu:i386':                     'lib32-libosmesa6-amdgpu',                 
    'libosmesa6-amdgpu-dev':                      'libosmesa6-amdgpu',                       
    'libosmesa6-amdgpu-dev:i386':                 'lib32-libosmesa6-amdgpu',                 
    'libwayland-amdgpu-client0':                  'libwayland-amdgpu-client0',               
    'libwayland-amdgpu-client0:i386':             'lib32-libwayland-amdgpu-client0',         
    'libwayland-amdgpu-cursor0':                  'libwayland-amdgpu-cursor0',               
    'libwayland-amdgpu-cursor0:i386':             'lib32-libwayland-amdgpu-cursor0',         
    'libwayland-amdgpu-dev':                      'libwayland-amdgpu',                       
    'libwayland-amdgpu-dev:i386':                 'lib32-libwayland-amdgpu',                 
    'libwayland-amdgpu-doc':                      'libwayland-amdgpu-doc',                   
    'libwayland-amdgpu-egl1':                     'libwayland-amdgpu-egl1',                  
    'libwayland-amdgpu-egl1:i386':                'lib32-libwayland-amdgpu-egl1',            
    'libwayland-amdgpu-server0':                  'libwayland-amdgpu-server0',               
    'libwayland-amdgpu-server0:i386':             'lib32-libwayland-amdgpu-server0',         
    'libxatracker-amdgpu-dev':                    'libxatracker-amdgpu',                     
    'libxatracker-amdgpu-dev:i386':               'lib32-libxatracker-amdgpu',               
    'libxatracker2-amdgpu':                       'libxatracker2-amdgpu',                    
    'libxatracker2-amdgpu:i386':                  'lib32-libxatracker2-amdgpu',              
    'llvm-amdgpu':                                'llvm-amdgpu',                             
    'llvm-amdgpu:i386':                           'lib32-llvm-amdgpu',                       
    'llvm-amdgpu-7.1':                            'llvm-amdgpu-7.1',                         
    'llvm-amdgpu-7.1:i386':                       'lib32-llvm-amdgpu-7.1',                   
    'llvm-amdgpu-7.1-dev':                        'llvm-amdgpu-7.1',                         
    'llvm-amdgpu-7.1-dev:i386':                   'lib32-llvm-amdgpu-7.1',                   
    'llvm-amdgpu-7.1-doc':                        'llvm-amdgpu-7.1-doc',                     
    'llvm-amdgpu-7.1-runtime':                    'llvm-amdgpu-7.1-runtime',                 
    'llvm-amdgpu-7.1-runtime:i386':               'lib32-llvm-amdgpu-7.1-runtime',           
    'llvm-amdgpu-dev':                            'llvm-amdgpu',                             
    'llvm-amdgpu-dev:i386':                       'lib32-llvm-amdgpu',                       
    'llvm-amdgpu-runtime':                        'llvm-amdgpu-runtime',                     
    'llvm-amdgpu-runtime:i386':                   'lib32-llvm-amdgpu-runtime',               
    'mesa-amdgpu-common-dev':                     'mesa-amdgpu-common',                      
    'mesa-amdgpu-common-dev:i386':                'lib32-mesa-amdgpu-common',                
    'mesa-amdgpu-omx-drivers':                    'mesa-amdgpu-omx-drivers',                 
    'mesa-amdgpu-omx-drivers:i386':               'lib32-mesa-amdgpu-omx-drivers',           
    'mesa-amdgpu-va-drivers':                     'mesa-amdgpu-va-drivers',                  
    'mesa-amdgpu-va-drivers:i386':                'lib32-mesa-amdgpu-va-drivers',            
    'mesa-amdgpu-vdpau-drivers':                  'mesa-amdgpu-vdpau-drivers',               
    'mesa-amdgpu-vdpau-drivers:i386':             'lib32-mesa-amdgpu-vdpau-drivers',         
    'opencl-amdgpu-pro':                          'opencl-amdgpu-pro-meta',                  
    'opencl-amdgpu-pro-dev':                      'opencl-amdgpu-pro',                       
    'opencl-amdgpu-pro-icd':                      'opencl-amdgpu-pro-icd',                   
    'opencl-orca-amdgpu-pro-icd':                 'opencl-orca-amdgpu-pro-icd',              
    'opencl-orca-amdgpu-pro-icd:i386':            'lib32-opencl-orca-amdgpu-pro-icd',        
    'roct-amdgpu-pro':                            'roct-amdgpu-pro',                         
    'roct-amdgpu-pro-dev':                        'roct-amdgpu-pro',                         
    'vulkan-amdgpu':                              'vulkan-amdgpu',                           
    'vulkan-amdgpu:i386':                         'lib32-vulkan-amdgpu',                     
    'vulkan-amdgpu-pro':                          'vulkan-amdgpu-pro',                       
    'vulkan-amdgpu-pro:i386':                     'lib32-vulkan-amdgpu-pro',                 
    'wayland-protocols-amdgpu':                   'wayland-protocols-amdgpu',                
    'wsa-amdgpu':                                 'wsa-amdgpu',                              
    'wsa-amdgpu:i386':                            'lib32-wsa-amdgpu',                        
    'xserver-xorg-amdgpu-video-amdgpu':           None,                                      #disabled_because_hwe_version_is_available
    'xserver-xorg-amdgpu-video-amdgpu:i386':      None,                                      #disabled_because_hwe_version_is_available
    'xserver-xorg-hwe-amdgpu-video-amdgpu':       'xserver-xorg-amdgpu-video-amdgpu',        
    'xserver-xorg-hwe-amdgpu-video-amdgpu:i386':  'lib32-xserver-xorg-amdgpu-video-amdgpu',  

    # Not yet checked carefully manually
}



## maps debian dependencies to arch dependencies
replace_deps = {
    #"libc6":                None,
    #"libgcc1":              None,
    #"libstdc++6":           None,
    #"libx11-6":             "libx11",
    #"libx11-xcb1":          None,
    #"libxcb-dri2-0":        "libxcb",
    #"libxcb-dri3-0":        "libxcb",
    #"libxcb-present0":      "libxcb",
    #"libxcb-sync1":         "libxcb",
    #"libxcb-glx0":          "libxcb",
    #"libxcb1":              "libxcb",
    #"libxext6":             "libxext",
    #"libxshmfence1":        "libxshmfence",
    #"libxdamage1":          "libxdamage",
    #"libxfixes3":           "libxfixes",
    #"libxxf86vm1":          "libxxf86vm",
    #"libudev1":             "libsystemd",
    #"libpciaccess0":        "libpciaccess",
    #"libepoxy0":            "libepoxy",
    #"libelf1":              None, # no lib32- package in Arch, just disabling for now
    #"xserver-xorg-core":    "xorg-server",
    #"libcunit1":            "bcunit",
    #"libdrm-radeon1":       "libdrm",
    #"amdgpu-pro-firmware":  "linux-firmware",
    #"libssl1.0.0":          "openssl",
    #"zlib1g":               "zlib",

    #"libvdpau1": "libvdpau",
    #"libtinfo5": "ncurses5-compat-libs",
    #"libgstreamer1.0-0": "gstreamer",
    #"libgstreamer-plugins-base1.0-0": "gst-plugins-base",
    #"libglib2.0-0": "glib2",
    #"libomxil-bellagio0": "libomxil-bellagio",

    ## replace *-dev packages with arch linux ones containing the headers
    #"libffi-dev": "libffi",
    #"lib32-libffi-dev": "lib32-libffi",
    #"libtinfo-dev": "ncurses",
    #"lib32-libtinfo-dev": "lib32-ncurses",
    #"libedit2": "libedit",
    #"libpci3": "pciutils",


    ##"libjs-jquery": "jquery",
    ##"libjs-underscorea": "underscorejs" # the underscroejs AUR pkg dos not install to /usr/share/javascript !
    #"libjs-jquery":       None,
    #"libjs-underscorea":  None,
    
    # Further is made by me (Ashark)
    # To make this list I used:
    #cat Packages | grep Depends | sed 's/Depends: //' | sed 's/, /\n/g' | sort -u | grep -v "amdgpu" > list_tmp # extra deps in debian
    #cat list_tmp | cut -f1 -d" " | sort -u > list_tmp2 # removed versions
    #echo > list_tmp3 # clear file
    #for line in $(cat list_tmp2); do
    #echo now processing $line;
    #arch_dep=`bash ./translate_deb_to_arch_dependency.sh $line`; # https://github.com/helixarch/debtap/issues/41#issuecomment-489166020
    #if [[ $arch_dep == "could_not_translate" ]]; then arch_str="'$line', #could_not_auto_translate";
    #elif [[ $arch_dep == "" ]]; then arch_str="None, #auto_translated";
    #else arch_str="'$arch_dep', #auto_translated"
    #fi
    #str="'$line': "; str="$str $arch_str"; echo $str >> list_tmp3;
    #done
    #cat list_tmp3 | column -t | sed 's/^'\''/    '\''/' > list_tmp4 # prepare columns
    # Then we need to carefully check deps mapping manually.
    'binfmt-support':                  'opera',                    #auto_translated
    'dkms':                            'dkms',                     #auto_translated
    'libc6':                           'aarch64-linux-gnu-glibc',  #auto_translated
    'libcunit1':                       'cunit',                    #auto_translated
    'libedit2':                        'libedit',                  #auto_translated
    'libelf1':                         'libelf',                   #auto_translated
    'libepoxy0':                       'libepoxy',                 #auto_translated
    'libexpat1':                       'expat',                    #auto_translated
    'libffi6':                         'libffi',                   #auto_translated
    'libffi-dev':                      'libffi',                   #auto_translated
    'libgcc1':                         None,                       #auto_translated
    'libglib2.0-0':                    'glib2',                    #auto_translated
    'libgstreamer1.0-0':               'gstreamer',                #auto_translated
    'libgstreamer-plugins-base1.0-0':  'gst-plugins-base-libs',    #auto_translated
    'libjs-jquery':                    'libjs-jquery',             #could_not_auto_translate
    'libjs-underscore':                'libjs-underscore',         #could_not_auto_translate
    'libmirclient-dev':                'libmirclient-dev',         #could_not_auto_translate
    'libnuma1':                        'numactl',                  #auto_translated
    'libomxil-bellagio0':              'libomxil-bellagio',        #auto_translated
    'libpci3':                         None,                       #auto_translated
    'libselinux1':                     'libselinux',               #auto_translated
    'libstdc++6':                      'aarch64-linux-gnu-gcc',    #auto_translated
    'libtinfo5':                       'libtinfo5',                #could_not_auto_translate
    'libtinfo-dev':                    'libtinfo-dev',             #could_not_auto_translate
    'libudev1':                        'systemd-libs',             #auto_translated
    'libudev-dev':                     'systemd-libs',             #auto_translated
    'libx11-6':                        'libx11',                   #auto_translated
    'libx11-dev':                      'libx11',                   #auto_translated
    'libx11-xcb1':                     'libx11',                   #auto_translated
    'libx11-xcb-dev':                  'libx11',                   #auto_translated
    'libxcb1':                         'libxcb',                   #auto_translated
    'libxcb-dri2-0':                   'libxcb',                   #auto_translated
    'libxcb-dri2-0-dev':               'libxcb',                   #auto_translated
    'libxcb-dri3-0':                   'libxcb',                   #auto_translated
    'libxcb-dri3-dev':                 'libxcb',                   #auto_translated
    'libxcb-glx0':                     'libxcb',                   #auto_translated
    'libxcb-glx0-dev':                 'libxcb',                   #auto_translated
    'libxcb-present0':                 'libxcb',                   #auto_translated
    'libxcb-present-dev':              'libxcb',                   #auto_translated
    'libxcb-sync1':                    'libxcb',                   #auto_translated
    'libxcb-sync-dev':                 'libxcb',                   #auto_translated
    'libxcb-xfixes0':                  'libxcb',                   #auto_translated
    'libxdamage1':                     'libxdamage',               #auto_translated
    'libxdamage-dev':                  'libxdamage',               #auto_translated
    'libxext6':                        'libxext',                  #auto_translated
    'libxext-dev':                     'libxext',                  #auto_translated
    'libxfixes3':                      'libxfixes',                #auto_translated
    'libxfixes-dev':                   'libxfixes',                #auto_translated
    'libxml2':                         'libxml2',                  #auto_translated
    'libxshmfence1':                   'libxshmfence',             #auto_translated
    'libxshmfence-dev':                'libxshmfence',             #auto_translated
    'libxxf86vm1':                     'libxxf86vm',               #auto_translated
    'libxxf86vm-dev':                  'libxxf86vm',               #auto_translated
    'x11proto-dri2-dev':               'x11proto-dri2-dev',        #could_not_auto_translate
    'x11proto-gl-dev':                 'x11proto-gl-dev',          #could_not_auto_translate
    'xserver-xorg-hwe-18.04':          'xserver-xorg-hwe-18.04',   #could_not_auto_translate
    'zlib1g':                          'zlib',                     #auto_translated
    # Not yet mapped manually
}

## do not convert the dependencies listed to lib32 variants
no_lib32_convert = [
    "binfmt-support"
]

## override the version requirement extracted from deb
replace_version = {
    "libdrm-amdgpu": "= redefined", # doesn't work for some reason, TODO fix that
}

## maps debians archs to arch's archs
architectures_map = {
    "amd64": "x86_64",
    "i386": "i686",
    "all": "any"
}

# To see list of uniq licences files and packages that uses them, I used this:
    # tmpdir=tmpdir; rm -rf "$tmpdir"; mkdir "$tmpdir";
    # for file in  $(ls *deb);
    # do
    #     cd "$tmpdir"
    #     ar x ../$file data.tar.xz
    #     files=$(tar -tf data.tar.xz)
    #     if [[ $files != "" ]]; then
    #         tar -xvf data.tar.xz ./usr/share/doc;
    #         rm data.tar.xz;
    #     fi
    #     files=""; cd ..
    # done
    #
    # cd tmpdir/usr/share/doc
    # rm list_tmp
    # for dir in $(ls -d *); do
    #     md5sum $dir/copyright >> list_tmp
    # done
    # cat list_tmp | sort
# Then I mapped each copyright hash to its short licence name:

licenses_hashes_map = {
    "063e0448ac11bde832bec75b88775293": "custom",
    "1cc2ccbd48178dec3ac4fe3f75deb273": "MIT",
    "241ed682eeb4973b7b7ac9131624f31f": "custom",
    "41133d491f0177abc7dcd732e55763d3": "custom",
    "65863e6b7e72f9b0d6921bfb874872e2": "MIT",
    "66f2e857194d9a397e5d81fedef2fb99": "X11",
    "7409e7a90acac9454eac07568798ae6e": "MIT",
    "757ddbf4ba06bfecb85c5bd02f8e188c": "custom",
    "75da66945980a43adf1e1856271b9d4a": "custom",
    "acc80450c1bd42944061a30272f0c132": "MIT",
    "b1afa13daf74f4073c4813368bc1b1b0": "MIT",
    "c7b12b6702da38ca028ace54aae3d484": "MIT",
    "d41d8cd98f00b204e9800998ecf8427e": "empty license?",
    "e0bd46672d2d82a9d57216a931d0e0bf": "custom:AMD GPU-PRO",
    "f2b0e0926d102efc9a09f8b9a740209d": "GPL2",
}

# To see list of suggested and recommended packages:
# cat Packages-extracted | egrep "Suggest|Recommends" | sort -u
optdepends_descriptions = {
    "libegl1-amdgpu-mesa-drivers":   "TODO_some_description",
    "libgl1-amdgpu-mesa-dri":        "TODO_some_description",
    "libgl1-amdgpu-pro-dri":         "TODO_some_description",
    #"libtxc-dxtn-s2tc0 | libtxc-dxtn0": "TODO_some_description", # which variant?
    "llvm-amdgpu-7.1-dev":           "TODO_some_description",
    "libglide3":                     "TODO_some_description",
    "linux-firmware":                "TODO_some_description",
    "llvm-amdgpu-7.1-doc":           "TODO_some_description",
}

if not debugging:
    subprocess.run(["wget", "--referer", url_ref, "-N", source_url_resolved])

def hashFile(file):
    block = 64 * 1024
    hash = hashlib.sha256()
    with open(file, 'rb') as f:
        buf = f.read(block)
        while len(buf) > 0:
            hash.update(buf)
            buf = f.read(block)
    return hash.hexdigest()

sources = [ source_url ]
sha256sums = [ hashFile(source_file) ]

patches = sorted(glob.glob("*.patch"))

for patch in patches:
    sources.append(patch)
    sha256sums.append(hashFile(patch))

#sources.append("20-amdgpu.conf")
#sha256sums.append(hashFile("20-amdgpu.conf"))

header_tpl = """# Author: Janusz Lewandowski <lew21@xtreeme.org>
# Contributor: David McFarland <corngood@gmail.com>
# Autogenerated from AMD's Packages file

major={pkgver_base}
minor={pkgver_build}

pkgbase=amdgpu-pro-installer
pkgname={package_names}
pkgver=${{major}}_${{minor}}
pkgrel={pkgrel}
arch=('x86_64')
url='https://www.amd.com/en/support/kb/release-notes/rn-rad-lin-19-10-unified'
license=('custom')
makedepends=('wget')

DLAGENTS='{dlagents}'

source=({source})
sha256sums=({sha256sums})

"""

if debug_pkgext:
    header_tpl += "PKGEXT=\".pkg.tar\"\n"

package_functions = """
# extracts a debian package
# $1: deb file to extract
extract_deb() {
    local tmpdir="$(basename "${1%.deb}")"
    rm -Rf "$tmpdir"
    mkdir "$tmpdir"
    cd "$tmpdir"
    ar x "$1"
    tar -C "${pkgdir}" -xf data.tar.xz
}
# move ubuntu specific /usr/lib/x86_64-linux-gnu to /usr/lib
# $1: debian package library dir (goes from opt/amdgpu or opt/amdgpu-pro and from x86_64 or i386)
# $2: arch package library dir (goes to usr/lib or usr/lib32)
move_libdir() {
    local deb_libdir="$1"
    local arch_libdir="$2"

    if [ -d "${pkgdir}/${deb_libdir}" ]; then
        if [ ! -d "${pkgdir}/${arch_libdir}" ]; then
            mkdir -p "${pkgdir}/${arch_libdir}"
        fi
        mv -t "${pkgdir}/${arch_libdir}/" "${pkgdir}/${deb_libdir}"/*
        find ${pkgdir} -type d -empty -delete
    fi
}
# move copyright file to proper place and remove debian changelog
# move_copyright() {
#     pkgname_deb=${pkgname//-meta}; pkgname_deb=${pkgname_deb/lib32-/};
#     rm "${pkgdir}/usr/share/doc/${pkgname_deb}/changelog.Debian.gz"
#     mkdir -p ${pkgdir}/usr/share/licenses/${pkgname}
#     mv ${pkgdir}/usr/share/doc/${pkgname_deb}/copyright ${pkgdir}/usr/share/licenses/${pkgname}
#     find ${pkgdir}/usr/share/doc -type d -empty -delete
# }
# remove copyright file and remove debian changelog - only while debugging, not for release
remove_copyright() {
    pkgname_deb=${pkgname//-meta}; pkgname_deb=${pkgname_deb/lib32-/};
    rm "${pkgdir}/usr/share/doc/${pkgname_deb}/changelog.Debian.gz"
    rm "${pkgdir}/usr/share/doc/${pkgname_deb}/copyright" # only while debugging, not for release
    find ${pkgdir}/usr -type d -empty -delete
}
"""

package_header_tpl = """package_{NAME} () {{
    pkgdesc={DESC}
"""

package_deb_extract_tpl = """    extract_deb "${{srcdir}}"/amdgpu-pro-${{major}}-${{minor}}-ubuntu-18.04/{Filename}
"""

package_move_libdir_tpl = """    move_libdir "opt/amdgpu{PRO}/lib/{DEBDIR}-linux-gnu" "usr/lib{ARCHDIR}"
"""

package_move_copyright = """    remove_copyright
"""

package_lib32_cleanup = """
    # lib32 cleanup
    rm -rf "${pkgdir}"/usr/{bin,lib,include,share} "${pkgdir}/var" "${pkgdir}"/opt/amdgpu-pro/{bin,include,share}
    rm -rf "${pkgdir}"/opt/amdgpu-pro/lib/xorg/modules/extensions/
"""

package_footer = """}
"""

default_arch = ['x86_64']


def quote(string):
    return "\"" + string.replace("\\", "\\\\").replace("\"", "\\\"") + "\""

class Package:
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

        if not hasattr(self, "arch"):
            self.arch = default_arch
        self.deb_source_infos = []

        self.optdepends = []

    def fill_arch_info(self, deb_info):
        self.deb_source_infos.append(deb_info)

        try:
            self.arch = [architectures_map[deb_info["Architecture"]], ]
        except:
            self.arch = default_arch

        if deb_info["Architecture"] == "i386":
            if self.arch_pkg_name.startswith('lib32-'):
                self.arch = ['x86_64']
            else:
                import sys
                sys.stderr.write("ERROR: There is a bug in this script, package '%s' is i386 (came from %s) and should start with 'lib32'. Check packages_map!\n" % (self.arch_pkg_name, deb_info["Package"]))


        try:
            deb_deps = deb_info["Depends"].split(', ')
        except:
            deb_deps = None

        domap = True
        #if self.arch_pkg_name == "amdgpu-pro" or self.arch_pkg_name == "lib32-amdgpu-pro":
            #domap = False

        if deb_deps:
            deb_deps = [ depWithAlt_to_singleDep(dep) if dependencyWithAltRE.search(dep) else dep for dep in deb_deps ]
            deb_deps = [ dependencyNameWithVersionRE.match(dep).groups() for dep in deb_deps ]
            deb_deps = [(replace_deps[deb_pkg_name] if deb_pkg_name in replace_deps else deb_pkg_name, version) for deb_pkg_name, version in deb_deps]
            deb_deps = ["\"" + convertName(lib32_prefix_if_32bit(deb_pkg_name), deb_info, domap) + convertVersionSpecifier(deb_pkg_name, version) + "\"" for deb_pkg_name, version in deb_deps if deb_pkg_name]
            deb_deps = [ dep for dep in deb_deps if not dep.startswith("\"=")]

            # remove all dependencies on itself
            deb_deps = [ dep for dep in deb_deps if dep[1:len(self.arch_pkg_name)+1] != self.arch_pkg_name ]

            if hasattr(self, 'depends') and self.depends:
                deb_deps += self.depends

            self.depends = list(sorted(set( deb_deps ))) # remove duplicates and append to already existing dependencies

        try:
            deb_suggs = deb_info["Suggests"].split(', ')
        except:
            deb_suggs = None

        try:
            deb_recomms = deb_info["Recommends"].split(', ')
        except:
            deb_recomms = None

        deb_optdeps = []
        if deb_suggs:
            deb_optdeps = deb_suggs
        if deb_recomms:
            deb_optdeps = deb_optdeps + deb_recomms

        deb_optdeps = [depWithAlt_to_singleDep(dep) if dependencyWithAltRE.search(dep) else dep for dep in deb_optdeps]
        deb_optdeps = [dependencyNameWithVersionRE.match(dep).groups() for dep in deb_optdeps]
        deb_optdeps = [(replace_deps[deb_pkg_name] if deb_pkg_name in replace_deps else deb_pkg_name, version) for deb_pkg_name, version in deb_optdeps]
        deb_optdeps = ["\"" + convertName(lib32_prefix_if_32bit(deb_pkg_name), deb_info, domap) + convertVersionSpecifier(deb_pkg_name, version) + ": "
                       + (optdepends_descriptions[deb_pkg_name] if deb_pkg_name in optdepends_descriptions else "Warning unspecified optdep description" )
                       + "\"" for deb_pkg_name, version in deb_optdeps if deb_pkg_name]
        self.optdepends = self.optdepends + list(sorted(set(deb_optdeps)))

        if not hasattr(self, 'desc'):
            desc = deb_info["Description"].split("\n")
            if len(desc) > 2:
                desc = desc[0]
            else:
                desc = " ".join(x.strip() for x in desc)

            if deb_info["Architecture"] == "i386":
                desc += ' (32-bit)'

            self.desc = desc

        if not hasattr(self, 'version'):
            ver = deb_info["Version"]
            ver = ver.replace(pkgver_base, "${major}").replace(pkgver_build, "${minor}").replace("-","_").replace("1:","")
            #if ver != "${major}_${minor}":
            self.version = ver

        deb_info["Filename"] = deb_info["Filename"].replace("./","")
        deb_file = debfile.DebFile("src/amdgpu-pro-19.10-785425-ubuntu-18.04/%s" % deb_info["Filename"])

        if not hasattr(self, 'license'):
            copyright_md5 = deb_file.md5sums()[b'usr/share/doc/%s/copyright' % (str.encode(deb_info["Package"]))]
            if copyright_md5 in licenses_hashes_map:
                self.license = "('%s')" % licenses_hashes_map[copyright_md5]
            else:
                self.license = "('NOT_IN_MAP')"

        if not hasattr(self,'backup'):
            if deb_file.control.has_file("conffiles"):
                self.backup = [ line.decode('utf-8').replace("\n","") for line in deb_file.control.get_file("conffiles") if line.decode('utf-8') ]
                self.backup = [ re.sub("^/", "", line) for line in self.backup ] # removing leading slash

        if not hasattr(self, 'install'):
            if Path("%s.install" % self.arch_pkg_name).is_file():
                self.install = "%s.install" % self.arch_pkg_name


    def toPKGBUILD(self):
        ret = package_header_tpl.format(
            NAME=self.arch_pkg_name,
            DESC=quote(self.desc) if hasattr(self, 'desc') else quote("No description for package %s" % self.arch_pkg_name),
        )

        if hasattr(self, 'version'):
            ret += "    pkgver=%s\n" % self.version
        if hasattr(self, 'license'):
            ret += "    license=%s\n" % self.license
        if hasattr(self, 'install'):
            ret += "    install=%s\n" % self.install

        # add any given list/array with one of those names to the pkgbuild
        for array in ('arch', 'provides', 'conflicts', 'replaces', 'groups'):
            if(hasattr(self, array)):
                ret += "    %s=('%s')\n" % (array, "' '".join(getattr(self, array)))

        if hasattr(self, 'depends'):
            ret += "    depends=(%s)\n" % " ".join(self.depends)
        if self.optdepends:
            ret += "    optdepends=(%s)\n" % "\n                ".join(self.optdepends)
        if hasattr(self, 'backup'):
            ret += "    backup=(%s)\n" % " ".join(self.backup)

        ret += "\n" # separating variables and functions with empty line

        for info in self.deb_source_infos:
            tmp_str=package_deb_extract_tpl.format(**info)
            ret += tmp_str.replace(str(pkgver_base), "${major}").replace(str(pkgver_build), "${minor}")

        if not self.arch_pkg_name.endswith("-meta"):
            PRO=""
            DEBDIR=""
            ARCHDIR=""
            if "amdgpu-pro" in self.arch_pkg_name:
                PRO="-pro"
            if self.arch_pkg_name.startswith('lib32-'):
                DEBDIR="i386"
                ARCHDIR="32"
            else:
                DEBDIR="x86_64"
                ARCHDIR=""
            ret += package_move_libdir_tpl.format(
                PRO=PRO,
                DEBDIR=DEBDIR,
                ARCHDIR=ARCHDIR,
            )

        ret += package_move_copyright

        if hasattr(self, 'extra_commands'):
            ret += "\n    # extra_commands:\n    "
            ret += "\n    ".join( self.extra_commands )

        if self.arch_pkg_name.startswith('lib32-'):
            ret += package_lib32_cleanup
        ret += package_footer
        return ret


pkgbuild_packages = gen_arch_packages()


# regex for parsing version information of a deb dependency
dependencyNameWithVersionRE = re.compile(r"([^ ]+)(?: \((.+)\))?")

# regex for detecting dependency with alternative
dependencyWithAltRE = re.compile(r" \| ")

def depWithAlt_to_singleDep(depWithAlt):
    # I (Ashark) used this to get a list of dependencies with alternatives:
    # cat Packages | grep -vE "Filename|Size|MD5sum|SHA1|SHA256|Priority|Maintainer|Version: 19.10-785425|Description|^ +" >  Packages-short-nodesc
    # cat Packages-short-nodesc | grep Depends | grep "|" | sed "s/Depends: //" | sed "s/, /\n/g" | grep "|" | sort -u # also see Recommends and Suggests
    # And I got this list:
        # amdgpu (= 19.10-785425) | amdgpu-hwe (= 19.10-785425) # choose latest (i.e. hwe)
        # amdgpu-lib (= 19.10-785425) | amdgpu-lib-hwe (= 19.10-785425) # choose latest (i.e. hwe)
        # amdgpu-pro (= 19.10-785425) | amdgpu-pro-hwe (= 19.10-785425) # choose latest (i.e. hwe)
        # libudev1 | libudev0 # choose latest (i.e. libudev1)
        # libva1-amdgpu | libva2-amdgpu | libva1 | libva2 # choose latest (i.e. libva2*) But don't know which variant
        # libvdpau1-amdgpu | libvdpau1 # do not know which variant

    splitted_alts = dependencyWithAltRE.split(depWithAlt)
    splitted_name_and_ver = [dependencyNameWithVersionRE.match(dep).groups() for dep in splitted_alts]

    if splitted_name_and_ver[0][0] + "-hwe" == splitted_name_and_ver[1][0]:
        return splitted_alts[1] # use hwe variant
    if splitted_name_and_ver[0][0] == "libudev1" and splitted_name_and_ver[1][0] == "libudev0":
        return splitted_alts[0] # use libudev1 variant
    if splitted_name_and_ver[0][0] == "libva1-amdgpu" and splitted_name_and_ver[1][0] == "libva2-amdgpu" and splitted_name_and_ver[2][0] == "libva1" and splitted_name_and_ver[3][0] == "libva2":
        return "TODO_Do_not_know_what_to_choose" # TODO set correct variant here
    if splitted_name_and_ver[0][0] == "libvdpau1-amdgpu" and splitted_name_and_ver[1][0] == "libvdpau1":
        return "TODO_Do_not_know_what_to_choose" # TODO set correct variant here
    if splitted_name_and_ver[0][0] == "libtxc-dxtn-s2tc0" and splitted_name_and_ver[1][0] == "libtxc-dxtn0": # from libgl1-amdgpu-mesa-dri Recommends array
        return "TODO_Do_not_know_what_to_choose" # TODO set correct variant here
    return "Warning_Do_not_know_which_alt_to_choose"

deb_archs={}

def convertName(name, deb_info, domap=True):
    ret = name
    if deb_info["Architecture"] == "i386" and (name not in deb_archs or "any" not in deb_archs[name]):
        if not name in no_lib32_convert:
            ret = "lib32-" + name

    if name in packages_map:
        if domap:
            return packages_map[name]
        return ""
    return ret

def convertVersionSpecifier(name, spec):
    if name in replace_version:
        return replace_version[name]
    if not spec:
        return ""

    sign, spec = spec.split(" ", 1)

    spec = spec.strip()
    if ":" in spec: # debian epochs means nothing in arch context, so strip them
        deb_epoch, spec = spec.rsplit(":", 1)
        # also would be good to omit debian-revision, as it has nothing to do with arch's pkgrel
        # but anyway we omit > and >= deps, so I did not implemented it yet
    if name in deb_package_names:
        spec = spec.replace(pkgver_base, "${major}").replace(pkgver_build, "${minor}").replace("-","_")
        if not re.search(r'minor', spec):
            spec = spec + "_${minor}"
        spec = spec + "-${pkgrel}"
        return sign + spec
    if sign == ">" or sign == ">=": # assume Arch users have latest versions of all packages
        return ""
    return sign + spec

dep32RE = re.compile(r"(.*):i386")
def lib32_prefix_if_32bit(dep):
    rdep = dep
    match = dep32RE.match(dep)
    if match:
        rdep = match.group(1)
        if not rdep in no_lib32_convert:
            rdep = 'lib32-%s' % rdep
    return rdep



# get list of unique arch packages from package map
arch_package_names=list(pkgbuild_packages.keys())
deb_package_names=[]

if not debugging:
    print(header_tpl.format(
        package_names="(\n" + "\n".join( arch_package_names ) + "\n)",
        pkgrel=pkgrel,
        dlagents=dlagents,
        pkgver_base=pkgver_base,
        pkgver_build=pkgver_build,
        source="\n\t".join(sources),
        sha256sums="\n\t".join(sha256sums)
    ))

    print(package_functions)

f = ""
if not debugging:
    with lzma.open(source_file, "r") as tar:
        with tarfile.open(fileobj=tar) as tf:
            tf.extractall("src")
    f = open("src/amdgpu-pro-%s-%s-ubuntu-18.04/Packages" % (pkgver_base, pkgver_build), "r")
else:
    f = open("Packages-debugging", "r")

deb_package_list = []

for deb_info in deb822.Packages.iter_paragraphs(f):
    if not deb_info["Package"] in deb_archs:
        deb_archs[deb_info["Package"]] = set()

    deb_archs[deb_info["Package"]].add(deb_info["Architecture"])
    deb_package_list.append(deb_info)

deb_package_names = [info["Package"] + ":i386" if info["Architecture"] == "i386" else info["Package"] for info in deb_package_list]

f.close()

for deb_info in deb_package_list:
    name = deb_info["Package"]
    arch_pkg = None
    if deb_info["Architecture"] == "i386":
        name = deb_info["Package"] + ":i386"
    if name in packages_map:  # to allow temporary commenting out mappings from packages_map while using full Packages file
        if packages_map[name] in pkgbuild_packages:  # to allow temporary commenting out packages from pkgbuild_packages
            arch_pkg = pkgbuild_packages[packages_map[name]]

    if arch_pkg:
        arch_pkg.fill_arch_info(deb_info)

for pkg in arch_package_names:
    print(pkgbuild_packages[pkg].toPKGBUILD())
