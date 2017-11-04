from debian import deb822
import re
import gzip
import lzma
import tarfile
import subprocess
import hashlib
import glob

pkgver_base = "17.30"
pkgver_build = "465504"
pkgrel = 3
debug_pkgext = False


pkgver = "{0}.{1}".format(pkgver_base, pkgver_build)
url_ref="https://support.amd.com/en-us/kb-articles/Pages/AMDGPU-PRO-Install.aspx"
dlagents="https::/usr/bin/wget --referer {0} -N %u".format(url_ref)

            # https://www2.ati.com/drivers/linux/ubuntu/amdgpu-pro-16.40-348864.tar.xz
source_url = "https://www2.ati.com/drivers/linux/ubuntu/amdgpu-pro-{0}-{1}.tar.xz".format(pkgver_base, pkgver_build)
source_file = "amdgpu-pro-{0}-{1}.tar.xz".format(pkgver_base, pkgver_build)

def gen_arch_packages():
	arch_packages = {
		'amdgpu-pro': Package(
			desc = "The AMDGPU Pro driver package",
			install = "amdgpu-pro-core.install",
			extra_commands = [
				"mv \"${pkgdir}\"/usr/lib/x86_64-linux-gnu/dri ${pkgdir}/usr/lib/",
				"# This is needed because libglx.so has a hardcoded DRI_DRIVER_PATH",
				"ln -s /usr/lib/dri ${pkgdir}/usr/lib/x86_64-linux-gnu/dri",
				'mkdir -p "${pkgdir}/etc/ld.so.conf.d/"',
				'echo "/opt/amdgpu-pro/lib/x86_64-linux-gnu/" > "${pkgdir}"/etc/ld.so.conf.d/amdgpu-pro.conf',
			]
		),

		'amdgpu-pro-dkms': Package(
			arch = ['any'],
			descr = "The AMDGPU Pro kernel module",
			extra_commands = [
				"msg 'Applying patches...'",
				"(cd ${{pkgdir}}/usr/src/amdgpu-pro-{0}-{1};".format(pkgver_base, pkgver_build),
				"\tsed -i 's/\/extra/\/extramodules/' dkms.conf",
				";\n".join(["\t\tmsg2 '{0}'\n\t\tpatch -p1 -i \"${{srcdir}}/{0}\"".format(patch) for patch in patches]),
				")",
				]
		),

		'amdgpu-pro-libgl': Package(
			desc = "The AMDGPU Pro libgl library symlinks",
			conflicts = ['libgl'],
			provides  = ['libgl'],
		),

		'amdgpu-pro-opencl': Package(
			desc = "The AMDGPU Pro OpenCL implementation",
			provides  = ['opencl-driver']
		),
		'amdgpu-pro-libdrm': Package(
			desc = "The AMDGPU Pro userspace interface to kernel DRM services",
			conflicts = ['libdrm'],
			provides = ['libdrm'],
		),

		'amdgpu-pro-vulkan': Package(
			desc = "The AMDGPU Pro Vulkan driver",
			provides = ['vulkan-driver'],
			extra_commands = [
				'mkdir -p "${pkgdir}"/usr/share/vulkan/icd.d/',
				'mv "${pkgdir}"/etc/vulkan/icd.d/amd_icd64.json "${pkgdir}"/usr/share/vulkan/icd.d/',
				'rm -rf "${pkgdir}"/etc/vulkan/'
			]
		),

		'amdgpu-pro-vdpau': Package(
			desc = "The AMDGPU Pro VDPAU driver",
			extra_commands = [
				'mkdir -p "${pkgdir}"/usr/lib/',
				'ln -s /opt/amdgpu-pro/lib/x86_64-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib/libvdpau_amdgpu.so.1.0.0',
				'ln -s /opt/amdgpu-pro/lib/x86_64-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib/libvdpau_amdgpu.so.1',
				'ln -s /opt/amdgpu-pro/lib/x86_64-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib/libvdpau_amdgpu.so',
			]
		),

		'amdgpu-pro-mesa-omx': Package(
			desc = "Mesa OpenMAX video drivers for AMDGPU Pro",
		),

		'amdgpu-pro-gst-omx': Package(
			desc = "GStreamer OpenMAX plugins for AMDGPU Pro",
		),

		'lib32-amdgpu-pro': Package(
			desk = "The AMDGPU Pro driver package (32bit libraries)",
			extra_commands = [
				'mkdir -p "${pkgdir}"/usr/lib32/',
				'mv "${pkgdir}"/usr/lib/i386-linux-gnu/dri "${pkgdir}"/usr/lib32/',

				'rm -rf "${pkgdir}"/etc',
				'mkdir -p "${pkgdir}/etc/ld.so.conf.d/"',
				'echo "/opt/amdgpu-pro/lib/i386-linux-gnu/" > "${pkgdir}"/etc/ld.so.conf.d/lib32-amdgpu-pro.conf'
			]
		),

		'lib32-amdgpu-pro-opencl': Package(
			desc = "The AMDGPU Pro OpenCL implementation",
			provides  = ['lib32-opencl-driver']
		),

		'lib32-amdgpu-pro-vulkan': Package(
			desc = "The AMDGPU Pro Vulkan driver (32bit libraries)",
			provides = ['lib32-vulkan-driver'],
			extra_commands = [
				'mkdir -p "${pkgdir}"/usr/share/vulkan/icd.d/',
				'mv "${pkgdir}"/etc/vulkan/icd.d/amd_icd32.json "${pkgdir}"/usr/share/vulkan/icd.d/',
				'rm -rf "${pkgdir}"/etc/vulkan/'
			]
		),

		'lib32-amdgpu-pro-libdrm': Package(
			desc = "The AMDGPU Pro userspace interface to kernel DRM services (32bit libraries)",
			conflicts = ['lib32-libdrm'],
			provides = ['lib32-libdrm'],
		),

		'lib32-amdgpu-pro-libgl': Package(
			desc = "The AMDGPU Pro libgl library symlinks (32bit libraries)",
			conflicts = ['lib32-libgl'],
			provides  = ['lib32-libgl'],
		),

		'lib32-amdgpu-pro-vdpau': Package(
			desc = "The AMDGPU Pro VDPAU driver (32bit libraries)",
			extra_commands = [
				'mkdir -p "${pkgdir}"/usr/lib32/',
				'ln -s /opt/amdgpu-pro/lib/i386-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib32/libvdpau_amdgpu.so.1.0.0',
				'ln -s /opt/amdgpu-pro/lib/i386-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib32/libvdpau_amdgpu.so.1',
				'ln -s /opt/amdgpu-pro/lib/i386-linux-gnu/vdpau/libvdpau_amdgpu.so.1.0.0 "${pkgdir}"/usr/lib32/libvdpau_amdgpu.so',
			]
		),

		'lib32-amdgpu-pro-mesa-omx': Package(
			desc = "Mesa OpenMAX video drivers for AMDGPU Pro (32bit libraries)",
		),

		'lib32-amdgpu-pro-gst-omx': Package(
			desc = "GStreamer OpenMAX plugins for AMDGPU Pro (32bit libraries)",
		),

		'xf86-video-amdgpu-pro': Package(
			desc = "The AMDGPU Pro X.org video driver",
			conflicts = ['xf86-video-amdgpu', 'xorg-server<1.19.0', 'X-ABI-VIDEODRV_VERSION<23', 'X-ABI-VIDEODRV_VERSION>=24'],
			provides  = ['xf86-video-amdgpu'], # in case anything depends on that
			groups = ['xorg-drivers'],
		)
	}
	for key in arch_packages:
		arch_packages[key].name = key
	return arch_packages


