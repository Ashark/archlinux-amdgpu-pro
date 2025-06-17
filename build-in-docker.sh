#!/bin/bash

# Build and start the container
docker-compose up -d

# Execute the build commands as builder user
docker-compose exec --user builder amdgpu-pro-builder bash -c '
    # Create and update the mirror
    aptly -ignore-signatures mirror create agpro-6.4.1 http://repo.radeon.com/amdgpu/6.4.1/ubuntu noble proprietary
    aptly -ignore-signatures mirror update agpro-6.4.1

    # Publish the mirror
    aptly publish drop noble || true
    aptly snapshot create snapshot-$(date +%F) from mirror agpro-6.4.1
    aptly publish --skip-signing snapshot snapshot-$(date +%F)

    # Unpack all deb packages
    ./unpack_all_deb_packages.sh

    # Generate packages map
    python3 concat_packages_extracted.py
    ./gen_packages_map.sh > packages_map.py

    # Generate dependency replacements
    ./gen_replace_deps.sh > replace_deps.py

    # Regenerate PKGBUILD
    mv update-local-repo.sh update-local-repo.sh.bak
    echo '#!/bin/bash' > update-local-repo.sh
    chmod +x update-local-repo.sh
    ./remake_all.sh
    mv update-local-repo.sh.bak update-local-repo.sh

    echo "Generating .SRCINFO..."
    makepkg --printsrcinfo > .SRCINFO
'

# Stop the container
docker-compose down 

if [ -f update-local-repo.sh.bak ]; then
    mv update-local-repo.sh.bak update-local-repo.sh
fi