FROM archlinux

RUN set -e; \
    pacman --noconfirm -Sy; \
    pacman --noconfirm -S archlinux-keyring; \
    pacman --noconfirm -Su; \
    pacman-db-upgrade; \
    trust extract-compat; \
    pacman --noconfirm -S go-ipfs python nginx; \
    useradd -G daemon -s /bin/nologin -d /ipfs ipfs;

WORKDIR /ipfs

ADD src/start.py /
ADD src/nginx.conf /etc/nginx/nginx.conf
ADD src/pinner /srv/http/pinner

VOLUME /ipfs

EXPOSE 80

CMD ["/usr/sbin/python", "/start.py"]
