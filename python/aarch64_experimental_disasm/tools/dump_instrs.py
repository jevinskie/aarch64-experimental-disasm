#!/usr/bin/env python3

import argparse

from aarch64_experimental_disasm import mra_encoding_xml


def real_main(args):
    encs = mra_encoding_xml.parse_encodings_xml(args.xml_dir)
    print(encs)


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="aarch64-dump-instrs")
    parser.add_argument("-x", "--xml-dir", required=True, help="MRA XML directory")
    return parser


def main():
    real_main(get_arg_parser().parse_args())


if __name__ == "__main__":
    main()
