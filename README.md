Easily host files on IPFS
=========================

A docker container containing an HTTP gateway and IPFS node to easily host files on IPFS.

You run the docker container with a shared volume for the ipfs storage. If you add files
to the volume, they are added to ipfs, pinned and deleted.

Installation
============

The software is packages as a docker container. Pick any of the following options to start the docker container.

Locally
-------

Test run with `docker run --volume /opt/ipfs:/ipfs --publish 4000:80 bneijt/ipfs-video-gateway`
and visit [localhost:4000](http://localhost:4000) to view the front-end.

If you like it, use daemonize and restart to make it more permanent:

    docker run --volume /opt/ipfs:/ipfs --publish 4000:80 -d --restart=always bneijt/ipfs-video-gateway

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

Usage
=====

The docker container will check to see if there are files in `/ipfs` every 10 seconds or so. If there is a directory of file, and none of the files are hidden or end with `.part` it will add the files to IPFS and delete the folder.

If you have provisioned a server using cloud-init, you can rsync files to it using:

    rsync --progress -r folder_to_add root@ip_of_server:/opt/ipfs/

of if you are running the files locally, use `rsync --progress -r folder_to_add /opt/ipfs/`. **Remember: files in /opt/ipfs will be deleted after adding them to the ipfs index**.

If you have not used `--volume` when starting docker, you can upload the files into the container using [docker cp](https://docs.docker.com/engine/reference/commandline/cp/)

    docker ps # to find out the container id
    docker cp directory container_id:/ipfs


Development
===========

Update files in `src`, test using [`test.sh`](test.sh)
