#!/usr/bin/env python

import os
import logging
import typing


## NGINX_CONFIG_FILES
#
# nginx config files need to be parsed
# should be path string join by ";"
#
NGINX_CONFIG_FILES = os.environ.get("NGINX_CONFIG_FILES", "")


## EXCLUDE_DOMAINS
#
# certbot not goona process thos domains
#
EXCLUDE_DOMAINS = os.environ.get("EXCLUDE_DOMAINS", "")


## DNS Owner Mail
#
DNS_EMAIL = os.environ.get("DNS_EMAIL", "mori@mori.mail")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_nginx_configs():

    logger.info("try start parse nginx config")

    logger.info(f"get nginx configs from env: {NGINX_CONFIG_FILES}")

    server_names = []

    import re
    import itertools

    server_name_regex = re.compile(r"server_name\s+([^;]+);")

    # find through all config files
    for nginx_config_file in NGINX_CONFIG_FILES.split(";"):
        if not os.path.exists(nginx_config_file):
            continue

        with open(nginx_config_file, "r") as _f:
            re_find_result = server_name_regex.findall(_f.read())
            # split batch name to one by one
            server_names.extend(
                itertools.chain(*[i.split(" ") for i in re_find_result])
            )

    server_names = [i.strip() for i in server_names]
    server_names = [i for i in server_names if len(i) > 0]
    logger.info(f"parsed {len(server_names)} from configs: {server_names}")
    return server_names


def run_certbot(server_names: typing.List[str]):

    args = ["certbot", "certonly", "--standalone"]

    # append servernames
    for server_name in server_names:
        args.extend(["-d", server_name])

    args.extend(["-m", DNS_EMAIL, "--non-interactive", "--agree-tos", "--staging"])

    print(" ".join(args))
    # args.append


if __name__ == "__main__":
    server_names = parse_nginx_configs()
    run_certbot(server_names)
