FROM archlinux:latest

# Install base dependencies
RUN pacman -Syu --noconfirm \
    base-devel \
    python \
    python-pip \
    python-debian \
    dpkg \
    git \
    sudo \
    fakeroot \
    wget \
    which \
    expac \
    pacman-contrib

# Create a build user for yay
RUN useradd -m builder && echo "builder ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/builder
USER builder
WORKDIR /home/builder

# Install yay (AUR helper)
RUN git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si --noconfirm

# Install AUR packages: aptly and debtap
RUN yay -S --noconfirm aptly debtap

USER root
WORKDIR /build

# Copy the repository files
COPY . .

# Set up the build environment
RUN chown -R builder:builder /build && ./reposetup.sh

# Verify expac is available
RUN which expac || (echo "expac not found" && exit 1)

# Default command
CMD ["/bin/bash"] 