#!/usr/bin/env python3

import argparse
from pathlib import Path

from aarch64_experimental_disasm import mra_encoding_xml
from rich import print


def real_main(args):
    if args.xml_dir is not None:
        encs = mra_encoding_xml.parse_encodings_xml(args.xml_dir)
        print(encs)
    elif args.xml_inst is not None:
        encs = mra_encoding_xml.parse_instruction_xml(args.xml_inst)
        print(encs)


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="aarch64-dump-instrs")
    parser.add_argument("-x", "--xml-dir", type=Path, help="MRA XML directory")
    parser.add_argument("-i", "--xml-inst", type=Path, help="MRA XML instruction file")
    return parser


def main():
    real_main(get_arg_parser().parse_args())


if __name__ == "__main__":
    main()
