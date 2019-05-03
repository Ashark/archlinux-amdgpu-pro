from debian import deb822
import re
import gzip
import lzma
import tarfile
import subprocess
import hashlib
import glob

pkgver_base = "19.10"
pkgver_build = "785425"
pkgrel = 1
debug_pkgext = False


pkgver = "{0}.{1}".format(pkgver_base, pkgver_build)
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
        
        # To generate this I used:
        # cat list_tmp3 | cut -f4 -d"'" | sort -u > list_tmp4
        # for line in $(cat list_tmp4); do echo -e "        '$line': Package(\n        ),"; done
        # desc attribute could be used to override Description from deb package.
        'amdgpu': Package(
        ),
        'amdgpu-core': Package(
        ),
        'amdgpu-dkms': Package(
        ),
        'amdgpu-doc': Package(
        ),
        'amdgpu-hwe': Package(
        ),
        'amdgpu-lib': Package(
        ),
        'amdgpu-lib32': Package(
        ),
        'amdgpu-lib-hwe': Package(
        ),
        'amdgpu-pro': Package(
        ),
        'amdgpu-pro-core': Package(
        ),
        'amdgpu-pro-hwe': Package(
        ),
        'amdgpu-pro-lib32': Package(
        ),
        'amdgpu-pro-pin': Package(
        ),
        'amf-amdgpu-pro': Package(
        ),
        'clinfo-amdgpu-pro': Package(
        ),
        'glamor-amdgpu': Package(
        ),
        'gst-omx-amdgpu': Package(
        ),
        'lib32-amdgpu': Package(
        ),
        'lib32-amdgpu-hwe': Package(
        ),
        'lib32-amdgpu-lib': Package(
        ),
        'lib32-amdgpu-lib-hwe': Package(
        ),
        'lib32-amdgpu-pro': Package(
        ),
        'lib32-amdgpu-pro-hwe': Package(
        ),
        'lib32-clinfo-amdgpu-pro': Package(
        ),
        'lib32-glamor-amdgpu': Package(
        ),
        'lib32-gst-omx-amdgpu': Package(
        ),
        'lib32-libdrm2-amdgpu': Package(
        ),
        'lib32-libdrm-amdgpu': Package(
        ),
        'lib32-libdrm-amdgpu-amdgpu1': Package(
        ),
        'lib32-libdrm-amdgpu-radeon1': Package(
        ),
        'lib32-libdrm-amdgpu-utils': Package(
        ),
        'lib32-libegl1-amdgpu-mesa': Package(
        ),
        'lib32-libegl1-amdgpu-mesa-drivers': Package(
        ),
        'lib32-libegl1-amdgpu-pro': Package(
        ),
        'lib32-libgbm1-amdgpu': Package(
        ),
        'lib32-libgbm1-amdgpu-pro': Package(
        ),
        'lib32-libgbm-amdgpu': Package(
        ),
        'lib32-libgl1-amdgpu-mesa': Package(
        ),
        'lib32-libgl1-amdgpu-mesa-dri': Package(
        ),
        'lib32-libgl1-amdgpu-mesa-glx': Package(
        ),
        'lib32-libgl1-amdgpu-pro-dri': Package(
        ),
        'lib32-libgl1-amdgpu-pro-ext': Package(
        ),
        'lib32-libgl1-amdgpu-pro-ext-hwe': Package(
        ),
        'lib32-libgl1-amdgpu-pro-glx': Package(
        ),
        'lib32-libglapi1-amdgpu-pro': Package(
        ),
        'lib32-libglapi-amdgpu-mesa': Package(
        ),
        'lib32-libgles1-amdgpu-mesa': Package(
        ),
        'lib32-libgles2-amdgpu-mesa': Package(
        ),
        'lib32-libgles2-amdgpu-pro': Package(
        ),
        'lib32-libllvm7.1-amdgpu': Package(
        ),
        'lib32-libopencl1-amdgpu-pro': Package(
        ),
        'lib32-libosmesa6-amdgpu': Package(
        ),
        'lib32-libwayland-amdgpu': Package(
        ),
        'lib32-libwayland-amdgpu-client0': Package(
        ),
        'lib32-libwayland-amdgpu-cursor0': Package(
        ),
        'lib32-libwayland-amdgpu-egl1': Package(
        ),
        'lib32-libwayland-amdgpu-server0': Package(
        ),
        'lib32-libxatracker2-amdgpu': Package(
        ),
        'lib32-libxatracker-amdgpu': Package(
        ),
        'lib32-llvm-amdgpu': Package(
        ),
        'lib32-llvm-amdgpu-7.1': Package(
        ),
        'lib32-llvm-amdgpu-7.1-runtime': Package(
        ),
        'lib32-llvm-amdgpu-runtime': Package(
        ),
        'lib32-mesa-amdgpu-common': Package(
        ),
        'lib32-mesa-amdgpu-omx-drivers': Package(
        ),
        'lib32-mesa-amdgpu-va-drivers': Package(
        ),
        'lib32-mesa-amdgpu-vdpau-drivers': Package(
        ),
        'lib32-opencl-orca-amdgpu-pro-icd': Package(
        ),
        'lib32-vulkan-amdgpu': Package(
        ),
        'lib32-vulkan-amdgpu-pro': Package(
        ),
        'lib32-wsa-amdgpu': Package(
        ),
        'lib32-xserver-xorg-amdgpu-video-amdgpu': Package(
        ),
        'lib32-xserver-xorg-hwe-amdgpu-video-amdgpu': Package(
        ),
        'libdrm2-amdgpu': Package(
        ),
        'libdrm-amdgpu': Package(
        ),
        'libdrm-amdgpu-amdgpu1': Package(
        ),
        'libdrm-amdgpu-common': Package(
        ),
        'libdrm-amdgpu-radeon1': Package(
        ),
        'libdrm-amdgpu-utils': Package(
        ),
        'libegl1-amdgpu-mesa': Package(
        ),
        'libegl1-amdgpu-mesa-drivers': Package(
        ),
        'libegl1-amdgpu-pro': Package(
        ),
        'libgbm1-amdgpu': Package(
        ),
        'libgbm1-amdgpu-pro': Package(
        ),
        'libgbm1-amdgpu-pro-base': Package(
        ),
        'libgbm-amdgpu': Package(
        ),
        'libgl1-amdgpu-mesa': Package(
        ),
        'libgl1-amdgpu-mesa-dri': Package(
        ),
        'libgl1-amdgpu-mesa-glx': Package(
        ),
        'libgl1-amdgpu-pro-appprofiles': Package(
        ),
        'libgl1-amdgpu-pro-dri': Package(
        ),
        'libgl1-amdgpu-pro-ext': Package(
        ),
        'libgl1-amdgpu-pro-ext-hwe': Package(
        ),
        'libgl1-amdgpu-pro-glx': Package(
        ),
        'libglapi1-amdgpu-pro': Package(
        ),
        'libglapi-amdgpu-mesa': Package(
        ),
        'libgles1-amdgpu-mesa': Package(
        ),
        'libgles2-amdgpu-mesa': Package(
        ),
        'libgles2-amdgpu-pro': Package(
        ),
        'libllvm7.1-amdgpu': Package(
        ),
        'libopencl1-amdgpu-pro': Package(
        ),
        'libosmesa6-amdgpu': Package(
        ),
        'libwayland-amdgpu': Package(
        ),
        'libwayland-amdgpu-client0': Package(
        ),
        'libwayland-amdgpu-cursor0': Package(
        ),
        'libwayland-amdgpu-doc': Package(
        ),
        'libwayland-amdgpu-egl1': Package(
        ),
        'libwayland-amdgpu-server0': Package(
        ),
        'libxatracker2-amdgpu': Package(
        ),
        'libxatracker-amdgpu': Package(
        ),
        'llvm-amdgpu': Package(
        ),
        'llvm-amdgpu-7.1': Package(
        ),
        'llvm-amdgpu-7.1-doc': Package(
        ),
        'llvm-amdgpu-7.1-runtime': Package(
        ),
        'llvm-amdgpu-runtime': Package(
        ),
        'mesa-amdgpu-common': Package(
        ),
        'mesa-amdgpu-omx-drivers': Package(
        ),
        'mesa-amdgpu-va-drivers': Package(
        ),
        'mesa-amdgpu-vdpau-drivers': Package(
        ),
        'opencl-amdgpu-pro': Package(
        ),
        'opencl-amdgpu-pro-icd': Package(
        ),
        'opencl-orca-amdgpu-pro-icd': Package(
        ),
        'roct-amdgpu-pro': Package(
        ),
        'vulkan-amdgpu': Package(
        ),
        'vulkan-amdgpu-pro': Package(
        ),
        'wayland-protocols-amdgpu': Package(
        ),
        'wsa-amdgpu': Package(
        ),
        'xserver-xorg-amdgpu-video-amdgpu': Package(
        ),
        'xserver-xorg-hwe-amdgpu-video-amdgpu': Package(
        ),
        # Not yet checked manually, and not yet checked for preinst/postinst/etc files
    }
    for key in pkgbuild_packages:
        pkgbuild_packages[key].name = key
    return pkgbuild_packages


