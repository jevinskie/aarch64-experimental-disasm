from pathlib import Path

import jinja2

from .mra_encoding_xml import Constraint, Encoding, Field


def hex32(u32: int) -> str:
    return f"{u32:#010x}"


def gen_cpp(header_path: Path, encodings: list[Encoding]) -> None:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(Path(__file__).parent / "templates"))
    )
    template = env.get_template("cpp_gen.cpp.jinja2")
    cpp = template.render(encs=encodings)
    with open(header_path, "w") as hdr:
        hdr.write(cpp)
