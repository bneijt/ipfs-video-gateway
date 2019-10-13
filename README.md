Easy IPFS gateway and pinner
=================

These are Ansible scripts to set up your own [IPFS](https://ipfs.io/) gateway on a Debian server including a small web front-end that allows for pinning of IPFS content.

Installation
============

There are two ways of installing the gateway on a server: using the ansible script to remotely provision the server or using the cloud-init snippet below. The cloud-init snippet is the best approach for beginners.

Using cloud-init to provision on server creation
------------------------------------------------

You can use [cloud-init to configure a Scaleway server](https://www.scaleway.com/docs/how-to-use-cloud-init-to-configure-your-server-at-first-boot/) and have everything automatically done.

Copy paste the following cloud-init in the *Configure advanced options* section of the Scaleway new server form:

    #cloud-config
    packages:
      - ansible
      - git
      - whois
    package_update: true
    package_upgrade: true
    package_reboot_if_required: true
    runcmd:
      - "git clone https://github.com/bneijt/ipfs-video-gateway.git"
      - "cd ipfs-video-gateway && HOME=/root PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin ansible-playbook --connection=local --inventory=127.0.0.1, playbook.yml 2>&1|/usr/bin/tee /tmp/tee.log"
      - "echo admin:`mkpasswd -m sha-256 ADMINPASSWORDHERE` > /etc/nginx/htpasswd"

After starting the server, wait for a few minutes for the system to update, install and configure.

You should see the website come up and you should be able to start pinning content. To pin content you will be requested to
use a password for the user `admin`. The password is configured above by replacing `ADMINPASSWORDHERE` with the password you want.
If you forget to do this, the password will simply be the capital letters `ADMINPASSWORDHERE`.


Remote provision using local Ansible installation
-------------------------------------------------

- Locally install [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- Have a debian based server with SSH connectivity ready. You could [start a Scaleway Debian server](https://www.scaleway.com/docs/create-and-connect-to-your-server/), a Debian Stretch DEV1-S will do, but you can also use another already running server. Keep in mind however, that the provisioning will override the following: firewall configuration, nginx configuration, repository information
- Verify that you can ssh into your server
- Configure the user and ip address in `inventory.yml`
- Provision the server using `ansible-playbook --inventory-file=inventory.yml playbook.yml`

After provision has finished, you should be able to access the IPFS pinner web interface at your server ip.

Consider trying to pin [Qmb7yZdYZeRoLCvTvjwMzqeS4Jv9jeJuHKCBuUkHoAFhRh](https://ipfstube.erindachtler.me/v/Qmb7yZdYZeRoLCvTvjwMzqeS4Jv9jeJuHKCBuUkHoAFhRh)

**Please note**: Currently there is no security enabled! After provisioning anybody will be able to pin any content. You can disable pinning by chaning the `/etc/nginx.conf` file by removing the proxy to the ipfs api.
