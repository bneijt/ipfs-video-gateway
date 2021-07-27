Easily host files on IPFS
=========================

A docker container containing an HTTP gateway and IPFS node to easily host files on IPFS.

You run the docker container with a shared volume for the ipfs storage. If you add files
to the volume, they are added to ipfs, pinned and deleted.

Installation
============

Build with `docker build -t ipfs-video-gateway .`

Test with `docker run -p 4000:80 -it ipfs-video-gateway`

Using cloud-init to provision on server creation
------------------------------------------------

You can use [cloud-init to configure a Scaleway server](https://www.scaleway.com/docs/how-to-use-cloud-init-to-configure-your-server-at-first-boot/) and have everything automatically done.

Copy paste the following cloud-init in the *Configure advanced options* section of the Scaleway new server form:

  #cloud-config

  apt:
    sources:
      docker.list:
        source: deb [arch=amd64] https://download.docker.com/linux/ubuntu $RELEASE stable
        keyid: 9DC858229FC7DD38854AE2D88D81803C0EBFCD88

  packages:
    - apt-transport-https
    - ca-certificates
    - curl
    - gnupg-agent
    - software-properties-common
    - docker-ce
    - docker-ce-cli
    - containerd.io

  # Enable ipv4 forwarding, required on CIS hardened machines
  write_files:
    - path: /etc/sysctl.d/enabled_ipv4_forwarding.conf
      content: |
        net.ipv4.conf.all.forwarding=1

  # create the docker group
  groups:
    - docker

  # Add default auto created user to docker group
  system_info:
    default_user:
      groups: [docker]
  runcmd:
    - "docker run --volume /opt/ipfs:/ipfs --publish 80:80 -d --restart=always bneijt/ipfs-video-gateway"

After starting the server, wait for a few minutes for the system to update, install and configure.
