Easy IPFS gateway and pinner
=================

These are Ansible scripts to set up your own [IPFS](https://ipfs.io/) gateway on a Debian server including a small web front-end that allows for pinning of IPFS content.

Installation
============

Using cloud-init
---------------

You can use [cloud-init to configure a Scaleway server](https://www.scaleway.com/docs/how-to-use-cloud-init-to-configure-your-server-at-first-boot/) and have everything automatically done.

Copy paste the following cloud-init in the *Configure advanced options* section of the Scaleway new server form:

    #cloud-config
    packages:
      - ansible
      - git
      - sudo
    package_update: true
    package_upgrade: true
    package_reboot_if_required: true
    runcmd:
      - "git clone https://github.com/bneijt/ipfs-video-gateway.git"
      - "cd ipfs-video-gateway && ansible-playbook --connection=local --inventory=127.0.0.1, playbook.yml"




To remote server via local Ansible
--------------------------
- Locally install [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- [Start a Scaleway Debian server](https://www.scaleway.com/docs/create-and-connect-to-your-server/), a Debian Stretch START1-XS will do
- Verify that you can ssh into your server
- Configure the user and ip address in `inventory.yml`
- Provision the server using `ansible-playbook --inventory-file=inventory.yml playbook.yml`

After provision has finished, you should be able to access the IPFS pinner web interface at your server ip.

Consider trying to pin [Qmb7yZdYZeRoLCvTvjwMzqeS4Jv9jeJuHKCBuUkHoAFhRh](https://ipfstube.erindachtler.me/v/Qmb7yZdYZeRoLCvTvjwMzqeS4Jv9jeJuHKCBuUkHoAFhRh)

**Please note**: Currently there is no security enabled!