# this maps which deb packages should go into specific arch package
# packages without mapping go into 'amdgpu-pro'
packages_map_default = 'amdgpu-pro'
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
    
    # Further is made by me (Ashark)
    # To make this list I used:
    # cat Packages | grep Package | cut -f2 -d " " > list_tmp # all presented debian packages
    # prev=""; for line in $(cat list_tmp); do if [[ $prev != $line ]]; then echo $line; else echo $line:i386; fi; prev=$line; done > list_tmp2 # rename 32bit debian packages
    # for line in $(cat list_tmp2); do str="'$line': "; if [[ $line != *"i386" ]]; then archpkg=$line; else archpkg="lib32-${line//:i386/}"; fi; if [[ $archpkg == *"-dev" ]]; then archpkg=${archpkg//-dev/}; fi; str="    $str '$archpkg',"; echo $str; done | column -t > list_tmp3 # stupid mapping
    # Then it's needed to carefully check pkgs mapping manually.
    
    'amdgpu':                                     'amdgpu',
    'amdgpu:i386':                                'lib32-amdgpu',
    'amdgpu-core':                                'amdgpu-core',
    'amdgpu-dkms':                                'amdgpu-dkms',
    'amdgpu-doc':                                 'amdgpu-doc',
    'amdgpu-hwe':                                 'amdgpu-hwe',
    'amdgpu-hwe:i386':                            'lib32-amdgpu-hwe',
    'amdgpu-lib':                                 'amdgpu-lib',
    'amdgpu-lib:i386':                            'lib32-amdgpu-lib',
    'amdgpu-lib-hwe':                             'amdgpu-lib-hwe',
    'amdgpu-lib-hwe:i386':                        'lib32-amdgpu-lib-hwe',
    'amdgpu-lib32':                               'amdgpu-lib32',
    'amdgpu-pro':                                 'amdgpu-pro',
    'amdgpu-pro:i386':                            'lib32-amdgpu-pro',
    'amdgpu-pro-core':                            'amdgpu-pro-core',
    'amdgpu-pro-hwe':                             'amdgpu-pro-hwe',
    'amdgpu-pro-hwe:i386':                        'lib32-amdgpu-pro-hwe',
    'amdgpu-pro-lib32':                           'amdgpu-pro-lib32',
    'amdgpu-pro-pin':                             'amdgpu-pro-pin',
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
    'libgl1-amdgpu-pro-ext':                      'libgl1-amdgpu-pro-ext',
    'libgl1-amdgpu-pro-ext:i386':                 'lib32-libgl1-amdgpu-pro-ext',
    'libgl1-amdgpu-pro-ext-hwe':                  'libgl1-amdgpu-pro-ext-hwe',
    'libgl1-amdgpu-pro-ext-hwe:i386':             'lib32-libgl1-amdgpu-pro-ext-hwe',
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
    'opencl-amdgpu-pro':                          'opencl-amdgpu-pro',
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
    'xserver-xorg-amdgpu-video-amdgpu':           'xserver-xorg-amdgpu-video-amdgpu',
    'xserver-xorg-amdgpu-video-amdgpu:i386':      'lib32-xserver-xorg-amdgpu-video-amdgpu',
    'xserver-xorg-hwe-amdgpu-video-amdgpu':       'xserver-xorg-hwe-amdgpu-video-amdgpu',
    'xserver-xorg-hwe-amdgpu-video-amdgpu:i386':  'lib32-xserver-xorg-hwe-amdgpu-video-amdgpu',
    # Not yet mapped manually
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
    "linux-firmware": "",
}

