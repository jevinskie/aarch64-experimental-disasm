import re
from pathlib import Path
from typing import Optional, Union

import lxml.objectify
from attrs import define
from lxml import objectify
from rich import print


@define
class Constraint:
    pos: int
    sz: int
    val: int
    neg: bool


@define
class Field:
    pos: int
    sz: int
    constraints: Optional[tuple[Constraint]]
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

    @property
    def pos_mask_str(self) -> str:
        return f"{self.pos_mask:#010x}"

    @property
    def pos_val_str(self) -> str:
        return f"{self.pos_val:#010x}"

    @property
    def neg_mask_str(self) -> str:
        return f"{self.neg_mask:#010x}"

    @property
    def neg_val_str(self) -> str:
        return f"{self.neg_val:#010x}"


def bitmask(pos: int, nbits: int) -> int:
    hi_mask = (1 << (pos + nbits)) - 1
    lo_mask = (1 << pos) - 1
    return hi_mask ^ lo_mask


# FIXME
def pack_constraints(constraints: list[Constraint]) -> list[Constraint]:
    orig = constraints
    packed = constraints.copy()
    csz = len(constraints)
    i = 0
    while True:
        if i + 1 >= csz:
            break
        j = i
        val = orig[j].val
        sz = orig[j].sz
        while j < csz - 1:
            if orig[j].pos - orig[j].sz == orig[j + 1].pos and orig[j].neg == orig[j + 1].neg:
                val = (val << orig[j].sz) | orig[j + 1].val
                sz += orig[j + 1].sz
                j += 1
            else:
                break
        if j != i:
            packed[: j - i + 1] = [Constraint(orig[j].pos, sz, val, orig[i].neg)]
        i = j + 1
    return packed


def parse_box(box) -> Field:
    sz = 1 if "width" not in box.attrib else int(box.attrib["width"])
    pos = int(box.attrib["hibit"]) - (sz - 1)
    name = None
    if "name" in box.attrib and "usename" in box.attrib:
        name = box.attrib["name"]
    if all(c.text is None for c in box.c):
        constraints = None
    else:
        if "constraint" in box.attrib:
            cstr = box.attrib["constraint"]
            neg = cstr.startswith("!= ")
            cstr = cstr.removeprefix("!= ")
            constraints = []
            csz = len(cstr)
            for i, b in enumerate(cstr):
                if b == "0":
                    constraints.append(Constraint(csz - i - 1, 1, 0, neg))
                elif b == "1":
                    constraints.append(Constraint(csz - i - 1, 1, 1, neg))
                elif b == "x":
                    pass
                else:
                    raise ValueError(f"got weird bit '{b}'")
            constraints = pack_constraints(constraints)
        else:
            constraints = []
            csz = len(box.c)
            for i, c in enumerate(box.c):
                if c.text == "0" or c.text == "(0)":
                    constraints.append(Constraint(csz - i - 1, 1, 0, False))
                elif c.text == "1" or c.text == "(1)":
                    constraints.append(Constraint(csz - i - 1, 1, 1, False))
                elif c.text == "x" or c.text == "(x)":
                    pass
                else:
                    raise ValueError(f"got weird bit '{c.text}'")
            constraints = pack_constraints(constraints)
    return Field(pos, sz, constraints, name)


def parse_boxes(boxes: lxml.objectify.ObjectifiedElement) -> tuple[Field]:
    fields = []
    for b in boxes:
        fields.append(parse_box(b))
    return tuple(fields)


def parse_fields(fields: tuple[Field]) -> tuple[int, int, int, int]:
    pos_mask, pos_val, neg_mask, neg_val = 0, 0, 0, 0
    for f in fields:
        if f.constraints is None:
            continue
        c = f.constraints
        for sub_c in c:
            if not sub_c.neg:
                pos_mask |= bitmask(f.pos + sub_c.pos, sub_c.sz)
                pos_val |= sub_c.val << (f.pos + sub_c.pos)
            else:
                neg_mask |= bitmask(f.pos + sub_c.pos, sub_c.sz)
                neg_val |= sub_c.val << (f.pos + sub_c.pos)
    return pos_mask, pos_val, neg_mask, neg_val


def parse_instruction_xml(xml_instsect_file: Path) -> list[Encoding]:
    encodings = []
    tree = objectify.parse(str(xml_instsect_file))
    if tree.docinfo.internalDTD.system_url != "iform-p.dtd":
        return []
    root = tree.getroot()
    classes = root.find("classes")
    if classes is None:
        return []
    iclasses = classes.iclass
    for iclass in iclasses:
        path = iclass.regdiagram.attrib["psname"]
        path = path.replace("aarch64/instrs", "aarch64")
        path = Path(path).parent
        name = iclass.encoding.attrib["name"]
        mnemonic = next(
            filter(lambda dv: dv.attrib["key"] == "mnemonic", iclass.encoding.docvars.docvar)
        ).attrib["value"]
        fields = parse_boxes(iclass.regdiagram.box)
        pos_mask, pos_val, neg_mask, neg_val = parse_fields(fields)
        enc = Encoding(mnemonic, name, path, pos_mask, pos_val, neg_mask, neg_val, fields)
        encodings.append(enc)
    return encodings


def parse_encodings_xml(xml_dir: Path) -> list[Encoding]:
    encodings = []
    xml_files = xml_dir.glob("*.xml")
    for f in xml_files:
        encodings += parse_instruction_xml(f)
    return encodings
