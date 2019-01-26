Easy IPFS gateway and pinner
=================

These are Ansible scripts to set up your own [IPFS](https://ipfs.io/) gateway on a Debian server including a small web front-end that allows for pinning of IPFS content.

Installation
============

- Locally install [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- [Start a Scaleway Debian server](https://www.scaleway.com/docs/create-and-connect-to-your-server/), a Debian Stretch START1-XS will do
- Verify that you can ssh into your server
- Configure the user and ip address in `inventory.yml`
- Provision the server using `ansible-playbook --inventory-file=inventory.yml playbook.yml`

After provision has finished, you should be able to access the IPFS pinner web interface at your server ip.

**Please note**: Currently there is no security enabled!
