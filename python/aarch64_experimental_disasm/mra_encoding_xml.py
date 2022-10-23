from pathlib import Path

from attrs import define
from lxml import etree, objectify


@define
class Encoding:
    mnemonic: str
    name: str
    pos_bitmask: int
    pos_bitpattern: int
    neg_bitmask: int
    neg_bitpattern: int


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
            print(f"field [{lobit}, {hibit}]")

    encodings = []

    return encodings