# this maps which deb packages should go into specific arch package
# packages without mapping go into 'amdgpu-pro'
packages_map_default = 'amdgpu-pro'
packages_map = {
	'amdgpu-pro':                       'amdgpu-pro',        # deb is metapackage
	'amdgpu-pro-core':                  'amdgpu-pro',        # deb is metapackage
	'libgbm1-amdgpu-pro':               'amdgpu-pro',
	'libgbm1-amdgpu-pro-base':          'amdgpu-pro',
	'libgbm1-amdgpu-pro-dev':           'amdgpu-pro',
	'ids-amdgpu-pro':                   'amdgpu-pro',

	'libllvm5.0-amdgpu-pro':            'amdgpu-pro',
	'llvm-amdgpu-pro-5.0-dev':          'amdgpu-pro',
	'llvm-amdgpu-pro-5.0':              'amdgpu-pro',
	'llvm-amdgpu-pro-5.0-runtime':      'amdgpu-pro',
	'llvm-amdgpu-pro-runtime':          'amdgpu-pro',
	'llvm-amdgpu-pro-dev':              'amdgpu-pro',

	'gst-omx-amdgpu-pro':               'amdgpu-pro-gst-omx',
	'mesa-amdgpu-pro-omx-drivers':      'amdgpu-pro-mesa-omx',

	'amdgpu-pro-dkms':                  'amdgpu-pro-dkms',

	'clinfo-amdgpu-pro':                'amdgpu-pro-opencl',
	'libopencl1-amdgpu-pro':            'amdgpu-pro-opencl',
	'opencl-amdgpu-pro-icd':            'amdgpu-pro-opencl',
	'rocm-amdgpu-pro':                  'amdgpu-pro-opencl',
	'rocm-amdgpu-pro-icd':              'amdgpu-pro-opencl',
	'rocm-amdgpu-pro-opencl':           'amdgpu-pro-opencl',
	'rocm-amdgpu-pro-opencl-dev':       'amdgpu-pro-opencl',
	'rocr-amdgpu-pro':                  'amdgpu-pro-opencl',
	'rocr-amdgpu-pro-dev':              'amdgpu-pro-opencl',
	'roct-amdgpu-pro':                  'amdgpu-pro-opencl',
	'roct-amdgpu-pro-dev':              'amdgpu-pro-opencl',
	'hsa-runtime-tools-amdgpu-pro':     'amdgpu-pro-opencl',
	'hsa-runtime-tools-amdgpu-pro-dev': 'amdgpu-pro-opencl',
	'hsa-ext-amdgpu-pro-finalize':      'amdgpu-pro-opencl',
	'hsa-ext-amdgpu-pro-image':         'amdgpu-pro-opencl',

	'vulkan-amdgpu-pro':                'amdgpu-pro-vulkan',

	'libdrm-amdgpu-pro-amdgpu1':        'amdgpu-pro-libdrm',
	'libdrm-amdgpu-pro-radeon1':        'amdgpu-pro-libdrm',
	'libdrm-amdgpu-pro-dev':            'amdgpu-pro-libdrm',
	'libdrm-amdgpu-pro-utils':          'amdgpu-pro-libdrm',
	'libdrm2-amdgpu-pro':               'amdgpu-pro-libdrm',

	# the following libs will be symlinked by amdgpu-pro-libgl, just like mesa-libgl and nvidia-libgl
	'libegl1-amdgpu-pro':               'amdgpu-pro-libgl',
	'libgl1-amdgpu-pro-appprofiles':    'amdgpu-pro-libgl',
	## contents of this should probably go into /usr/lib/xorg/modules/dri/ instead of /usr/lib/dri ?
	'libgl1-amdgpu-pro-dri':            'amdgpu-pro',
	'libgl1-amdgpu-pro-ext':            'amdgpu-pro-libgl',
	'libgl1-amdgpu-pro-glx':            'amdgpu-pro-libgl',
	'libgles2-amdgpu-pro':              'amdgpu-pro-libgl',
	'libglamor-amdgpu-pro-dev':         None, # disabled

	'libvdpau-amdgpu-pro':              'amdgpu-pro-vdpau',
	'xserver-xorg-video-amdgpu-pro':    'xf86-video-amdgpu-pro',
	'xserver-xorg-video-glamoregl-amdgpu-pro':    None,
	'xserver-xorg-video-modesetting-amdgpu-pro':    'xf86-video-amdgpu-pro',


	'lib32-amdgpu-pro':                 'lib32-amdgpu-pro', # deb is a metapackage
	'lib32-amdgpu-pro-lib32':           'lib32-amdgpu-pro', # deb is a metapackage
	'lib32-libgbm1-amdgpu-pro':         'lib32-amdgpu-pro',
	'lib32-libgbm1-amdgpu-pro-dev':     'lib32-amdgpu-pro',

	'lib32-gst-omx-amdgpu-pro':         'lib32-amdgpu-pro-gst-omx',
	'lib32-mesa-amdgpu-pro-omx-drivers':'lib32-amdgpu-pro-mesa-omx',

	'lib32-opencl-amdgpu-pro-icd':      'lib32-amdgpu-pro-opencl',
	'lib32-libopencl1-amdgpu-pro':      'lib32-amdgpu-pro-opencl',
	'lib32-rocm-amdgpu-pro':            'lib32-amdgpu-pro-opencl',
	'lib32-rocm-amdgpu-pro-icd':        'lib32-amdgpu-pro-opencl',
	'lib32-rocm-amdgpu-pro-opencl':     'lib32-amdgpu-pro-opencl',
	'lib32-rocm-amdgpu-pro-opencl-dev': 'lib32-amdgpu-pro-opencl',
	'lib32-rocr-amdgpu-pro':            'lib32-amdgpu-pro-opencl',
	'lib32-rocr-amdgpu-pro-dev':        'lib32-amdgpu-pro-opencl',
	'lib32-roct-amdgpu-pro':            'lib32-amdgpu-pro-opencl',
	'lib32-roct-amdgpu-pro-dev':        'lib32-amdgpu-pro-opencl',

	'lib32-vulkan-amdgpu-pro':          'lib32-amdgpu-pro-vulkan',

	'lib32-libdrm-amdgpu-pro-amdgpu1':  'lib32-amdgpu-pro-libdrm',
	'lib32-libdrm-amdgpu-pro-radeon1':  'lib32-amdgpu-pro-libdrm',
	'lib32-libdrm-amdgpu-pro-dev':      'lib32-amdgpu-pro-libdrm',
	'lib32-libdrm2-amdgpu-pro':         'lib32-amdgpu-pro-libdrm',


	'lib32-libegl1-amdgpu-pro':         'lib32-amdgpu-pro-libgl',
	'lib32-libgl1-amdgpu-pro-dri':      'lib32-amdgpu-pro',
	'lib32-libgl1-amdgpu-pro-ext':      'lib32-amdgpu-pro-libgl',
	'lib32-libgl1-amdgpu-pro-glx':      'lib32-amdgpu-pro-libgl',
	'lib32-libgles2-amdgpu-pro':        'lib32-amdgpu-pro-libgl',
	'lib32-libglamor-amdgpu-pro-dev':   None,

	'lib32-libvdpau-amdgpu-pro':        'lib32-amdgpu-pro-vdpau',

	# the following are not needed and should be discarded:
	'lib32-xserver-xorg-video-amdgpu-pro':              None,
	'lib32-xserver-xorg-video-glamoregl-amdgpu-pro':    None,
	'lib32-xserver-xorg-video-modesetting-amdgpu-pro':  None,
	'lib32-clinfo-amdgpu-pro': None,
	'lib32-libdrm-amdgpu-pro-utils': None,
}



