# Generated with ./gen_packages_map.sh > packages_map.py
# for driver version 22.40-1538781.22.04

packages_map = {
    'amdgpu-pro':                              None,                       #we_have_already_combined_libgl_to_single_package
    'amdgpu-pro-core':                         None,                       #unneeded_meta_package
    'amdgpu-pro-lib32':                        None,                       #we_have_already_combined_libgl_to_single_package
    'amdgpu-pro-oglp':                         None,                       #unneeded_meta_package
    'amdgpu-pro-oglp:i386':                    None,                       #unneeded_meta_package
    'amf-amdgpu-pro':                          'amf-amdgpu-pro',           #mapped_manually
    'clinfo-amdgpu-pro':                       None,                       #unneeded_pro_component
    'clinfo-amdgpu-pro:i386':                  None,                       #unneeded_pro_component
    'libamdenc-amdgpu-pro':                    'amf-amdgpu-pro',           #mapped_manually.Maybe_this_should_go_to_a_saparate_package?
    'libegl1-amdgpu-pro-oglp':                 'amdgpu-pro-oglp',          #mapped_manually
    'libegl1-amdgpu-pro-oglp:i386':            'lib32-amdgpu-pro-oglp',    #mapped_manually
    'libgl1-amdgpu-pro-oglp-dri':              'amdgpu-pro-oglp',          #mapped_manually
    'libgl1-amdgpu-pro-oglp-dri:i386':         'lib32-amdgpu-pro-oglp',    #mapped_manually
    'libgl1-amdgpu-pro-oglp-ext':              'amdgpu-pro-oglp',          #mapped_manually
    'libgl1-amdgpu-pro-oglp-gbm':              'amdgpu-pro-oglp',          #mapped_manually
    'libgl1-amdgpu-pro-oglp-glx':              'amdgpu-pro-oglp',          #mapped_manually
    'libgl1-amdgpu-pro-oglp-glx:i386':         'lib32-amdgpu-pro-oglp',    #mapped_manually
    'libgles1-amdgpu-pro-oglp':                'amdgpu-pro-oglp',          #mapped_manually
    'libgles1-amdgpu-pro-oglp:i386':           'lib32-amdgpu-pro-oglp',    #mapped_manually
    'libgles2-amdgpu-pro-oglp':                'amdgpu-pro-oglp',          #mapped_manually
    'libgles2-amdgpu-pro-oglp:i386':           'lib32-amdgpu-pro-oglp',    #mapped_manually
    'ocl-icd-libopencl1-amdgpu-pro':           None,                       #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro:i386':      None,                       #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro-dev':       None,                       #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro-dev:i386':  None,                       #unneeded_pro_component
    'opencl-legacy-amdgpu-pro-icd':            None,                       #opencl_goes_to_opencl-amd
    'opencl-legacy-amdgpu-pro-icd:i386':       None,                       #opencl_goes_to_opencl-amd
    'vulkan-amdgpu-pro':                       'vulkan-amdgpu-pro',        #mapped_manually
    'vulkan-amdgpu-pro:i386':                  'lib32-vulkan-amdgpu-pro',  #mapped_manually
}
