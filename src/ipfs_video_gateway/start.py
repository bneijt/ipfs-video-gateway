#!/usr/bin/python3
import logging
import os
import shutil
import subprocess
import sys
from typing import Callable, List, Optional

IPFS_HOME = "/ipfs"
FOLDER_STATUS_CACHE = {}

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
        init_commands = [
            "ipfs init --empty-repo --profile flatfs,server",
            "ipfs config Addresses.API /ip4/0.0.0.0/tcp/5001",
            "ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/8080",
        ]

        for ic in init_commands:
            checked_run(as_ipfs(ic))
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


def ipfs_add(file_path: str):
    logger.info(f"Adding '{file_path}'")
    sys.stdout.flush()
    checked_run(
        as_ipfs(
            f"ipfs add --recursive --wrap-with-directory --silent --pin '{file_path}'"
        )
    )


def is_stable(path: str, forget: bool = False) -> bool:
    global FOLDER_STATUS_CACHE
    if forget:
        if path in FOLDER_STATUS_CACHE:
            del FOLDER_STATUS_CACHE[path]
        return
    current_status = "#".join(
        [
            "#".join(
                [
                    f"{name}={os.path.getsize(os.path.join(root, name))}"
                    for name in sorted(files)
                ]
            )
            for root, _, files in os.walk(path)
        ]
    )
    old_state = FOLDER_STATUS_CACHE.get(path)
    FOLDER_STATUS_CACHE[path] = current_status
    return old_state is not None and old_state == current_status


def check_for_new_files() -> None:
    for name in os.listdir(IPFS_HOME):
        if name.startswith(".") or name.endswith(".part"):
            continue
        file_path = os.path.join(IPFS_HOME, name)

        if os.path.isdir(file_path):
            if not contains_files(name, is_hidden_or_part_file):
                if is_stable(file_path):
                    ipfs_add(file_path)
                    shutil.rmtree(file_path)
                    is_stable(file_path, forget=True)
                else:
                    logger.info(
                        f"Ignoring '{file_path}' because it has changing content"
                    )

            else:
                logger.info(
                    f"Ignoring '{file_path}' because it contains hidden or partial files"
                )
                sys.stdout.flush()
                continue

        else:
            if not is_hidden_or_part_file(file_path):
                ipfs_add(file_path)
                os.unlink(file_path)
            else:
                logger.info(
                    f"Ignoring '{file_path}' because it contains hidden or partial files"
                )
                sys.stdout.flush()
                continue


def main():
    enable_nginx = "DISABLE_NGINX" not in os.environ

    checked_run(subprocess.Popen(["chown", "ipfs", IPFS_HOME]))
    checked_run(subprocess.Popen(["chmod", "u+rwx,g+rwx", IPFS_HOME]))

    init_ipfs()
    subprocess_list = []  # type: List[subprocess.Popen]

    if enable_nginx:
        subprocess_list.append(start_nginx())

    subprocess_list.append(start_ipfs())
    wait_for_either(subprocess_list, check_for_new_files)
    for sp in subprocess_list:
        sp.terminate()
    return 0


if __name__ == "__main__":
    sys.exit(main())