## maps debian dependencies to arch dependencies
replace_deps = {
	"libc6":                None,
	"libgcc1":              None,
	"libstdc++6":           None,
	"libx11-6":             "libx11",
	"libx11-xcb1":          None,
	"libxcb-dri2-0":        "libxcb",
	"libxcb-dri3-0":        "libxcb",
	"libxcb-present0":      "libxcb",
	"libxcb-sync1":         "libxcb",
	"libxcb-glx0":          "libxcb",
	"libxcb1":              "libxcb",
	"libxext6":             "libxext",
	"libxshmfence1":        "libxshmfence",
	"libxdamage1":          "libxdamage",
	"libxfixes3":           "libxfixes",
	"libxxf86vm1":          "libxxf86vm",
	"libudev1":             "libsystemd",
	"libpciaccess0":        "libpciaccess",
	"libepoxy0":            "libepoxy",
	"libelf1":              None, # no lib32- package in Arch, just disabling for now
	"xserver-xorg-core":    "xorg-server",
	"libcunit1":            "bcunit",
	"libdrm-radeon1":       "libdrm",
	"amdgpu-pro-firmware":  "linux-firmware",
	"libssl1.0.0":          "openssl",
	"zlib1g":               "zlib",

	"libvdpau1": "libvdpau",
	"libtinfo5": "ncurses5-compat-libs",
	"libgstreamer1.0-0": "gstreamer",
	"libgstreamer-plugins-base1.0-0": "gst-plugins-base",
	"libglib2.0-0": "glib2",
	"libomxil-bellagio0": "libomxil-bellagio",

	#"libjs-jquery": "jquery",
	#"libjs-underscorea": "underscorejs" # the underscroejs AUR pkg dos not install to /usr/share/javascript !
	"libjs-jquery":       None,
	"libjs-underscorea":  None,
}

