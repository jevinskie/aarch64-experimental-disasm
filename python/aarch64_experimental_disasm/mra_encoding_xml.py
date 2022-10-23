import re
from pathlib import Path
from typing import Union

from attrs import define
from lxml import objectify


@define
class Encoding:
    mnemonic: str
    name: str
    pos_bitmask: int
    pos_bitpattern: int
    neg_bitmask: int
    neg_bitpattern: int


BINSTR_RE = re.compile("[01]+")


def c_val(box) -> Union[None, int]:
    assert "constraint" not in box.attrib
    if all(c.text is None for c in box.c):
        return None
    bitstr = ""
    for c in box.c:
        assert BINSTR_RE.fullmatch(c.text)
        bitstr += c.text
    return int(bitstr, 2)


def parse_encodings_xml(xml_dir: str) -> list[Encoding]:
    enc_xml_path = Path(xml_dir) / "encodingindex.xml"
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

    return encodings
