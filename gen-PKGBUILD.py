#!/usr/bin/env python3

from debian import deb822
from debian import debfile
import re
import hashlib
import glob
from pathlib import Path
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader
import os.path

spec = spec_from_loader("versions", SourceFileLoader("versions", "versions"))
versions = module_from_spec(spec)
spec.loader.exec_module(versions)

pkgver_base = versions.pkgver_base
pkgver_build = versions.pkgver_build
ubuntu_ver = versions.ubuntu_ver
pkgrel = 1

debugging = False

debug_pkgext = True if debugging else False

url_ref = "https://www.amd.com/en/support/kb/release-notes/rn-amdgpu-unified-linux-22-20"
dlagents = "https::/usr/bin/wget --referer {0} -N %u".format(url_ref)
# TODO: remove dlagents?

source_repo_url = "http://repo.radeon.com/amdgpu/{0}/ubuntu/".format(pkgver_base)

def gen_arch_packages():
    pkgbuild_packages = {

        # Further is made by me (Ashark)
        # To make a more human readable Packages file I used this:
        # cat Packages | grep -vE "Filename|Size|MD5sum|SHA1|SHA256|Priority|Maintainer|Version: 19.20" >  Packages-short

        # To generate pkgbuild_packages template I used:
        # bash make_pkgbuild_pkgs_template.sh > tmp_pkgbuild_pkgs_template.txt

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

        'amf-amdgpu-pro': Package(),
        # 'libdrm-amdgpu': Package(
        #     provides = ['libdrm'],
        #     extra_commands = [
        #         # This applies to libdrm2-amdgpu
        #         "mv ${pkgdir}/lib/* ${pkgdir}/usr/lib",
        #         "rmdir ${pkgdir}/lib"
        #     ],
        # ),
        # 'lib32-libdrm-amdgpu': Package(
        #     provides=['lib32-libdrm'],
        #     extra_commands = [
        #         # This applies to libdrm2-amdgpu:i386
        #         "mv ${pkgdir}/lib ${pkgdir}/usr"
        #     ],
        # ),
        'amdgpu-pro-libgl': Package(
            desc = "AMDGPU Pro OpenGL driver",
            provides  = ['libgl'],
            extra_commands = [
            #     # This is instead of libgl1-amdgpu-pro-ext-hwe_19.20-812932_amd64.deb/postinst and libgl1-amdgpu-pro-ext-hwe_19.20-812932_amd64.deb/prerm
            #     'mv "${pkgdir}"/opt/amdgpu-pro/lib/xorg/modules/extensions/libglx-ext-hwe.so "${pkgdir}"/opt/amdgpu-pro/lib/xorg/modules/extensions/libglx.so',
                'move_libdir "usr/lib/x86_64-linux-gnu" "usr/lib"',
                'move_libdir "opt/amdgpu-pro/lib/x86_64-linux-gnu" "usr/lib/amdgpu-pro"',
                'move_libdir "opt/amdgpu-pro/lib/xorg" "usr/lib/amdgpu-pro/xorg"',
                'move_libdir "opt/amdgpu/share/drirc.d" "usr/share/drirc.d"',
                'sed -i "s|/opt/amdgpu-pro/lib/x86_64-linux-gnu|#/usr/lib/amdgpu-pro  # commented to prevent problems of booting with amdgpu-pro, use progl script|" "${pkgdir}"/etc/ld.so.conf.d/10-amdgpu-pro-x86_64.conf',

                'install -Dm755 "${srcdir}"/progl "${pkgdir}"/usr/bin/progl',
                'install -Dm755 "${srcdir}"/progl.bash-completion "${pkgdir}"/usr/share/bash-completion/completions/progl',

                '# For some reason, applications started with normal OpenGL (i.e. without ag pro) crashes at launch if this conf file is presented, so hide it for now, until I find out the reason of that.',
                'mv "${pkgdir}"/usr/share/drirc.d/10-amdgpu-pro.conf "${pkgdir}"/usr/share/drirc.d/10-amdgpu-pro.conf.hide',
            ]
        ),
        'lib32-amdgpu-pro-libgl': Package(
            desc = "AMDGPU Pro OpenGL driver (32-bit)",
            provides=['lib32-libgl'],
            extra_commands=[
                # # This is instead of libgl1-amdgpu-pro-ext-hwe_19.20-812932_i386.deb/postinst and libgl1-amdgpu-pro-ext-hwe_19.20-812932_i386.deb/prerm
                # 'mv "${pkgdir}"/opt/amdgpu-pro/lib/xorg/modules/extensions/libglx-ext-hwe.so "${pkgdir}"/opt/amdgpu-pro/lib/xorg/modules/extensions/libglx.so',
                # Clean-up duplicated files to be able to install simultaneously with 64bit version
                'rm "${pkgdir}"/etc/amd/amdrc "${pkgdir}"/opt/amdgpu-pro/lib/xorg/modules/extensions/libglx.so "${pkgdir}"/opt/amdgpu/share/drirc.d/10-amdgpu-pro.conf',

                'move_libdir "usr/lib/i386-linux-gnu" "usr/lib32"',
                'move_libdir "opt/amdgpu-pro/lib/i386-linux-gnu" "usr/lib32/amdgpu-pro"',
                'sed -i "s|/opt/amdgpu-pro/lib/i386-linux-gnu|#/usr/lib32/amdgpu-pro  # commented to prevent problems of booting with amdgpu-pro, use progl32 script|" "${pkgdir}"/etc/ld.so.conf.d/10-amdgpu-pro-i386.conf',
            ]
        ),
        #'opencl-amdgpu-pro-comgr': Package( desc = "Code object manager (COMGR)" ),
        #'opencl-amdgpu-pro-dev': Package(  ),
        #'opencl-amdgpu-pro-pal': Package(
            #desc = "AMDGPU Pro OpenCL driver PAL",
            #provides=['opencl-driver']
        #),
        #'opencl-amdgpu-pro-orca': Package(
            #desc = "AMDGPU Pro OpenCL driver ORCA aka legacy",
            #provides=['opencl-driver']
        #),
        #'lib32-opencl-amdgpu-pro-orca': Package(
            #desc="AMDGPU Pro OpenCL driver ORCA aka legacy (32-bit)",
            #provides=['lib32-opencl-driver']
        #),
        'vulkan-amdgpu-pro': Package(
            provides=['vulkan-driver'],
            extra_commands = [
                # This is instead of vulkan-amdgpu-pro_19.20-812932_amd64.deb/postinst and vulkan-amdgpu-pro_19.20-812932_amd64.deb/prerm
                'mkdir -p "${pkgdir}"/usr/share/vulkan/icd.d/',
                'mv "${pkgdir}"/opt/amdgpu-pro/etc/vulkan/icd.d/amd_icd64.json "${pkgdir}"/usr/share/vulkan/icd.d/amd_pro_icd64.json',
                'mv "${pkgdir}"/usr/lib/amdvlk64.so "${pkgdir}"/usr/lib/amdvlkpro64.so',
                'sed -i "s#/opt/amdgpu-pro/lib/x86_64-linux-gnu/amdvlk64.so#/usr/lib/amdvlkpro64.so#" "${pkgdir}"/usr/share/vulkan/icd.d/amd_pro_icd64.json',
                'find ${pkgdir} -type d -empty -delete',
            ]
        ),
        'lib32-vulkan-amdgpu-pro': Package(
            provides=['lib32-vulkan-driver'],
            extra_commands = [
                # This is instead of vulkan-amdgpu-pro_19.20-812932_i386.deb/postinst and vulkan-amdgpu-pro_19.20-812932_i386.deb/prerm
                'mkdir -p "${pkgdir}"/usr/share/vulkan/icd.d/',
                'mv "${pkgdir}"/opt/amdgpu-pro/etc/vulkan/icd.d/amd_icd32.json "${pkgdir}"/usr/share/vulkan/icd.d/amd_pro_icd32.json',
                'mv "${pkgdir}"/usr/lib32/amdvlk32.so "${pkgdir}"/usr/lib32/amdvlkpro32.so',
                'sed -i "s#/opt/amdgpu-pro/lib/i386-linux-gnu/amdvlk32.so#/usr/lib32/amdvlkpro32.so#" "${pkgdir}"/usr/share/vulkan/icd.d/amd_pro_icd32.json',
                'find ${pkgdir} -type d -empty -delete',
            ]
        ),

    }
    for key in pkgbuild_packages:
        pkgbuild_packages[key].arch_pkg_name = key
    return pkgbuild_packages