## maps debians archs to arch's archs
architectures_map = {
    "amd64": "x86_64",
    "i386": "i686",
    "all": "any"
}



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
# Maintainer: David McFarland <corngood@gmail.com>
# Autogenerated from AMD's Packages file

pkgbase=amdgpu-pro-installer
pkgname={package_names}
pkgver={pkgver}
pkgrel={pkgrel}
arch=('x86_64')
url='https://www.amd.com/en/support/kb/release-notes/rn-rad-lin-19-10-unified'
license=('custom:AMD')
makedepends=('wget')

DLAGENTS='{dlagents}'

major={pkgver_base}
minor={pkgver_build}

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
# $1: library dir
# $2: destination (optional)
move_libdir() {
    local libdir="usr/lib"
    if [ -n "$2" ]; then
        libdir="$2"
    fi
    if [ -d "$1" ]; then
        if [ -d "${pkgdir}/${libdir}" ]; then
            cp -ar -t "${pkgdir}/${libdir}/" "$1"/*
            rm -rf "$1"
        else
            mkdir -p "${pkgdir}/${libdir}"
            mv -t "${pkgdir}/${libdir}/" "$1"/*
            rmdir "$1"
        fi
    fi
}
"""

package_header_tpl = """
package_{NAME} () {{
    pkgdesc={DESC}
"""

package_deb_extract_tpl = """    extract_deb "${{srcdir}}"/amdgpu-pro-${{major}}-${{minor}}/{Filename}
"""

#package_header_i386 = """    move_libdir "${pkgdir}/opt/amdgpu-pro" "usr"
#    move_libdir "${pkgdir}/opt/amdgpu-pro/lib/i386-linux-gnu" "usr/lib32"
package_header_i386 = """
    move_libdir "${pkgdir}/lib" "usr/lib32"
"""

#package_header_x86_64 = """    move_libdir "${pkgdir}/opt/amdgpu-pro" "usr"
#    move_libdir "${pkgdir}/opt/amdgpu-pro/lib/x86_64-linux-gnu"
package_header_x86_64 = """
    move_libdir "${pkgdir}/lib"
"""

package_lib32_cleanup = """

    # lib32 cleanup
    rm -rf "${pkgdir}"/usr/{bin,lib,include,share} "${pkgdir}/var" "${pkgdir}"/opt/amdgpu-pro/{bin,include,share}
    rm -rf "${pkgdir}"/opt/amdgpu-pro/lib/xorg/modules/extensions/
"""

package_footer = """
}
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

    def add_deb(self, deb_info):
        self.deb_source_infos.append(deb_info)

        try:
            self.arch = [architectures_map[deb_info["Architecture"]], ]
        except:
            self.arch = default_arch

        if deb_info["Architecture"] == "i386":
            if self.name.startswith('lib32-'):
                self.arch = ['x86_64']
            else:
                import sys
                sys.stderr.write("ERROR: There is a bug in this script, package '%s' is i386 (came from %s) and should start with 'lib32'. Check packages_map!\n" % (self.name, deb_info["Package"]))


        try:
            deps = deb_info["Depends"].split(', ')
        except:
            deps = None

        domap = True
        #if self.name == "amdgpu-pro" or self.name == "lib32-amdgpu-pro":
            #domap = False

        if deps:
            deps = [ dependencyRE.match(dep).groups() for dep in deps ]
            deps = [(replace_deps[name] if name in replace_deps else name, version) for name, version in deps]
            deps = ["\"" + convertName(fix_32(name), deb_info, domap) + convertVersionSpecifier(fix_32(name), version) + "\"" for name, version in deps if name]
            deps = [ dep for dep in deps if not dep.startswith("\"=")]

            # remove all dependencies on itself
            deps = [ dep for dep in deps if dep[1:len(self.name)+1] != self.name ]

            if hasattr(self, 'depends') and self.depends:
                deps += self.depends

            self.depends = list(sorted(set( deps ))) # remove duplicates and append to already existing dependencies

            if not hasattr(self, 'desc'):
                desc = deb_info["Description"].split("\n")
                if len(desc) > 2:
                    desc = desc[0]
                else:
                    desc = " ".join(x.strip() for x in desc)

                if deb_info["Architecture"] == "i386":
                    desc += ' (32bit libraries)'

                self.desc = desc

    def toPKGBUILD(self):
        ret = package_header_tpl.format(
            NAME=self.name,
            DESC=quote(self.desc) if hasattr(self, 'desc') else quote("No description for package %s" % self.name),
        )

        if hasattr(self, 'install'):
            ret += "    install=%s\n" % self.install

        # add any given list/array with one of those names to the pkgbuild
        for array in ('arch', 'provides', 'conflicts', 'replaces', 'groups', 'optdepends'):
            if(hasattr(self, array)):
                ret += "    %s=('%s')\n" % (array, "' '".join(getattr(self, array)))

        if hasattr(self, 'depends'):
            ret += "    depends=(%s)\n\n" % " ".join(self.depends)

        for info in self.deb_source_infos:
            tmp_str=package_deb_extract_tpl.format(**info)
            ret += tmp_str.replace(str(pkgver_base), "${major}").replace(str(pkgver_build), "${minor}")

        if self.name.startswith('lib32-'):
            ret += package_header_i386
        else:
            ret += package_header_x86_64

        if hasattr(self, 'extra_commands'):
            ret += "\n\t# extra_commands:\n\t"
            ret += "\n\t".join( self.extra_commands )

        if self.name.startswith('lib32-'):
            ret += package_lib32_cleanup
        ret += package_footer
        return ret


pkgbuild_packages = gen_arch_packages()


# regex for parsing version information of a deb dependency
dependencyRE = re.compile(r"([^ ]+)(?: \((.+)\))?")

deb_archs={}

def convertName(name, info, domap=True):
    ret = name
    if info["Architecture"] == "i386" and (name not in deb_archs or "any" not in deb_archs[name]):
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
    if name in deb_package_names:
        return "=${major}.${minor}-${pkgrel}"
    if not spec:
        return ""

    sign, spec = spec.split(" ", 1)

    spec = spec.strip()
    if ":" in spec:
        whatever, spec = spec.rsplit(":", 1)
    return sign + spec

dep32RE = re.compile(r"(.*):i386")
def fix_32(dep):
    rdep = dep
    match = dep32RE.match(dep)
    if match:
        rdep = match.group(1)
        if not rdep in no_lib32_convert:
            rdep = 'lib32-%s' % rdep
    return rdep


def parse_Packages_file(f):
    global deb_package_names
    package_list=[]

    for deb_info in deb822.Packages.iter_paragraphs(f):
        if not deb_info["Package"] in deb_archs:
            deb_archs[deb_info["Package"]] = set()

        deb_archs[deb_info["Package"]].add(deb_info["Architecture"])
        package_list.append(deb_info)

    deb_package_names = [info["Package"] + ":i386" if info["Architecture"] == "i386" else info["Package"] for info in package_list]

    f.seek(0)

    for deb_info in package_list:
        name = deb_info["Package"]
        arch_pkg = pkgbuild_packages[ packages_map_default]
        if deb_info["Architecture"] == "i386":
            name = deb_info["Package"] + ":i386"
            arch_pkg = pkgbuild_packages["lib32-" + packages_map_default] # use lib32-<default-pkg> for 32bit packages as default package
        if name in packages_map:
            if packages_map[name] in pkgbuild_packages:
                arch_pkg = pkgbuild_packages[ packages_map[name]]
            else:
                arch_pkg = None

        if arch_pkg:
            arch_pkg.add_deb(deb_info)

    #    print(convertPackage(deb_info, package_names + optional_names))


# get list of unique arch packages from package map
arch_package_names=list(pkgbuild_packages.keys())
arch_package_names.sort()
deb_package_names=[]

print(header_tpl.format(
    package_names="(" + " ".join( arch_package_names ) + ")",
    pkgver=pkgver,
    pkgrel=pkgrel,
    dlagents=dlagents,
    pkgver_base=pkgver_base,
    pkgver_build=pkgver_build,
    source="\n\t".join(sources),
    sha256sums="\n\t".join(sha256sums)
))

print(package_functions)


with lzma.open(source_file, "r") as tar:
    with tarfile.open(fileobj=tar) as tf:
        with tf.extractfile("amdgpu-pro-%s-%s-ubuntu-18.04/Packages" %(pkgver_base,pkgver_build)) as packages:
            parse_Packages_file(packages)

for pkg in arch_package_names:
    print(pkgbuild_packages[pkg].toPKGBUILD())
