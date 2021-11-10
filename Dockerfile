FROM archlinux

RUN set -e; \
    pacman --noconfirm -Sy; \
    pacman --noconfirm -S archlinux-keyring; \
    pacman --noconfirm -Su; \
    pacman-db-upgrade; \
    trust extract-compat; \
    pacman --noconfirm -S go-ipfs python python-pip nginx; \
    useradd -G daemon -s /bin/nologin -d /ipfs ipfs;

WORKDIR /ipfs

ADD static/nginx.conf /etc/nginx/nginx.conf
ADD static/pinner /srv/http/pinner

# Copy and install base requirements
COPY dist/*_lock*.whl /
RUN  pip install --no-cache-dir /*.whl \
    && rm /*.whl

# Copy and install package
COPY dist/*.whl /
RUN  pip install --no-cache-dir /*.whl \
    && rm /*.whl

VOLUME /ipfs

EXPOSE 80

CMD ["/usr/sbin/python", "-m", "ipfs_video_gateway.start"]