# This maps which deb packages should go into specific arch package
from packages_map import packages_map

# This maps debian dependencies to arch linux dependencies
from replace_deps import replace_deps

# Almost every pro package depends on these two, but I omited them (hoping they are not needed, but not tested), so disabling these dependencies globally
replace_deps['libwayland-amdgpu-client0'] = None
replace_deps['libwayland-amdgpu-server0'] = None

## do not convert the dependencies listed to lib32 variants
no_lib32_convert = [
    # "some_debian_package_name",
]

## override the version requirement extracted from deb
replace_version = {
    # "some-debian-package-name": "=redefinedVersion",
}

## maps debians archs to arch's archs
architectures_map = {
    "amd64": "x86_64",
    "i386": "i686",
    "all": "any"
}

# To see list of uniq licences files and packages that uses them, I used this:
    # cd unpacked_debs
    # for dir in $(ls -d *); do
    #     md5sum $dir/copyright
    # done | sort
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
    "0edd336396b019512b94c98b0240ea77": "custom: AMDGPU-PRO EULA",
    "f2b0e0926d102efc9a09f8b9a740209d": "GPL2",
}

# To see list of suggested and recommended packages:
# cat Packages-extracted | egrep "Suggest|Recommends" | sort -u
optdepends_descriptions = {
    "libegl1-amdgpu-mesa-drivers":   "TODO_some_description",
    "libgl1-amdgpu-mesa-dri":        "TODO_some_description",
    "libgl1-amdgpu-pro-dri":         "TODO_some_description",
    "libtxc-dxtn-s2tc0":             "TODO_some_description",
    "llvm-amdgpu-7.1-dev":           "TODO_some_description",
    "libglide3":                     "TODO_some_description",
    "linux-firmware":                "TODO_some_description",
    "llvm-amdgpu-7.1-doc":           "TODO_some_description",
}


