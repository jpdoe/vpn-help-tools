#! /usr/bin/python

# Check that certificates match vpn configs
# Author: Jan Polák

import glob
import os
import re

os.system("")

REG_CRT = re.compile(
    r"-----BEGIN CERTIFICATE-----(?P<cert>[\s\S]*?)-----END CERTIFICATE-----"
)
REG_OVPN = re.compile(
    r"^<cert>\n-----BEGIN CERTIFICATE-----(?P<cert>[\s\S]*?)-----END CERTIFICATE-----",
    re.M,
)

CERT_DIR = "crt\\"
PREFIX = "prefix-"


class Colors:
    OKGREEN = "\033[92m"
    BADRED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def check_certs(certs):
    """Checks if certificate and configuration match"""
    path = certs + "*.crt"

    # add check for crt and opvn files
    # if crt dont exist, user will be not checked
    names = [os.path.splitext(os.path.basename(item))[0] for item in glob.glob(path)]

    for user in names:

        try:
            cert_crt = open(CERT_DIR + user + ".crt", "r").read()
        except FileNotFoundError as err:
            print(
                f"{Colors.BADRED}{Colors.BOLD}Cannot open crt file for {user}. {err}{Colors.ENDC}"
            )
            exit()

        try:
            cert_ovpn = open(CERT_DIR + PREFIX + user + "-config.ovpn", "r").read()

        except FileNotFoundError as err:

            print(
                f"{Colors.BADRED}Cannot open ovpn file for {user}. {err}{Colors.ENDC}"
            )
            exit()

        try:
            cert_crt_match = REG_CRT.search(cert_crt).group("cert")

        except AttributeError as err:
            print(f" {user}: Bad - regexp cannot match! {err}")

        try:
            cert_ovpn_match = REG_OVPN.search(cert_ovpn).group("cert")
        except AttributeError as err:

            print(f"{Colors.BADRED}Bad - regexp cannot match! {err}{Colors.ENDC}")

        if cert_crt_match == cert_ovpn_match:

            print(f"{Colors.OKGREEN}{user}: OK{Colors.ENDC}")

        else:

            print(f"{Colors.BADRED}{user}: BAD{Colors.ENDC}")


check_certs(CERT_DIR)
