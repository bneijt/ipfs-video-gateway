#!/usr/bin/python3
import logging
import sys
import os
import subprocess
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


def start_ipfs() -> subprocess.Popen:
    return as_ipfs("ipfs daemon --enable-gc")


def as_ipfs(cmd: str) -> subprocess.Popen:
    return subprocess.Popen(["su", "-s", "/bin/bash", "-g", "ipfs", "-c", cmd, "ipfs"])


def start_nginx() -> subprocess.Popen:
    return subprocess.Popen(["nginx"])


def wait_for_either(processList: List[subprocess.Popen], in_between: Callable):
    while True:
        for p in processList:
            try:
                return p.wait(10)
            except subprocess.TimeoutExpired:
                pass
        in_between()


def is_hidden_or_part_file(file_name: str) -> bool:
    return file_name.startswith(".") or file_name.endswith(".part")


def contains_files(path: str, matcher: Callable[[str], bool]) -> bool:
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            if any(map(matcher, dirs + files)):
                return True
    return matcher(os.path.basename(path))


def check_for_new_files() -> None:
    for name in os.listdir(IPFS_HOME):
        if name.startswith(".") or name.endswith(".part"):
            continue
        file_path = os.path.join(IPFS_HOME, name)

        # We ignore the directory if it contains hidden files
        # and example of this is partial rsync uploads
        if contains_files(name, is_hidden_or_part_file):
            logger.info(
                f"Ignoring '{file_path}' because it contains hidden or partial files"
            )
            sys.stdout.flush()
            continue

        logger.info(f"Adding '{file_path}'")
        sys.stdout.flush()
        checked_run(
            as_ipfs(
                f"ipfs add --recursive --wrap-with-directory --silent --pin '{file_path}'"
            )
        )
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