## override the version requirement extracted from deb
replace_version = {
	"linux-firmware": "",
}

## maps debians archs to arch's archs
arch_map = {
	"amd64": "x86_64",
	"i386": "i686",
	"all": "any"
}



subprocess.run(["wget", "--referer", url_ref, "-N", source_url])

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
url='http://www.amd.com'
license=('custom:AMD')
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

package_deb_extract_tpl = """	extract_deb "${{srcdir}}"/amdgpu-pro-%s-%s/{Filename}
""" %(pkgver_base,pkgver_build)

#package_header_i386 = """	move_libdir "${pkgdir}/opt/amdgpu-pro" "usr"
#	move_libdir "${pkgdir}/opt/amdgpu-pro/lib/i386-linux-gnu" "usr/lib32"
package_header_i386 = """
	move_libdir "${pkgdir}/lib" "usr/lib32"
"""

#package_header_x86_64 = """	move_libdir "${pkgdir}/opt/amdgpu-pro" "usr"
#	move_libdir "${pkgdir}/opt/amdgpu-pro/lib/x86_64-linux-gnu"
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

	def add_deb(self, info):
		self.deb_source_infos.append(info)

		try:
			self.arch = [ arch_map[info["Architecture"]], ]
		except:
			self.arch = default_arch

		if info["Architecture"] == "i386":
			if self.name.startswith('lib32-'):
				self.arch = ['x86_64']
			else:
				import sys
				sys.stderr.write("ERROR: There is a bug in this script, package '%s' is i386 (came from %s) and should start with 'lib32'. Check packages_map!\n" % (self.name,info["Package"]))


		try:
			deps = info["Depends"].split(', ')
		except:
			deps = None

		domap = True
		if self.name == "amdgpu-pro" or self.name == "lib32-amdgpu-pro":
			domap = False

		if deps:
			deps = [ dependencyRE.match(dep).groups() for dep in deps ]
			deps = [(replace_deps[name] if name in replace_deps else name, version) for name, version in deps]
			deps = ["'" + convertName(fix_32(name), info, domap) + convertVersionSpecifier(fix_32(name), version) + "'" for name, version in deps if name]
			deps = [ dep for dep in deps if not dep.startswith("'=")]

			# remove all dependencies on itself
			deps = [ dep for dep in deps if dep[1:len(self.name)+1] != self.name ]

			if hasattr(self, 'depends') and self.depends:
				deps += self.depends

			self.depends = list(sorted(set( deps ))) # remove duplicates and append to already existing dependencies

			if not hasattr(self, 'desc'):
				desc = info["Description"].split("\n")
				if len(desc) > 2:
					desc = desc[0]
				else:
					desc = " ".join(x.strip() for x in desc)

				if info["Architecture"] == "i386":
					desc += ' (32bit libraries)'

				self.desc = desc

	def toPKGBUILD(self):
		ret = package_header_tpl.format(
			NAME=self.name,
			DESC=quote(self.desc) if hasattr(self, 'desc') else quote("No description for package %s" % self.name),
		)

		if hasattr(self, 'install'):
			ret += "	install=%s\n" % self.install

		# add any given list/array with one of those names to the pkgbuild
		for array in ('arch', 'provides', 'conflicts', 'replaces', 'groups', 'optdepends'):
			if(hasattr(self, array)):
				ret += "	%s=('%s')\n" % (array, "' '".join(getattr(self, array)))

		if hasattr(self, 'depends'):
			ret += "	depends=(%s)\n\n" % " ".join(self.depends)

		for info in self.deb_source_infos:
			ret += package_deb_extract_tpl.format(**info)

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


