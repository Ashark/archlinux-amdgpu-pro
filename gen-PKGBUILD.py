from debian import deb822
import re
import gzip
import lzma
import tarfile
import subprocess
import hashlib
import glob

pkgver_base = "16.30.3"
pkgver_build = "315407"
pkgrel = 2

pkgver = "{0}.{1}".format(pkgver_base, pkgver_build)
url_ref="http://support.amd.com/en-us/kb-articles/Pages/AMDGPU-PRO-Beta-Driver-for-Vulkan-Release-Notes.aspx"
dlagents="https::/usr/bin/wget --referer {0} -N %u".format(url_ref)

source_url = "https://www2.ati.com/drivers/linux/amdgpu-pro_{0}-{1}.tar.xz".format(pkgver_base, pkgver_build)

def gen_arch_packages():
	arch_packages = {
		'amdgpu-pro': Package(
			desc = "The AMDGPU Pro driver package",
			install = "amdgpu-pro-core.install",
			extra_commands = [
				"sed -i 's@/usr/lib/x86_64-linux-gnu/@/usr/lib/@' ${pkgdir}/usr/lib/amdgpu-pro/ld.conf",
				"sed -i 's@/usr/lib/i386-linux-gnu/@/usr/lib32/@' ${pkgdir}/usr/lib/amdgpu-pro/ld.conf",
				"mkdir -p ${pkgdir}/etc/ld.so.conf.d/",
				"ln -s /usr/lib/amdgpu-pro/ld.conf ${pkgdir}/etc/ld.so.conf.d/10-amdgpu-pro.conf",
				"mkdir -p ${pkgdir}/etc/modprobe.d/",
				"ln -s /usr/lib/amdgpu-pro/modprobe.conf ${pkgdir}/etc/modprobe.d/amdgpu-pro.conf",
			]
		),

		'amdgpu-pro-dkms': Package(
			arch = ['any'],
			descr = "The AMDGPU Pro kernel module",
			extra_commands = [
				"(cd ${{pkgdir}}/usr/src/amdgpu-pro-{0}-{1};".format(pkgver_base, pkgver_build),
				"\tsed -i 's/\/extra/\/extramodules/' dkms.conf",
				";\n".join(["\t\tpatch -p1 -i \"${{srcdir}}/{0}\"".format(patch) for patch in patches]),
				")",
				]
		),

		'amdgpu-pro-firmware': Package(
			desc = "The AMDGPU Pro firmware files for amdgpu cards.",
			extra_commands = [
				"mv ${pkgdir}/usr/lib/firmware ${pkgdir}/usr/lib/firmware.tmp",
				"mkdir -p ${pkgdir}/usr/lib/firmware",
				"mv ${pkgdir}/usr/lib/firmware.tmp ${pkgdir}/usr/lib/firmware/updates"
			]
		),

		'amdgpu-pro-libgl': Package(
			desc = "The AMDGPU Pro libgl library symlinks",
			conflicts = ['libgl'],
			provides  = ['libgl'],
			depends   = ['amdgpu-pro'],
			extra_commands = [
				'mkdir -p "${pkgdir}"/usr/lib',
				'cd "${pkgdir}"/usr/lib',
				'ln -s /usr/lib/amdgpu-pro/libGL.so.1.2   libGL.so.1.2',
				'ln -s /usr/lib/amdgpu-pro/libEGL.so.1    libEGL.so.1',
				'ln -s /usr/lib/amdgpu-pro/libGLESv2.so.2 libGLESv2.so.2',
				'ln -s libGL.so.1.2   libGL.so.1',
				'ln -s libGL.so.1.2   libGL.so',
				'ln -s libEGL.so.1    libEGL.so',
				'ln -s libGLESv2.so   libGLESv2.so',
			]
		),

		'amdgpu-pro-opencl': Package(
			desc = "The AMDGPU Pro OpenCL implementation",
			conflicts = ['libcl'],
			provides  = ['libcl']
		),
		'amdgpu-pro-libdrm': Package(
			desc = "The AMDGPU Pro userspace interface to kernel DRM services"
		),

		'amdgpu-pro-vulkan': Package(
			desc = "The AMDGPU Pro Vulkan driver",
			extra_commands = [
				"sed -i 's@/usr/lib/x86_64-linux-gnu/@/usr/lib/@' ${pkgdir}/etc/vulkan/icd.d/amd_icd64.json"
			]
		),

		'amdgpu-pro-vdpau': Package(
			desc = "The AMDGPU Pro VDPAU driver"
		),

		'lib32-amdgpu-pro': Package(
			desk = "The AMDGPU Pro driver package (32bit libraries)"
		),

		'lib32-amdgpu-pro-opencl': Package(
			desc = "The AMDGPU Pro OpenCL implementation",
			conflicts = ['lib32-libcl'],
			provides  = ['lib32-libcl']
		),

		'lib32-amdgpu-pro-vulkan': Package(
			desc = "The AMDGPU Pro Vulkan driver (32bit libraries)",
			extra_commands = [
				"sed -i 's@/usr/lib/i386-linux-gnu/@/usr/lib32/@' ${pkgdir}/etc/vulkan/icd.d/amd_icd32.json"
			]
		),

		'lib32-amdgpu-pro-libdrm': Package(
			desc = "The AMDGPU Pro userspace interface to kernel DRM services (32bit libraries)"
		),

		'lib32-amdgpu-pro-libgl': Package(
			desc = "The AMDGPU Pro libgl library symlinks (32bit libraries)",
			conflicts = ['lib32-libgl'],
			provides  = ['lib32-libgl'],
			depends   = ['lib32-amdgpu-pro'],
			extra_commands = [
				'mkdir -p "${pkgdir}"/usr/lib32',
				'cd "${pkgdir}"/usr/lib32',
				'ln -s /usr/lib32/amdgpu-pro/libGL.so.1.2   libGL.so.1.2',
				'ln -s /usr/lib32/amdgpu-pro/libEGL.so.1    libEGL.so.1',
				'ln -s /usr/lib32/amdgpu-pro/libGLESv2.so.2 libGLESv2.so.2',
				'ln -s libGL.so.1.2   libGL.so.1',
				'ln -s libGL.so.1.2   libGL.so',
				'ln -s libEGL.so.1    libEGL.so',
				'ln -s libGLESv2.so   libGLESv2.so',
			]
		),

		'lib32-amdgpu-pro-vdpau': Package(
			desc = "The AMDGPU Pro VDPAU driver (32bit libraries)"
		),

		'xf86-video-amdgpu-pro': Package(
			desc = "The AMDGPU Pro X.org video driver",
			conflicts = ['xf86-video-amdgpu', 'xorg-server<1.18.0', 'X-ABI-VIDEODRV_VERSION<20', 'X-ABI-VIDEODRV_VERSION>=21'],
			provides  = ['xf86-video-amdgpu'], # in case anything depends on that
			groups = ['xorg-drivers' 'xorg'],
			extra_commands = [
				"mkdir -p ${pkgdir}/usr/lib/x86_64-linux-gnu",
				"# This is needed because libglx.so has a hardcoded DRI_DRIVER_PATH",
				"ln -s /usr/lib/dri ${pkgdir}/usr/lib/x86_64-linux-gnu/dri",
				"mv ${pkgdir}/usr/lib/amdgpu-pro/1.18/ ${pkgdir}/usr/lib/xorg",
				"rm -rf ${pkgdir}/usr/lib/amdgpu-pro/1.*",
			]
		)
	}
	for key in arch_packages:
		arch_packages[key].name = key
	return arch_packages