def hashFile(file):
    block = 64 * 1024
    hash = hashlib.sha256()
    with open(file, 'rb') as f:
        buf = f.read(block)
        while len(buf) > 0:
            hash.update(buf)
            buf = f.read(block)
    return hash.hexdigest()

sources = [ "progl", "progl.bash-completion" ]
sha256sums = [ hashFile("progl"), hashFile("progl.bash-completion") ]

patches = sorted(glob.glob("*.patch"))

for patch in patches:
    sources.append(patch)
    sha256sums.append(hashFile(patch))

#sources.append("20-amdgpu.conf")
#sha256sums.append(hashFile("20-amdgpu.conf"))


header_tpl = """# Author: Janusz Lewandowski <lew21@xtreeme.org>
# Contributor: David McFarland <corngood@gmail.com>
# Maintainer: Andrew Shark <ashark @at@ linuxcomp.ru>
# Autogenerated from AMD's Packages file
# with https://github.com/Ashark/archlinux-amdgpu-pro/blob/master/gen-PKGBUILD.py

major={pkgver_base}
minor={pkgver_build}
ubuntu_ver={ubuntu_ver}

pkgbase=amdgpu-pro-installer
pkgname={package_names}
pkgver=${{major}}_${{minor}}
pkgrel={pkgrel}
arch=('x86_64')
url={url}
license=('custom: multiple')
groups=('Radeon_Software_for_Linux')
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
move_copyright() {
    find ${pkgdir}/usr/share/doc -name "changelog.Debian.gz" -delete
    mkdir -p ${pkgdir}/usr/share/licenses/${pkgname}
    find ${pkgdir}/usr/share/doc -name "copyright" -exec mv {} ${pkgdir}/usr/share/licenses/${pkgname} \;
    find ${pkgdir}/usr/share/doc -type d -empty -delete
}
"""

package_header_tpl = """package_{NAME} () {{
    pkgdesc={DESC}
"""

package_deb_extract_tpl = """    extract_deb "${{srcdir}}"/{BaseFilename}
"""

package_move_libdir_tpl = """    move_libdir "opt/amdgpu{PRO}/lib/{DEBDIR}-linux-gnu" "usr/lib{ARCHDIR}"
"""

