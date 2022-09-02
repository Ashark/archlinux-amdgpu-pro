# Generated with ./gen_packages_map.sh > packages_map.py
# for driver version 22.20-1462318~22.04

packages_map = {
    'amdgpu-pro':                              None,                       #we_have_already_combined_libgl_to_single_package
    'amdgpu-pro-core':                         None,                       #unneeded_meta_package
    'amdgpu-pro-lib32':                        None,                       #we_have_already_combined_libgl_to_single_package
    'amf-amdgpu-pro':                          'amf-amdgpu-pro',           #mapped_manually
    'clinfo-amdgpu-pro':                       None,                       #unneeded_pro_component
    'clinfo-amdgpu-pro:i386':                  None,                       #unneeded_pro_component
    'libamdenc-amdgpu-pro':                    'amf-amdgpu-pro',           #mapped_manually.Maybe_this_should_go_to_a_saparate_package?
    'libegl1-amdgpu-pro':                      'amdgpu-pro-libgl',         #mapped_manually
    'libegl1-amdgpu-pro:i386':                 'lib32-amdgpu-pro-libgl',   #mapped_manually
    'libgl1-amdgpu-pro-appprofiles':           'amdgpu-pro-libgl',         #mapped_manually
    'libgl1-amdgpu-pro-dri':                   'amdgpu-pro-libgl',         #mapped_manually
    'libgl1-amdgpu-pro-dri:i386':              'lib32-amdgpu-pro-libgl',   #mapped_manually
    'libgl1-amdgpu-pro-ext':                   'amdgpu-pro-libgl',         #mapped_manually
    'libgl1-amdgpu-pro-ext:i386':              'lib32-amdgpu-pro-libgl',   #mapped_manually
    'libgl1-amdgpu-pro-glx':                   'amdgpu-pro-libgl',         #mapped_manually
    'libgl1-amdgpu-pro-glx:i386':              'lib32-amdgpu-pro-libgl',   #mapped_manually
    'libglapi1-amdgpu-pro':                    'amdgpu-pro-libgl',         #mapped_manually
    'libglapi1-amdgpu-pro:i386':               'lib32-amdgpu-pro-libgl',   #mapped_manually
    'libgles2-amdgpu-pro':                     'amdgpu-pro-libgl',         #mapped_manually
    'libgles2-amdgpu-pro:i386':                'lib32-amdgpu-pro-libgl',   #mapped_manually
    'ocl-icd-libopencl1-amdgpu-pro':           None,                       #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro:i386':      None,                       #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro-dev':       None,                       #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro-dev:i386':  None,                       #unneeded_pro_component
    'opencl-legacy-amdgpu-pro-icd':            None,                       #opencl_goes_to_opencl-amd
    'opencl-legacy-amdgpu-pro-icd:i386':       None,                       #opencl_goes_to_opencl-amd
    'vulkan-amdgpu-pro':                       'vulkan-amdgpu-pro',        #mapped_manually
    'vulkan-amdgpu-pro:i386':                  'lib32-vulkan-amdgpu-pro',  #mapped_manually
}
