#!/usr/bin/env python3

import argparse
from pathlib import Path

from aarch64_experimental_disasm.mra_encoding_xml import *
from rich import print


def print_encoding(enc: Encoding):
    pm = enc.pos_mask
    pv = enc.pos_val
    nm = enc.neg_mask
    nv = enc.neg_val
    pmbs = f"{pm:#034b}"[2:]
    pvbs = f"{pv:#034b}"[2:]
    nmbs = f"{nm:#034b}"[2:]
    nvbs = f"{nv:#034b}"[2:]
    bs = ["-"] * 32
    for i in range(32):
        assert not (nmbs[i] == "1" and pmbs[i] == "1")
        if nmbs[i] == "1":
            if nvbs[i] == "0":
                bs[i] = "*"
            else:
                bs[i] = "|"
        elif pmbs[i] == "1":
            if pvbs[i] == "0":
                bs[i] = "0"
            else:
                bs[i] = "1"
    bs = "".join(bs)
    print(f"{bs};{enc.mnemonic};{enc.name}")


def real_main(args):
    if args.xml_dir is not None:
        encs = parse_encodings_xml(args.xml_dir)
        # print(encs)
        for enc in encs:
            print_encoding(enc)
    elif args.xml_inst is not None:
        encs = parse_instruction_xml(args.xml_inst)
        print(encs)
        for enc in encs:
            print_encoding(enc)


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="aarch64-dump-instrs")
    parser.add_argument("-x", "--xml-dir", type=Path, help="MRA XML directory")
    parser.add_argument("-i", "--xml-inst", type=Path, help="MRA XML instruction file")
    return parser


def main():
    real_main(get_arg_parser().parse_args())


if __name__ == "__main__":
    main()