package_move_copyright = """    move_copyright
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

        # Removing unneeded dependencies
        # if self.arch_pkg_name == "amdgpu-pro-meta" or self.arch_pkg_name == "lib32-amdgpu-pro-meta":
        #     # Removes dependency on many open components, which are provided by standard arch repos
        #     deb_deps.remove('amdgpu-hwe (= %s-%s)' % (pkgver_base, pkgver_build))  # for hwe releases
        #     # deb_deps.remove('amdgpu (= %s-%s)' % (pkgver_base, pkgver_build)) # for non-hwe releases, i.e. LTS release with xx.xx.0 version
        # if self.arch_pkg_name == "amdgpu-pro-lib32-meta":
        #     deb_deps.remove('amdgpu (= %s-%s) | amdgpu-hwe (= %s-%s)' % (pkgver_base, pkgver_build, pkgver_base, pkgver_build))
        #     deb_deps.remove('amdgpu-lib32 (= %s-%s)' % (pkgver_base, pkgver_build))
        if self.arch_pkg_name == "opencl-amdgpu-pro-dev":
            deb_deps.remove('ocl-icd-libopencl1-amdgpu-pro (= %s-%s)' % (pkgver_base, pkgver_build))
        if self.arch_pkg_name == "opencl-amdgpu-pro-meta":
            deb_deps.remove('amdgpu-dkms (= %s-%s)' % (pkgver_base, pkgver_build)) # I do not know why it wants amdgpu-dkms, but I did not built it, so just rm this dep for now
            deb_deps.remove('clinfo-amdgpu-pro (= %s-%s)' % (pkgver_base, pkgver_build))
            deb_deps.remove('ocl-icd-libopencl1-amdgpu-pro (= %s-%s)' % (pkgver_base, pkgver_build))
        #if self.arch_pkg_name == "amf-amdgpu-pro":
            #deb_deps.remove('opencl-amdgpu-pro-icd') # looks like amf works ok even without opencl part
        # if self.arch_pkg_name == "vulkan-amdgpu-pro":
        #     deb_deps.remove('amdgpu-pro-core')  # already removed, as I dropped ag-core-meta
        # if self.arch_pkg_name == "lib32-vulkan-amdgpu-pro":
        #     deb_deps.remove('amdgpu-pro-core')  # already removed, as I dropped ag-core-meta

        if deb_deps:
            deb_deps = [ depWithAlt_to_singleDep(dep) if dependencyWithAltRE.search(dep) else dep for dep in deb_deps ]
            deb_deps = [ dependencyNameWithVersionRE.match(dep).groups() for dep in deb_deps ]
            deb_deps = [(replace_deps[deb_pkg_name] if deb_pkg_name in replace_deps else deb_pkg_name, version) for deb_pkg_name, version in deb_deps]
            deb_deps = ["\"" + convertName(deb_pkg_name, deb_info, domap) + convertVersionSpecifier(deb_pkg_name, version) + "\"" for deb_pkg_name, version in deb_deps if deb_pkg_name]
            deb_deps = [ dep for dep in deb_deps if dep != "\"\"" ]
            deb_deps = [ dep for dep in deb_deps if not dep.startswith("\"=")]

            # if self.arch_pkg_name == "opencl-amdgpu-pro-orca":
            #     deb_deps.append('\"libdrm-amdgpu=${major}_${minor}-${pkgrel}\"')
            # if self.arch_pkg_name == "lib32-opencl-amdgpu-pro-orca":
            #     deb_deps.append('\"lib32-libdrm-amdgpu=${major}_${minor}-${pkgrel}\"')
            # # I am not sure if it is needed for pal variant, but just to be safe:
            # if self.arch_pkg_name == "opencl-amdgpu-pro-pal":
            #     deb_deps.append('\"libdrm-amdgpu=${major}_${minor}-${pkgrel}\"')

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

        if deb_optdeps:
            deb_optdeps = [depWithAlt_to_singleDep(dep) if dependencyWithAltRE.search(dep) else dep for dep in deb_optdeps]
            deb_optdeps = [dependencyNameWithVersionRE.match(dep).groups() for dep in deb_optdeps]
            deb_optdeps = [(replace_deps[deb_pkg_name] if deb_pkg_name in replace_deps else deb_pkg_name, version) for deb_pkg_name, version in deb_optdeps]
            deb_optdeps = ["\"" + convertName(deb_pkg_name, deb_info, domap) + convertVersionSpecifier(deb_pkg_name, version) + ": "
                           + (optdepends_descriptions[deb_pkg_name] if deb_pkg_name in optdepends_descriptions else "Warning unspecified optdep description" )
                           + "\"" for deb_pkg_name, version in deb_optdeps if deb_pkg_name]

        # remove all optional dependencies on itself
        deb_optdeps = [dep for dep in deb_optdeps if dep[1:len(self.arch_pkg_name) + 1] != self.arch_pkg_name]

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

        sources.append(source_repo_url.replace(pkgver_base,"${major}") + deb_info["Filename"].replace(pkgver_base,"${major}").replace(pkgver_build,"${minor}"))
        sha256sums.append(deb_info["SHA256"])

        deb_file = debfile.DebFile(os.path.expanduser("~/.aptly/public/%s" % (deb_info["Filename"])))

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

        if hasattr(self, 'license'):
            ret += "    license=%s\n" % self.license
        if hasattr(self, 'install'):
            ret += "    install=%s\n" % self.install

        if hasattr(self, 'arch'):
            if self.arch != default_arch: # omitting default arch for making pkgbuild cleaner
                ret += "    arch=('%s')\n" % " ".join(self.arch)

        # add any given list/array with one of those names to the pkgbuild
        for array in ('provides', 'conflicts', 'replaces', 'groups'):
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
            tmp_str=package_deb_extract_tpl.format(BaseFilename=os.path.basename(info["Filename"]))
            ret += tmp_str.replace(str(pkgver_base), "${major}").replace(str(pkgver_build), "${minor}")

        if self.arch_pkg_name != "amdgpu-pro-libgl" and self.arch_pkg_name != "lib32-amdgpu-pro-libgl":
            # for ag-p-lgl and l32-ag-p-lgl I have temporary disabled movelibdir function (because it requires further investigation)

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
            ret += "\n"

        # if self.arch_pkg_name.startswith('lib32-'):
        #     ret += package_lib32_cleanup
        ret += package_footer
        return ret


pkgbuild_packages = gen_arch_packages()


# regex for parsing version information of a deb dependency
dependencyNameWithVersionRE = re.compile(r"([^ ]+)(?: \((.+)\))?")

# regex for detecting dependency with alternative
dependencyWithAltRE = re.compile(r" \| ")

def depWithAlt_to_singleDep(depWithAlt):
    # I (Ashark) used this to get a list of dependencies with alternatives:
    # cat Packages | grep -vE "Filename|Size|MD5sum|SHA1|SHA256|Priority|Maintainer|Version|Description|^ +" >  Packages-short-nodesc
    # cat Packages-short-nodesc | egrep "Depends|Suggests|Recommends" | grep "|" | sed 's/Depends: //' | sed 's/Suggests: //' | sed 's/Recommends: //' | sed "s/, /\n/g" | grep "|" | sort -u
    # And I got this list:
        # amdgpu (= 19.20-812932) | amdgpu-hwe (= 19.20-812932)
        # amdgpu-lib (= 19.20-812932) | amdgpu-lib-hwe (= 19.20-812932)
        # amdgpu-pro (= 19.20-812932) | amdgpu-pro-hwe (= 19.20-812932)
        # libtxc-dxtn-s2tc0 | libtxc-dxtn0
        # libudev1 | libudev0
        # libva1-amdgpu | libva2-amdgpu | libva1 | libva2
        # libvdpau1-amdgpu | libvdpau1

    splitted_alts = dependencyWithAltRE.split(depWithAlt)
    splitted_name_and_ver = [dependencyNameWithVersionRE.match(dep).groups() for dep in splitted_alts]

    if splitted_name_and_ver[0][0] + "-hwe" == splitted_name_and_ver[1][0]:
        return splitted_alts[1] # use hwe variant (i.e. latest)
    if splitted_name_and_ver[0][0] == "libtxc-dxtn-s2tc0" and splitted_name_and_ver[1][0] == "libtxc-dxtn0": # from libgl1-amdgpu-mesa-dri Recommends array
        return splitted_alts[0] # use libtxc-dxtn-s2tc0. libtxc-dxtn0 is a virtual package, which is provided by libtxc-dxtn-s2tc0
    if splitted_name_and_ver[0][0] == "libudev1" and splitted_name_and_ver[1][0] == "libudev0":
        return splitted_alts[0] # use libudev1 (i.e. latest)
    if splitted_name_and_ver[0][0] == "libva1-amdgpu" and splitted_name_and_ver[1][0] == "libva2-amdgpu" and splitted_name_and_ver[2][0] == "libva1" and splitted_name_and_ver[3][0] == "libva2":
        return splitted_alts[3] # use libva2. libva*-amdgpu doesn't exist in repos and not provided in bundle. Probably amd's mistake
    if splitted_name_and_ver[0][0] == "libvdpau1-amdgpu" and splitted_name_and_ver[1][0] == "libvdpau1":
        return splitted_alts[1] # use libvdpau1. libvdpau1-amdgpu doesn't exist in repos and not provided in bundle. Probably amd's mistake

    return "Warning_Do_not_know_which_alt_to_choose"

deb_pkgs_avail_archs={}

dep32RE = re.compile(r"(.*):i386")
def convertName(name, deb_info, domap=True):
    ret = name
    match = dep32RE.match(name)
    if match: # explicit :i386 dependency
        ret = match.group(1)
        if not ret in no_lib32_convert:
            ret = 'lib32-%s' % ret

    if deb_info["Architecture"] == "i386" and (name not in deb_pkgs_avail_archs or "all" not in deb_pkgs_avail_archs[name]):
        if not name in no_lib32_convert:
            ret = "lib32-" + name

    unambiguous_name = name
    if deb_info["Architecture"] == "i386":
        unambiguous_name = name + ":i386"

    if unambiguous_name in packages_map:
        if domap:
            if packages_map[unambiguous_name]: # this is to prevent returning None type, because we want to concatenate with str type
                return packages_map[unambiguous_name]
            return ""
        return ""

    if ret in packages_map:
        if packages_map[ret]:  # this is to prevent returning None type, because we want to concatenate with str type
            return packages_map[ret]
        return ""
    return ret

def convertVersionSpecifier(name, spec):
    if name in replace_version:
        return replace_version[name]

    if name in deb_package_names:
        # Different pkgver is not supported for split packages, see here: https://bbs.archlinux.org/viewtopic.php?id=246815
        # So we use the same pkgver for all split packages.
        return "=${major}_${minor}-${pkgrel}"

    if not spec:
        return ""

    sign, spec = spec.split(" ", 1)
    spec = spec.strip()

    if sign == ">" or sign == ">=": # assume Arch users have latest versions of all packages
        return ""

    if ":" in spec: # debian epochs means nothing in arch context, so strip them
        deb_epoch, spec = spec.rsplit(":", 1)
        # also would be good to omit debian-revision, as it has nothing to do with arch's pkgrel
        # but anyway we omit > and >= deps, so I did not implemented it yet
        return sign + spec

# get list of unique arch packages from package map
arch_package_names=list(pkgbuild_packages.keys())
deb_package_names=[]

# f = open("Packages-debugging", "r")
f = open("Packages-extracted", "r")

deb_package_list = []

for deb_info in deb822.Packages.iter_paragraphs(f):
    if not deb_info["Package"] in deb_pkgs_avail_archs:
        deb_pkgs_avail_archs[deb_info["Package"]] = set()

    deb_pkgs_avail_archs[deb_info["Package"]].add(deb_info["Architecture"])
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

if not debugging:
    print(header_tpl.format(
        package_names="(\n" + "\n".join( arch_package_names ) + "\n)",
        pkgrel=pkgrel,
        url=url_ref,
        dlagents=dlagents,
        pkgver_base=pkgver_base,
        pkgver_build=pkgver_build,
        ubuntu_ver=ubuntu_ver,
        source="\n\t".join(sources),
        sha256sums="\n\t".join(sha256sums)
    ))

    print(package_functions)

for pkg in arch_package_names:
    print(pkgbuild_packages[pkg].toPKGBUILD())
