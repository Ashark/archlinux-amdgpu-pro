# Generated with ./gen_packages_map.sh > packages_map.py
# for driver version 22.40-1518373.22.04

packages_map = {
    'amdgpu-pro':                              None,                                #we_have_already_combined_libgl_to_single_package
    'amdgpu-pro-core':                         None,                                #unneeded_meta_package
    'amdgpu-pro-lib32':                        None,                                #we_have_already_combined_libgl_to_single_package
    'amdgpu-pro-oglp':                         'amdgpu-pro-oglp',                   #
    'amdgpu-pro-oglp:i386':                    'lib32-amdgpu-pro-oglp',             #
    'amf-amdgpu-pro':                          'amf-amdgpu-pro',                    #mapped_manually
    'clinfo-amdgpu-pro':                       None,                                #unneeded_pro_component
    'clinfo-amdgpu-pro:i386':                  None,                                #unneeded_pro_component
    'libamdenc-amdgpu-pro':                    'amf-amdgpu-pro',                    #mapped_manually.Maybe_this_should_go_to_a_saparate_package?
    'libegl1-amdgpu-pro-oglp':                 'libegl1-amdgpu-pro-oglp',           #
    'libegl1-amdgpu-pro-oglp:i386':            'lib32-libegl1-amdgpu-pro-oglp',     #
    'libgl1-amdgpu-pro-oglp-dri':              'libgl1-amdgpu-pro-oglp-dri',        #
    'libgl1-amdgpu-pro-oglp-dri:i386':         'lib32-libgl1-amdgpu-pro-oglp-dri',  #
    'libgl1-amdgpu-pro-oglp-ext':              'libgl1-amdgpu-pro-oglp-ext',        #
    'libgl1-amdgpu-pro-oglp-gbm':              'libgl1-amdgpu-pro-oglp-gbm',        #
    'libgl1-amdgpu-pro-oglp-glx':              'libgl1-amdgpu-pro-oglp-glx',        #
    'libgl1-amdgpu-pro-oglp-glx:i386':         'lib32-libgl1-amdgpu-pro-oglp-glx',  #
    'libgles1-amdgpu-pro-oglp':                'libgles1-amdgpu-pro-oglp',          #
    'libgles1-amdgpu-pro-oglp:i386':           'lib32-libgles1-amdgpu-pro-oglp',    #
    'libgles2-amdgpu-pro-oglp':                'libgles2-amdgpu-pro-oglp',          #
    'libgles2-amdgpu-pro-oglp:i386':           'lib32-libgles2-amdgpu-pro-oglp',    #
    'ocl-icd-libopencl1-amdgpu-pro':           None,                                #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro:i386':      None,                                #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro-dev':       None,                                #unneeded_pro_component
    'ocl-icd-libopencl1-amdgpu-pro-dev:i386':  None,                                #unneeded_pro_component
    'opencl-legacy-amdgpu-pro-icd':            None,                                #opencl_goes_to_opencl-amd
    'opencl-legacy-amdgpu-pro-icd:i386':       None,                                #opencl_goes_to_opencl-amd
    'vulkan-amdgpu-pro':                       'vulkan-amdgpu-pro',                 #mapped_manually
    'vulkan-amdgpu-pro:i386':                  'lib32-vulkan-amdgpu-pro',           #mapped_manually
}