arch_packages = gen_arch_packages()


# regex for parsing version information of a deb dependency
dependencyRE = re.compile(r"([^ ]+)(?: \((.+)\))?")

deb_archs={}

def convertName(name, info, domap=True):
	ret = name
	if info["Architecture"] == "i386" and (name not in deb_archs or "any" not in deb_archs[name]):
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
		return "=" + pkgver + "-" + str(pkgrel)
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
		rdep = 'lib32-%s' % rdep
	return rdep


def writePackages(f):
	global deb_package_names
	package_list=[]

	for info in deb822.Packages.iter_paragraphs(f):
		if not info["Package"] in deb_archs:
			deb_archs[info["Package"]] = set()

		deb_archs[info["Package"]].add(info["Architecture"])
		package_list.append(info)

	deb_package_names = ["lib32-" + info["Package"] if info["Architecture"] == "i386" else info["Package"] for info in package_list]

	f.seek(0)

	for info in package_list:
		name = info["Package"]
		arch_pkg = arch_packages[ packages_map_default ]
		if info["Architecture"] == "i386":
			name = "lib32-" + info["Package"]
			arch_pkg = arch_packages[ "lib32-" + packages_map_default ] # use lib32-<default-pkg> for 32bit packages as default package
		if name in packages_map:
			if packages_map[name] in arch_packages:
				arch_pkg = arch_packages[ packages_map[name] ]
			else:
				arch_pkg = None

		if arch_pkg:
			arch_pkg.add_deb(info)

	#	print(convertPackage(info, package_names + optional_names))


# get list of unique arch packages from package map
arch_package_names=list(arch_packages.keys())
arch_package_names.sort()
deb_package_names=[]

print(header_tpl.format(
	package_names="(" + " ".join( arch_package_names ) + ")",
	pkgver=pkgver,
	pkgrel=pkgrel,
	dlagents=dlagents,
	source="\n\t".join(sources),
	sha256sums="\n\t".join(sha256sums)
))

print(package_functions)


with lzma.open(source_file, "r") as tar:
	with tarfile.open(fileobj=tar) as tf:
		with tf.extractfile("amdgpu-pro-%s-%s/Packages" %(pkgver_base,pkgver_build)) as packages:
			writePackages(packages)

for pkg in arch_package_names:
	print( arch_packages[pkg].toPKGBUILD() )
