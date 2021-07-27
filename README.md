Easily host files on IPFS
=========================

A docker container containing an HTTP gateway and IPFS node to easily host files on IPFS.

You run the docker container with a shared volume for the ipfs storage. If you add files
to the volume, they are added to ipfs, pinned and deleted.

Usage
-----

Start with `docker run --volume /opt/ipfs:/ipfs --publish 4000:80 bneijt/ipfs-video-gateway`
and visit [localhost:4000](http://localhost:4000) to view the front-end.

Development
-----------

See [`test.sh`](test.sh)

Using cloud-init to provision on server creation
------------------------------------------------

You can use [cloud-init to configure a Scaleway server](https://www.scaleway.com/docs/how-to-use-cloud-init-to-configure-your-server-at-first-boot/) and have everything automatically done.

Copy paste the following cloud-init in the *Configure advanced options* section of the Scaleway new server form:

  #cloud-config

  packages:
    - docker.io

  runcmd:
    - "docker run --volume /opt/ipfs:/ipfs --publish 80:80 -d --restart=always bneijt/ipfs-video-gateway"

After starting the server, wait for a few minutes for the system to update, install and configure.

Adding files
------------
You can add files to the /opt/ipfs folder to have them automatically (after a few seconds) added to ipfs. For example, to upload a local folder to your ipfs node using rsync:

  rsync --progress -r folder_to_add root@51.158.172.172:/opt/ipfs/