subprocess.run(["/usr/bin/wget", "--referer", url_ref, "-N", source_url])
source_file = "amdgpu-pro_{0}-{1}.tar.xz".format(pkgver_base, pkgver_build)

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
sha5sums = [ hashFile(source_file) ]

patches = sorted(glob.glob("*.patch"))

for patch in patches:
    sources.append(patch)
    sha5sums.append(hashFile(patch))

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
sha256sums=({sha5sums})

"""

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

package_deb_extract_tpl = """	extract_deb "${{srcdir}}"/amdgpu-pro-driver/{Filename}
"""

package_header_i386 = """	move_libdir "${pkgdir}/usr/lib/i386-linux-gnu" "usr/lib32"
	move_libdir "${pkgdir}/lib" "usr/lib32"
"""

package_header_x86_64 = """	move_libdir "${pkgdir}/usr/lib/x86_64-linux-gnu"
	move_libdir "${pkgdir}/lib"
"""

package_lib32_cleanup = """

	# lib32 cleanup
	rm -rf "${pkgdir}"/usr/{bin,lib,include,share} "${pkgdir}/var"
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
				print("ERROR: There is a bug in this script, package '%s' is i386 and should start with 'lib32'." % self.name)


		try:
			deps = info["Depends"].split(', ')
		except:
			deps = None

		if deps:
			deps = [ dependencyRE.match(dep).groups() for dep in deps ]
			deps = [(replace_deps[name] if name in replace_deps else name, version) for name, version in deps]
			deps = ["'" + convertName(name, info) + convertVersionSpecifier(name, version) + "'" for name, version in deps if name]

			# remove all dependencies on itself
			deps = [ dep for dep in deps if dep[1:len(self.name)+1] != self.name ]

			if hasattr(self, 'depends') and self.depends:
				deps += self.depends

			self.depends = list(set( deps )) # remove duplicates and append to already existing dependencies

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


