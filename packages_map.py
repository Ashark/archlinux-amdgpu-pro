# Generated with ./gen_packages_map.sh > packages_map.py
# for driver version 21.20-1271047

packages_map = {
    'amdgpu':                                  None,                       #unneeded_open_component
    'amdgpu-core':                             None,                       #unneeded_meta_package
    'amdgpu-dkms':                             None,                       #unneeded_open_component
    'amdgpu-dkms-firmware':                    None,                       #unneeded_open_component
    'amdgpu-doc':                              None,                       #arch_specific_instructions_will_be_covered_in_archwiki
    'amdgpu-lib':                              None,                       #unneeded_open_component
    'amdgpu-lib32':                            None,                       #unneeded_open_component
    'amdgpu-pin':                              None,                       #debian_specific_package,_not_needed
    'amdgpu-pro':                              None,                       #we_have_already_combined_libgl_to_single_package
    'amdgpu-pro-core':                         None,                       #unneeded_meta_package
    'amdgpu-pro-lib32':                        None,                       #we_have_already_combined_libgl_to_single_package
    'amdgpu-pro-pin':                          None,                       #debian_specific_package,_not_needed
    'amdgpu-pro-rocr-opencl':                  None,                       #opencl_goes_to_opencl-amd
    'amf-amdgpu-pro':                          'amf-amdgpu-pro',           #mapped_manually
    'clinfo-amdgpu-pro':                       None,                       #unneeded_pro_component
    'clinfo-amdgpu-pro:i386':                  None,                       #unneeded_pro_component
    'comgr-amdgpu-pro':                        None,                       #opencl_goes_to_opencl-amd
    'comgr-amdgpu-pro-dev':                    None,                       #opencl_goes_to_opencl-amd
    'gst-omx-amdgpu':                          None,                       #unneeded_open_component
    'gst-omx-amdgpu:i386':                     None,                       #unneeded_open_component
    'hip-rocr-amdgpu-pro':                     None,                       #opencl_goes_to_opencl-amd
    'hsa-runtime-rocr-amdgpu':                 None,                       #opencl_goes_to_opencl-amd
    'hsa-runtime-rocr-amdgpu-dev':             None,                       #opencl_goes_to_opencl-amd
    'hsakmt-roct-amdgpu':                      None,                       #opencl_goes_to_opencl-amd
    'hsakmt-roct-amdgpu-dev':                  None,                       #opencl_goes_to_opencl-amd
    'kfdtest-amdgpu':                          None,                       #opencl_goes_to_opencl-amd
    'libdrm-amdgpu-amdgpu1':                   None,                       #unneeded_open_component
    'libdrm-amdgpu-amdgpu1:i386':              None,                       #unneeded_open_component
    'libdrm-amdgpu-common':                    None,                       #unneeded_open_component
    'libdrm-amdgpu-dev':                       None,                       #not_installed_even_in_ubuntu
    'libdrm-amdgpu-dev:i386':                  None,                       #not_installed_even_in_ubuntu
    'libdrm-amdgpu-radeon1':                   None,                       #not_installed_even_in_ubuntu
    'libdrm-amdgpu-radeon1:i386':              None,                       #not_installed_even_in_ubuntu
    'libdrm-amdgpu-utils':                     None,                       #not_installed_even_in_ubuntu
    'libdrm-amdgpu-utils:i386':                None,                       #not_installed_even_in_ubuntu
    'libdrm2-amdgpu':                          None,                       #unneeded_open_component
    'libdrm2-amdgpu:i386':                     None,                       #unneeded_open_component
    'libegl1-amdgpu-mesa':                     None,                       #unneeded_open_component
    'libegl1-amdgpu-mesa:i386':                None,                       #unneeded_open_component
    'libegl1-amdgpu-mesa-dev':                 None,                       #unneeded_open_component
    'libegl1-amdgpu-mesa-dev:i386':            None,                       #unneeded_open_component
    'libegl1-amdgpu-mesa-drivers':             None,                       #unneeded_open_component
    'libegl1-amdgpu-mesa-drivers:i386':        None,                       #unneeded_open_component
    'libegl1-amdgpu-pro':                      'amdgpu-pro-libgl',         #mapped_manually
    'libegl1-amdgpu-pro:i386':                 'lib32-amdgpu-pro-libgl',   #mapped_manually
    'libgbm-amdgpu-dev':                       None,                       #unneeded_open_component
    'libgbm-amdgpu-dev:i386':                  None,                       #unneeded_open_component
    'libgbm1-amdgpu':                          None,                       #unneeded_open_component
    'libgbm1-amdgpu:i386':                     None,                       #unneeded_open_component
    'libgl1-amdgpu-mesa-dev':                  None,                       #unneeded_open_component
    'libgl1-amdgpu-mesa-dev:i386':             None,                       #unneeded_open_component
    'libgl1-amdgpu-mesa-dri':                  None,                       #unneeded_open_component
    'libgl1-amdgpu-mesa-dri:i386':             None,                       #unneeded_open_component
    'libgl1-amdgpu-mesa-glx':                  None,                       #unneeded_open_component
    'libgl1-amdgpu-mesa-glx:i386':             None,                       #unneeded_open_component
    'libgl1-amdgpu-pro-appprofiles':           'amdgpu-pro-libgl',         #mapped_manually
    'libgl1-amdgpu-pro-dri':                   'amdgpu-pro-libgl',         #mapped_manually
    'libgl1-amdgpu-pro-dri:i386':              'lib32-amdgpu-pro-libgl',   #mapped_manually
    'libgl1-amdgpu-pro-ext':                   'amdgpu-pro-libgl',         #mapped_manually
    'libgl1-amdgpu-pro-ext:i386':              'lib32-amdgpu-pro-libgl',   #mapped_manually
    'libgl1-amdgpu-pro-glx':                   'amdgpu-pro-libgl',         #mapped_manually
    'libgl1-amdgpu-pro-glx:i386':              'lib32-amdgpu-pro-libgl',   #mapped_manually
    'libglapi-amdgpu-mesa':                    None,                       #unneeded_open_component
    'libglapi-amdgpu-mesa:i386':               None,                       #unneeded_open_component
    'libglapi1-amdgpu-pro':                    'amdgpu-pro-libgl',         #mapped_manually
    'libglapi1-amdgpu-pro:i386':               'lib32-amdgpu-pro-libgl',   #mapped_manually
    'libgles1-amdgpu-mesa':                    None,                       #unneeded_open_component
    'libgles1-amdgpu-mesa:i386':               None,                       #unneeded_open_component
    'libgles1-amdgpu-mesa-dev':                None,                       #unneeded_open_component
    'libgles1-amdgpu-mesa-dev:i386':           None,                       #unneeded_open_component
    'libgles2-amdgpu-mesa':                    None,                       #unneeded_open_component
    'libgles2-amdgpu-mesa:i386':               None,                       #unneeded_open_component
    'libgles2-amdgpu-mesa-dev':                None,                       #unneeded_open_component
    'libgles2-amdgpu-mesa-dev:i386':           None,                       #unneeded_open_component
    'libgles2-amdgpu-pro':                     'amdgpu-pro-libgl',         #mapped_manually
    'libgles2-amdgpu-pro:i386':                'lib32-amdgpu-pro-libgl',   #mapped_manually
    'libllvm-amdgpu-pro-rocm':                 None,                       #opencl_goes_to_opencl-amd
    'libllvm12.0-amdgpu':                      None,                       #unneeded_open_component
    'libllvm12.0-amdgpu:i386':                 None,                       #unneeded_open_component
    'libwayland-amdgpu-bin':                   None,                       #unneeded_open_component
    'libwayland-amdgpu-bin:i386':              None,                       #unneeded_open_component
    'libwayland-amdgpu-client0':               None,                       #unneeded_open_component
    'libwayland-amdgpu-client0:i386':          None,                       #unneeded_open_component
    'libwayland-amdgpu-cursor0':               None,                       #unneeded_open_component
    'libwayland-amdgpu-cursor0:i386':          None,                       #unneeded_open_component
    'libwayland-amdgpu-dev':                   None,                       #unneeded_open_component
    'libwayland-amdgpu-dev:i386':              None,                       #unneeded_open_component
    'libwayland-amdgpu-doc':                   None,                       #unneeded_open_component
    'libwayland-amdgpu-egl-backend-dev':       None,                       #unneeded_open_component
    'libwayland-amdgpu-egl-backend-dev:i386':  None,                       #unneeded_open_component
    'libwayland-amdgpu-egl1':                  None,                       #unneeded_open_component
    'libwayland-amdgpu-egl1:i386':             None,                       #unneeded_open_component
    'libwayland-amdgpu-server0':               None,                       #unneeded_open_component
    'libwayland-amdgpu-server0:i386':          None,                       #unneeded_open_component
    'libxatracker-amdgpu-dev':                 None,                       #not_installed_even_in_ubuntu
    'libxatracker-amdgpu-dev:i386':            None,                       #not_installed_even_in_ubuntu
    'libxatracker2-amdgpu':                    None,                       #unneeded_open_component
    'libxatracker2-amdgpu:i386':               None,                       #unneeded_open_component
    'llvm-amdgpu':                             None,                       #not_installed_even_in_ubuntu
    'llvm-amdgpu:i386':                        None,                       #not_installed_even_in_ubuntu
    'llvm-amdgpu-12.0':                        None,                       #not_installed_even_in_ubuntu
    'llvm-amdgpu-12.0:i386':                   None,                       #not_installed_even_in_ubuntu
    'llvm-amdgpu-12.0-dev':                    None,                       #not_installed_even_in_ubuntu
    'llvm-amdgpu-12.0-dev:i386':               None,                       #not_installed_even_in_ubuntu
    'llvm-amdgpu-12.0-runtime':                None,                       #not_installed_even_in_ubuntu
    'llvm-amdgpu-12.0-runtime:i386':           None,                       #not_installed_even_in_ubuntu
    'llvm-amdgpu-dev':                         None,                       #not_installed_even_in_ubuntu
    'llvm-amdgpu-dev:i386':                    None,                       #not_installed_even_in_ubuntu
    'llvm-amdgpu-pro-rocm':                    None,                       #opencl_goes_to_opencl-amd
    'llvm-amdgpu-pro-rocm-dev':                None,                       #opencl_goes_to_opencl-amd
    'llvm-amdgpu-runtime':                     None,                       #not_installed_even_in_ubuntu
    'llvm-amdgpu-runtime:i386':                None,                       #not_installed_even_in_ubuntu
    'mesa-amdgpu-common-dev':                  None,                       #not_installed_even_in_ubuntu
    'mesa-amdgpu-common-dev:i386':             None,                       #not_installed_even_in_ubuntu
    'mesa-amdgpu-omx-drivers':                 None,                       #unneeded_open_component
    'mesa-amdgpu-omx-drivers:i386':            None,                       #unneeded_open_component
    'mesa-amdgpu-va-drivers':                  None,                       #unneeded_open_component
    'mesa-amdgpu-va-drivers:i386':             None,                       #unneeded_open_component
    'mesa-amdgpu-vdpau-drivers':               None,                       #unneeded_open_component
    'mesa-amdgpu-vdpau-drivers:i386':          None,                       #unneeded_open_component
    'ocl-icd-libopencl1-amdgpu-pro':           None,                       #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro:i386':      None,                       #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro-dev':       None,                       #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro-dev:i386':  None,                       #unneeded_pro_component
    'opencl-orca-amdgpu-pro-icd':              None,                       #opencl_goes_to_opencl-amd
    'opencl-orca-amdgpu-pro-icd:i386':         None,                       #opencl_goes_to_opencl-amd
    'opencl-rocr-amdgpu-pro':                  None,                       #opencl_goes_to_opencl-amd
    'opencl-rocr-amdgpu-pro-dev':              None,                       #opencl_goes_to_opencl-amd
    'rocm-device-libs-amdgpu-pro':             None,                       #opencl_goes_to_opencl-amd
    'vulkan-amdgpu':                           None,                       #unneeded_open_component
    'vulkan-amdgpu-pro':                       'vulkan-amdgpu-pro',        #mapped_manually
    'vulkan-amdgpu-pro:i386':                  'lib32-vulkan-amdgpu-pro',  #mapped_manually
    'wayland-protocols-amdgpu':                None,                       #unneeded_open_component
    'xserver-xorg-amdgpu-video-amdgpu':        None,                       #unneeded_open_component
}
