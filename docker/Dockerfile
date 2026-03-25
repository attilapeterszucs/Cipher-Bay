FROM debian:trixie-slim

# Install SSH server, sudo, and CODESYS runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    sudo \
    libgcc-s1 \
    libc6 \
    libpthread-stubs0-dev \
    libdbus-1-3 \
    udev \
    libcurl4 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create the codesys user with a password and sudo rights
ARG CODESYS_USER=codesys
ARG CODESYS_PASSWORD=codesys

RUN useradd -m -s /bin/bash ${CODESYS_USER} && \
    echo "${CODESYS_USER}:${CODESYS_PASSWORD}" | chpasswd && \
    usermod -aG sudo ${CODESYS_USER} && \
    echo "${CODESYS_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Prepare SSH daemon
RUN mkdir -p /var/run/sshd && \
    # Allow password authentication
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    # Allow root login (needed by CODESYS installer)
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    # Disable PAM to avoid login issues inside Docker
    sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config && \
    # Generate host keys
    ssh-keygen -A

# Create CODESYS data directory
RUN mkdir -p /var/opt/codesys/PlcLogic && \
    chown -R ${CODESYS_USER}:${CODESYS_USER} /var/opt/codesys

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
