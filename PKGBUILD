# Author: Janusz Lewandowski <lew21@xtreeme.org>
# Contributor: David McFarland <corngood@gmail.com>
# Maintainer: Andrew Shark <ashark @at@ linuxcomp.ru>
# Autogenerated from AMD's Packages file
# with https://github.com/Ashark/archlinux-amdgpu-pro/blob/master/gen-PKGBUILD.py

major=22.20.5
major_short=22.20
minor=1511376
ubuntu_ver=22.04

pkgbase=amdgpu-pro-installer
pkgname=(
amf-amdgpu-pro
amdgpu-pro-libgl
lib32-amdgpu-pro-libgl
vulkan-amdgpu-pro
lib32-vulkan-amdgpu-pro
)
pkgver=${major}_${minor}
pkgrel=1
arch=('x86_64')
url=https://www.amd.com/en/support/kb/release-notes/rn-amdgpu-unified-linux-22-20
license=('custom: multiple')
groups=('Radeon_Software_for_Linux')
makedepends=('wget')

DLAGENTS='https::/usr/bin/wget --referer https://www.amd.com/en/support/kb/release-notes/rn-amdgpu-unified-linux-22-20 -N %u'

source=(progl
	progl.bash-completion
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/a/amf-amdgpu-pro/amf-amdgpu-pro_1.4.26-${minor}~${ubuntu_ver}_amd64.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/liba/libamdenc-amdgpu-pro/libamdenc-amdgpu-pro_1.0-${minor}~${ubuntu_ver}_amd64.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libegl1-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_i386.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libegl1-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/a/appprofiles-amdgpu-pro/libgl1-amdgpu-pro-appprofiles_${major_short}-${minor}~${ubuntu_ver}_all.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libgl1-amdgpu-pro-dri_${major_short}-${minor}~${ubuntu_ver}_i386.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libgl1-amdgpu-pro-dri_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libgl1-amdgpu-pro-ext_${major_short}-${minor}~${ubuntu_ver}_i386.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libgl1-amdgpu-pro-ext_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libgl1-amdgpu-pro-glx_${major_short}-${minor}~${ubuntu_ver}_i386.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libgl1-amdgpu-pro-glx_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libglapi1-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_i386.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libglapi1-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libgles2-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_i386.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/o/opengl-amdgpu-pro/libgles2-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/v/vulkan-amdgpu-pro/vulkan-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_i386.deb
	http://repo.radeon.com/amdgpu/${major}/ubuntu/pool/proprietary/v/vulkan-amdgpu-pro/vulkan-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_amd64.deb)
sha256sums=(feb74796c3152cbafaba89d96e68a152f209bd3058c7eb0413cbe1ab0764e96f
	e32801c38b475cd8df17a407726b86db3de26410f563d688325b4d4314fc5354
	f41d6a763f297407658e9b753863a7ec9a9c835e7a3567f6191523fdfeb912bc
	8e8fbb5543b1c9b41c993c779c7dd088cde7c70364a21cac4deb0e8e6ccfcd6c
	a6418bba87c64d4f495bde394359cee4d787972ff34baebe30f4662deab8ac39
	cf5414440287fcbe79bb98c7b56e07d3a07d71394fcbe80a6d1ff37185355c34
	798d15813b39489796344f029f0496d35a61ccbb0a133afdabb5b7be91ace316
	c25e4ecb12555c3984ea4dbac9418745d2c5a332a2522793673f7ed215fbbf4d
	1b78663a07220cc52421536aebdbf2f1908d34c5ec245392ab4bea6122c7f144
	06b6c1208a4f985aa642c251fccdbc2b7cce923decf5f46bc5ea587e754df1da
	da9e802ea13b42c1b29ca3cdd83f7fc02bab449dda934781fcf5e3cc259abbeb
	3e91820eec935db365c41a0c1b2996d116bd169f708cf445cd029b52f222253d
	a9973270d0e829c93fc5805add8c1dfbc3c3a2fb28dfb672862cebcc39cd17d8
	59763b52bc59c9bb86ee9efa6ff772d9ef0fd54c8a0e2df77e61ce2ea4e9c450
	d72d35d17f901e184b6ac5464db1ce6ad26c022543ecd5a93c0cca311d49742e
	c4cecd9cd414e1661eb27c493e4bd23d5fff4d4998747de159456eb877936cf4
	4e01a1e4d51956dffb963e7d87fbeedfbe2aaa64fa10a92ce9792feee01714d5
	69a4e86d8f9e84c0430049d01544d563b7e64cb68781b41a72a74b1a45124347
	654c8426b7cda4c23d888d7a0520dab5f9fd43d9de2cc570f359d88968517232)



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

package_amf-amdgpu-pro () {
    pkgdesc="AMDGPU Pro Advanced Multimedia Framework"
    license=('custom: AMDGPU-PRO EULA')
    depends=("libdrm" "vulkan-amdgpu-pro=${major}_${minor}-${pkgrel}")
    optdepends=("rocm-opencl-runtime: Warning unspecified optdep description")

    extract_deb "${srcdir}"/amf-amdgpu-pro_1.4.26-${minor}~${ubuntu_ver}_amd64.deb
    extract_deb "${srcdir}"/libamdenc-amdgpu-pro_1.0-${minor}~${ubuntu_ver}_amd64.deb
    move_libdir "opt/amdgpu-pro/lib/x86_64-linux-gnu" "usr/lib"
    move_copyright
}

package_amdgpu-pro-libgl () {
    pkgdesc="AMDGPU Pro OpenGL driver"
    license=('custom: AMDGPU-PRO EULA')
    provides=('libgl')
    depends=("libdrm" "libx11" "libxcb" "libxdamage" "libxext" "libxfixes" "libxxf86vm")
    backup=(etc/amd/amdapfxx.blb)

    extract_deb "${srcdir}"/libegl1-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
    extract_deb "${srcdir}"/libgl1-amdgpu-pro-appprofiles_${major_short}-${minor}~${ubuntu_ver}_all.deb
    extract_deb "${srcdir}"/libgl1-amdgpu-pro-dri_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
    extract_deb "${srcdir}"/libgl1-amdgpu-pro-ext_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
    extract_deb "${srcdir}"/libgl1-amdgpu-pro-glx_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
    extract_deb "${srcdir}"/libglapi1-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
    extract_deb "${srcdir}"/libgles2-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
    move_copyright

    # extra_commands:
    move_libdir "usr/lib/x86_64-linux-gnu" "usr/lib"
    move_libdir "opt/amdgpu-pro/lib/x86_64-linux-gnu" "usr/lib/amdgpu-pro"
    move_libdir "opt/amdgpu-pro/lib/xorg" "usr/lib/amdgpu-pro/xorg"
    move_libdir "opt/amdgpu/share/drirc.d" "usr/share/drirc.d"
    sed -i "s|/opt/amdgpu-pro/lib/x86_64-linux-gnu|#/usr/lib/amdgpu-pro  # commented to prevent problems of booting with amdgpu-pro, use progl script|" "${pkgdir}"/etc/ld.so.conf.d/10-amdgpu-pro-x86_64.conf
    install -Dm755 "${srcdir}"/progl "${pkgdir}"/usr/bin/progl
    install -Dm755 "${srcdir}"/progl.bash-completion "${pkgdir}"/usr/share/bash-completion/completions/progl
    # For some reason, applications started with normal OpenGL (i.e. without ag pro) crashes at launch if this conf file is presented, so hide it for now, until I find out the reason of that.
    mv "${pkgdir}"/usr/share/drirc.d/10-amdgpu-pro.conf "${pkgdir}"/usr/share/drirc.d/10-amdgpu-pro.conf.hide
}

package_lib32-amdgpu-pro-libgl () {
    pkgdesc="AMDGPU Pro OpenGL driver (32-bit)"
    license=('custom: AMDGPU-PRO EULA')
    provides=('lib32-libgl')
    depends=("amdgpu-pro-libgl=${major}_${minor}-${pkgrel}" "lib32-libdrm" "lib32-libx11" "lib32-libxcb" "lib32-libxdamage" "lib32-libxext" "lib32-libxfixes" "lib32-libxxf86vm")
    backup=(etc/amd/amdrc etc/ld.so.conf.d/10-amdgpu-pro-i386.conf)

    extract_deb "${srcdir}"/libegl1-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_i386.deb
    extract_deb "${srcdir}"/libgl1-amdgpu-pro-dri_${major_short}-${minor}~${ubuntu_ver}_i386.deb
    extract_deb "${srcdir}"/libgl1-amdgpu-pro-ext_${major_short}-${minor}~${ubuntu_ver}_i386.deb
    extract_deb "${srcdir}"/libgl1-amdgpu-pro-glx_${major_short}-${minor}~${ubuntu_ver}_i386.deb
    extract_deb "${srcdir}"/libglapi1-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_i386.deb
    extract_deb "${srcdir}"/libgles2-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_i386.deb
    move_copyright

    # extra_commands:
    rm "${pkgdir}"/etc/amd/amdrc "${pkgdir}"/opt/amdgpu-pro/lib/xorg/modules/extensions/libglx.so "${pkgdir}"/opt/amdgpu/share/drirc.d/10-amdgpu-pro.conf
    move_libdir "usr/lib/i386-linux-gnu" "usr/lib32"
    move_libdir "opt/amdgpu-pro/lib/i386-linux-gnu" "usr/lib32/amdgpu-pro"
    sed -i "s|/opt/amdgpu-pro/lib/i386-linux-gnu|#/usr/lib32/amdgpu-pro  # commented to prevent problems of booting with amdgpu-pro, use progl32 script|" "${pkgdir}"/etc/ld.so.conf.d/10-amdgpu-pro-i386.conf
}

package_vulkan-amdgpu-pro () {
    pkgdesc="AMDGPU Pro Vulkan driver"
    license=('custom: AMDGPU-PRO EULA')
    provides=('vulkan-driver')
    depends=("vulkan-icd-loader")
    optdepends=("openssl-1.1: Warning unspecified optdep description")

    extract_deb "${srcdir}"/vulkan-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_amd64.deb
    move_libdir "opt/amdgpu-pro/lib/x86_64-linux-gnu" "usr/lib"
    move_copyright

    # extra_commands:
    mkdir -p "${pkgdir}"/usr/share/vulkan/icd.d/
    mv "${pkgdir}"/opt/amdgpu-pro/etc/vulkan/icd.d/amd_icd64.json "${pkgdir}"/usr/share/vulkan/icd.d/amd_pro_icd64.json
    mv "${pkgdir}"/usr/lib/amdvlk64.so "${pkgdir}"/usr/lib/amdvlkpro64.so
    sed -i "s#/opt/amdgpu-pro/lib/x86_64-linux-gnu/amdvlk64.so#/usr/lib/amdvlkpro64.so#" "${pkgdir}"/usr/share/vulkan/icd.d/amd_pro_icd64.json
    find ${pkgdir} -type d -empty -delete
}

package_lib32-vulkan-amdgpu-pro () {
    pkgdesc="AMDGPU Pro Vulkan driver (32-bit)"
    license=('custom: AMDGPU-PRO EULA')
    provides=('lib32-vulkan-driver')
    depends=("lib32-vulkan-icd-loader")
    optdepends=("lib32-openssl-1.1: Warning unspecified optdep description")

    extract_deb "${srcdir}"/vulkan-amdgpu-pro_${major_short}-${minor}~${ubuntu_ver}_i386.deb
    move_libdir "opt/amdgpu-pro/lib/i386-linux-gnu" "usr/lib32"
    move_copyright

    # extra_commands:
    mkdir -p "${pkgdir}"/usr/share/vulkan/icd.d/
    mv "${pkgdir}"/opt/amdgpu-pro/etc/vulkan/icd.d/amd_icd32.json "${pkgdir}"/usr/share/vulkan/icd.d/amd_pro_icd32.json
    mv "${pkgdir}"/usr/lib32/amdvlk32.so "${pkgdir}"/usr/lib32/amdvlkpro32.so
    sed -i "s#/opt/amdgpu-pro/lib/i386-linux-gnu/amdvlk32.so#/usr/lib32/amdvlkpro32.so#" "${pkgdir}"/usr/share/vulkan/icd.d/amd_pro_icd32.json
    find ${pkgdir} -type d -empty -delete
}

