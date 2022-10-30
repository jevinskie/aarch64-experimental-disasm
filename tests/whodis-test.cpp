#include <cerrno>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <string>

#include <fmt/format.h>

#include <argparse/argparse.hpp>
#include <scn/scn.h>
#include <whodis/whodis.h>

namespace fs = std::filesystem;

int main(int argc, const char **argv) {
    argparse::ArgumentParser parser(getprogname());
    parser.add_argument("-I", "--instr-list").help("input list of instructions to decode");
    parser.add_argument("-b", "--brute-force")
        .default_value(false)
        .implicit_value(true)
        .help("brute-force 2^32 test");

    try {
        parser.parse_args(argc, argv);
    } catch (const std::runtime_error &err) {
        fmt::print(stderr, "Error parsing arguments: {:s}\n", err.what());
        return -1;
    }

    const auto instr_list = parser.present<std::string>("--instr-list");
    const auto brute      = parser["--brute-force"] == true;

    if (instr_list) {
        // scn::basic_owning_file<char> file{instr_list->c_str(), "r"};
        // std::string line;
        // while (true) {
        //     auto lres = scn::getline(file, line);
        //     if (lres.error() == scn::error::end_of_range) {
        //         break;
        //     }
        //     fmt::print("line: {:s}\n", line);
        // }

        std::ifstream f;
        f.open(*instr_list);
        if (!f) {
            fmt::print(stderr, "Error opening '{:s}': {:s}\n", *instr_list, strerror(errno));
            return -2;
        }

        for (std::string line; std::getline(f, line);) {
            fmt::print("l: {:s}\n", line);
        }
    }

    if (brute) {
        for (uint64_t inst64 = 0; inst64 <= 0xffff'ffff; ++inst64) {
            uint32_t inst = (uint32_t)inst64;
            if ((inst & 0xf'ffff) == 0) {
                fmt::print("{:#010x}\n", inst);
            }
            if (uint16_t nm = whodis::get_num_matching(inst); nm > 1) {
                fmt::print("instr: {:#010x} {:s} {:s} num matching: {:d}\n", inst,
                           whodis::get_name(inst), whodis::get_mnemonic(inst), nm);
            }
        }
    }

    return 0;
}
