Easy personal IPFS gateway setup
=================

These are Ansible scripts to set up your own IPFS gateway on a Debian server.

Installation
============

- Locally install [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- [Start a Scaleway Debian server](https://www.scaleway.com/docs/create-and-connect-to-your-server/), a Debian Stretch START1-XS will do
- Verify that you can ssh into your server
- Configure the user (probably root) and ip address in `inventory.yml`
- Provision the server using `ansible-playbook --inventory-file=inventory.yml playbook.yml`

After provision has finished, you should be able to access `http://`_IP address of your server_`/ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme`