# this maps which deb packages should go into specific arch package
# packages without mapping go into 'amdgpu-pro'
packages_map_default = 'amdgpu-pro'
packages_map = {
	'amdgpu-pro':                       'amdgpu-pro',        # deb is metapackage
	'amdgpu-pro-core':                  'amdgpu-pro',
	'amdgpu-pro-graphics':              'amdgpu-pro',
	'libgles2-amdgpu-pro':              'amdgpu-pro',
	'libgbm1-amdgpu-pro':               'amdgpu-pro',

	## contents of this should probably go into /usr/lib/xorg/modules/dri/ instead of /usr/lib/dri ?
	'libgl1-amdgpu-pro-dri':            'amdgpu-pro',

	'amdgpu-pro-dkms':                  'amdgpu-pro-dkms',
	'amdgpu-pro-firmware':              'amdgpu-pro-firmware',

	'amdgpu-pro-clinfo':                'amdgpu-pro-opencl',
	'amdgpu-pro-computing':             'amdgpu-pro-opencl', # deb is metapackage
	'amdgpu-pro-libopencl-dev':         'amdgpu-pro-opencl',
	'amdgpu-pro-libopencl1':            'amdgpu-pro-opencl',
	'amdgpu-pro-opencl-icd':            'amdgpu-pro-opencl',

	'amdgpu-pro-vulkan-driver':         'amdgpu-pro-vulkan',

	'libdrm-amdgpu-pro-amdgpu1':        'amdgpu-pro-libdrm',
	'libdrm-amdgpu-pro-dev':            'amdgpu-pro-libdrm',
	'libdrm-amdgpu-pro-tools':          'amdgpu-pro-libdrm',
	'libdrm2-amdgpu-pro':               'amdgpu-pro-libdrm',

	'libegl1-amdgpu-pro':               'amdgpu-pro', # will be symlinked by amdgpu-pro-libgl, just like mesa-libgl and nvidia-libgl
	'libegl1-amdgpu-pro-dev':           'amdgpu-pro',
	'libgl1-amdgpu-pro-dev':            'amdgpu-pro',
	'libgl1-amdgpu-pro-glx':            'amdgpu-pro',
	'libgles2-amdgpu-pro-dev':          'amdgpu-pro',

	'libvdpau-amdgpu-pro':              'amdgpu-pro-vdpau',
	'xserver-xorg-video-amdgpu-pro':    'xf86-video-amdgpu-pro',


	'lib32-amdgpu-pro-lib32':           'lib32-amdgpu-pro', # deb is a metapackage
	'lib32-libgbm1-amdgpu-pro':         'lib32-amdgpu-pro',

	'lib32-amdgpu-pro-opencl-icd':      'lib32-amdgpu-pro-opencl',
	'lib32-amdgpu-pro-libopencl-dev':   'lib32-amdgpu-pro-opencl',
	'lib32-amdgpu-pro-libopencl1':      'lib32-amdgpu-pro-opencl',

	'lib32-amdgpu-pro-vulkan-driver':   'lib32-amdgpu-pro-vulkan',

	'lib32-libdrm-amdgpu-pro-dev':      'lib32-amdgpu-pro-libdrm',
	'lib32-libdrm2-amdgpu-pro':         'lib32-amdgpu-pro-libdrm',
	'lib32-libdrm-amdgpu-pro-amdgpu1':  'lib32-amdgpu-pro-libdrm',


	'lib32-libegl1-amdgpu-pro-dev':     'lib32-amdgpu-pro',
	'lib32-libgl1-amdgpu-pro-dev':      'lib32-amdgpu-pro',
	'lib32-libgl1-amdgpu-pro-dri':      'lib32-amdgpu-pro',
	'lib32-libgl1-amdgpu-pro-glx':      'lib32-amdgpu-pro',
	'lib32-libgles2-amdgpu-pro':        'lib32-amdgpu-pro',
	'lib32-libgles2-amdgpu-pro-dev':    'lib32-amdgpu-pro',
	'lib32-libegl1-amdgpu-pro':         'lib32-amdgpu-pro',

	'lib32-libvdpau-amdgpu-pro':        'lib32-amdgpu-pro-vdpau',


	'lib32-libgbm-amdgpu-pro-dev':      None, # deb has only *.a
	'libgbm-amdgpu-pro-dev':            None, # deb contains only *.a -> would be empty
}




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
	"libcunit1":            "cunit",
	"libdrm-radeon1":       "libdrm",
	"amdgpu-pro-firmware":  "linux-firmware",
	"libssl1.0.0":          "openssl",
	"zlib1g":               "zlib",
}

