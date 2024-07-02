# Generated with ./gen_replace_deps.sh > replace_deps.py
# for driver version optional

replace_deps = {
    'amdgpu-core':                 'amdgpu-core',           #could_not_auto_translate
    'amdgpu-dkms':                 'amdgpu-dkms',           #could_not_auto_translate
    'amdgpu-dkms-firmware':        'amdgpu-dkms-firmware',  #could_not_auto_translate
    'amdgpu-lib32':                'amdgpu-lib32',          #could_not_auto_translate
    'libc6':                       None,                    #manually_mapped
    'libdrm2-amdgpu':              'libdrm',                #auto_translated
    'libgbm1-amdgpu':              None,                    #manually_Do_not_know_what_it_is
    'libgcc-s1':                   None,                    #manually_mapped
    'libgl1':                      'libglvnd',              #manually_mapped
    'libssl1.1':                   'openssl-1.1',           #manually_mapped
    'libstdc++6':                  None,                    #manually_mapped
    'libvulkan1':                  'vulkan-icd-loader',     #manually_mapped
    'libwayland-amdgpu-client0':   'wayland',               #manually_mapped
    'libwayland-client0':          'wayland',               #auto_translated
    'libx11-6':                    'libx11',                #auto_translated
    'mesa-amdgpu-vulkan-drivers':  'mesa',                  #auto_translated
    'mesa-vulkan-drivers':         'vulkan-radeon',         #manually_mapped
    'rocm-opencl-runtime':         'rocm-opencl-runtime',   #manually_mapped
    'zlib1g':                      'zlib',                  #manually_mapped
}
