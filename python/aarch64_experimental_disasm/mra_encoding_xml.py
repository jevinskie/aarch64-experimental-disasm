import re
from pathlib import Path
from typing import Optional, Union

from attrs import define
from lxml import objectify
from rich import print


@define
class Constraint:
    val: int
    ne: bool


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


def parse_boxes(box) -> tuple[Field]:
    return ()


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
        boxes = iclass.regdiagram.box
        fields = parse_boxes(boxes)
        pos_mask, pos_val, neg_mask, neg_val = parse_fields(fields)
        enc = Encoding(mnemonic, name, path, pos_mask, pos_val, neg_mask, neg_val, fields)
        print(iclass)
    return tuple(*encodings)


def c_val(box) -> Union[None, int]:
    assert "constraint" not in box.attrib
    if all(c.text is None for c in box.c):
        return None
    bitstr = ""
    for c in box.c:
        assert BINSTR_RE.fullmatch(c.text)
        bitstr += c.text
    return int(bitstr, 2)


def parse_encodings_xml(xml_dir: Path) -> tuple[Encoding]:
    enc_xml_path = xml_dir / "encodingindex.xml"
    tree = objectify.parse(str(enc_xml_path))
    root = tree.getroot()
    iclass_sects = root.iclass_sect
    for iclass in iclass_sects:
        if iclass.attrib["id"] != "compbranch":
            continue
        rd = iclass.regdiagram
        print(rd.attrib["psname"])
        for b in rd.box:
            width = 1 if "width" not in b.attrib else int(b.attrib["width"])
            hibit = int(b.attrib["hibit"])
            lobit = hibit - (width - 1)
            name = None if "name" not in b.attrib else b.attrib["name"]
            bval = c_val(b)
            bval_str = "None" if bval is None else f"{bval:0{width}b}"
            print(f"field {name} [{lobit}, {hibit}] bval: {bval_str}")

    encodings = []

    return tuple(*encodings)