replace_version = {
	"linux-firmware": "",
}

# regex for parsing version information of a deb dependency
dependencyRE = re.compile(r"([^ ]+)(?: \((.+)\))?")

arch_map = {
	"amd64": "x86_64",
	"i386": "i686",
	"all": "any"
}

deb_archs={}

def convertName(name, info):
	ret = name
	if info["Architecture"] == "i386" and (name not in deb_archs or "any" not in deb_archs[name]):
		ret = "lib32-" + name

	if name in packages_map:
		return packages_map[name]
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

def convertPackage(info, names):
	if info["Architecture"] == "i386":
		name = "lib32-" + info["Package"]
		arch = "x86_64"
	else:
		name = info["Package"]
		arch = arch_map[info["Architecture"]]

	try:
		deps = info["Depends"].split(", ")
	except:
		deps = []

	deps = [dependency.match(dep).groups() for dep in deps]
	deps = [(replace_deps[name] if name in replace_deps else name, version) for name, version in deps]
	deps = ["'" + convertName(name, info) + convertVersionSpecifier(name, version, names) + "'" for name, version in deps if name]
	deps2 = []
	for dep in deps:
		if not dep in deps2:
			deps2.append(dep)
	deps = "(" + " ".join(deps2) + ")"

	special_op = special_ops[name] if name in special_ops else ""

	desc = info["Description"].split("\n")
	if len(desc) > 2:
		desc = desc[0]
	else:
		desc = " ".join(x.strip() for x in desc)

	ret = package_header_tpl.format(DEPENDS=deps, NAME=name, ARCH=arch, DESC=quote(desc), **info)

	if info["Architecture"] == "i386":
		ret += package_header_i386
	else:
		ret += package_header_x86_64

	if special_op:
		ret += special_op + "\n"
	if info["Architecture"] == "i386":
		ret += "\trm -Rf ${pkgdir}/usr/share/doc ${pkgdir}/usr/include\n"
	ret += package_footer

	return ret




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
		name = "lib32-" + info["Package"] if info["Architecture"] == "i386" else info["Package"]
		arch_pkg = arch_packages[ packages_map_default ]
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
	sha5sums="\n\t".join(sha5sums)
))

print(package_functions)


with lzma.open(source_file, "r") as tar:
	with tarfile.open(fileobj=tar) as tf:
		with tf.extractfile("amdgpu-pro-driver/Packages.gz") as gz:
			with gzip.open(gz, "r") as packages:
				writePackages(packages)

for pkg in arch_package_names:
	print( arch_packages[pkg].toPKGBUILD() )
