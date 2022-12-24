# Generated with ./gen_replace_deps.sh > replace_deps.py
# for driver version optional

replace_deps = {
    'amdgpu-core':                'amdgpu-core',          #could_not_auto_translate
    'amdgpu-lib32':               'amdgpu-lib32',         #could_not_auto_translate
    'libc6':                      None,                   #manually_mapped
    'libdrm2-amdgpu':             'libdrm',               #auto_translated
    'libdrm-amdgpu-amdgpu1':      'libdrm',               #auto_translated
    'libgbm1-amdgpu':             None,                   #manually_Do_not_know_what_it_is
    'libgcc-s1':                  None,                   #manually_mapped
    'libgl1':                     'libglvnd',             #manually_mapped
    'libssl1.1':                  'openssl-1.1',          #auto_translated
    'libstdc++6':                 None,                   #manually_mapped
    'libvulkan1':                 'vulkan-icd-loader',    #auto_translated
    'libwayland-amdgpu-client0':  'wayland',              #auto_translated
    'libwayland-client0':         'wayland',              #auto_translated
    'libx11-6':                   'libx11',               #auto_translated
    'rocm-opencl-runtime':        'rocm-opencl-runtime',  #manually_mapped
    'zlib1g':                     'zlib',                 #auto_translated
}
