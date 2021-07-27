#!/usr/bin/python3
import logging
import sys
import os
import time
import subprocess
import pwd
from typing import Callable, Optional, List
import shutil

IPFS_HOME = "/ipfs"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("START")


def checked_run(proc: subprocess.Popen):
    proc.wait()
    if proc.returncode != 0:
        raise Exception(f"Failure trying to execute: {str(proc.args)}")
    return proc


def init_ipfs() -> Optional[subprocess.Popen]:
    if not os.path.exists(os.path.join(IPFS_HOME, ".ipfs")):
        logger.info("Initializing ipfs")
        return as_ipfs(
            "ipfs init --empty-repo --profile flatfs,server",
        )
    return None


def start_ipfs():
    return as_ipfs("ipfs daemon --enable-gc")


def as_ipfs(cmd: str) -> subprocess.Popen:
    return subprocess.Popen(["su", "-s", "/bin/bash", "-g", "ipfs", "-c", cmd, "ipfs"])


def start_nginx():
    return subprocess.Popen(["nginx"])


def wait_for_either(processList: List[subprocess.Popen], in_between: Callable):
    while True:
        for p in processList:
            try:
                return p.wait(10)
            except subprocess.TimeoutExpired:
                pass
        in_between()


def check_for_new_files():
    for name in os.listdir(IPFS_HOME):
        if name.startswith("."):
            continue
        file_path = os.path.join(IPFS_HOME, name)
        logger.info(f"Adding '{file_path}'")
        checked_run(as_ipfs(f"ipfs add --recursive --wrap-with-directory --silent --pin '{file_path}'"))
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.unlink(file_path)


def main():
    checked_run(subprocess.Popen(["chown", "ipfs", IPFS_HOME]))
    checked_run(subprocess.Popen(["chmod", "u+rwx,g+rwx", IPFS_HOME]))

    ipfs_init_process = init_ipfs()
    nginx_process = start_nginx()
    if ipfs_init_process:
        ipfs_init_process.wait()
    ipfs_process = start_ipfs()
    wait_for_either([ipfs_process, nginx_process], check_for_new_files)
    nginx_process.terminate()
    return 0


if __name__ == "__main__":
    sys.exit(main())
