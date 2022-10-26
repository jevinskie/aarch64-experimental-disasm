import re
from pathlib import Path
from typing import Optional, Union

import lxml.objectify
from attrs import define
from lxml import objectify
from rich import print


@define
class Constraint:
    val: int
    neg: bool


@define
class Field:
    pos: int
    sz: int
    constraint: Optional[Constraint]
    name: Optional[str]


@define
class Encoding:
    mnemonic: str
    name: str
    path: Path
    pos_mask: int
    pos_val: int
    neg_mask: int
    neg_val: int
    fields: tuple[Field]


BINSTR_RE = re.compile("[01]+")
NE_BINSTR_RE = re.compile("!= [01]+")


def bitmask(pos: int, nbits: int) -> int:
    hi_mask = (1 << (pos + nbits)) - 1
    lo_mask = (1 << pos) - 1
    return hi_mask ^ lo_mask


def parse_box(box) -> Field:
    sz = 1 if "width" not in box.attrib else int(box.attrib["width"])
    pos = int(box.attrib["hibit"]) - sz
    name = None
    if "name" in box.attrib and "usename" in box.attrib:
        name = box.attrib["name"]
    if all(c.text is None for c in box.c):
        constraint = None
    else:
        if "constraint" in box.attrib:
            cstr = box.attrib["constraint"]
            if not cstr.startswith("!= "):
                constraint = Constraint(int(cstr, 2), False)
            else:
                cstr = cstr.removeprefix("!= ")
                constraint = Constraint(int(cstr, 2), True)
        else:
            cval = 0
            for c in box.c:
                cval = (cval << 1) | int(c.text, 2)
            constraint = Constraint(cval, False)
    return Field(pos, sz, constraint, name)


def parse_boxes(boxes: lxml.objectify.ObjectifiedElement) -> tuple[Field]:
    fields = []
    for b in boxes:
        fields.append(parse_box(b))
    return tuple(fields)


def parse_fields(fields: tuple[Field]) -> tuple[int, int, int, int]:
    pos_mask, pos_val, neg_mask, neg_val = 0, 0, 0, 0
    for f in fields:
        if f.constraint is None:
            continue
        c = f.constraint
        if not c.neg:
            pos_mask |= bitmask(f.pos, f.sz)
            pos_val |= c.val << f.pos
        else:
            neg_mask |= bitmask(f.pos, f.sz)
            neg_val |= c.val << f.pos
    return pos_mask, pos_val, neg_mask, neg_val


def parse_instruction_xml(xml_instsect_file: Path) -> tuple[Encoding]:
    encodings = []
    tree = objectify.parse(str(xml_instsect_file))
    root = tree.getroot()
    iclasses = root.classes.iclass
    for iclass in iclasses:
        path = iclass.regdiagram.attrib["psname"]
        path.replace("aarch64/instrs", "aarch64")
        path = Path(path).parent
        name = iclass.encoding.attrib["name"]
        mnemonic = next(
            filter(lambda dv: dv.attrib["key"] == "mnemonic", iclass.docvars.docvar)
        ).attrib["value"]
        fields = parse_boxes(iclass.regdiagram.box)
        pos_mask, pos_val, neg_mask, neg_val = parse_fields(fields)
        enc = Encoding(mnemonic, name, path, pos_mask, pos_val, neg_mask, neg_val, fields)
        encodings.append(enc)
    return tuple(encodings)


def parse_encodings_xml(xml_dir: Path) -> tuple[Encoding]:
    encodings = []
    return tuple(encodings)
