#pragma once

#include <cstdint>
#include <set>

namespace whodis {

enum enc_t : uint16_t;

struct EncodingBits {
    uint32_t pos_mask;
    uint32_t pos_val;
    uint32_t neg_mask;
    uint32_t neg_val;
};

#include "encodings.h"

constexpr bool matches_bits(uint32_t instr, const EncodingBits &enc_bits) {
    return ((instr & enc_bits.pos_mask) == enc_bits.pos_val) &&
           ((instr & enc_bits.neg_mask) != enc_bits.neg_val);
}

constexpr uint16_t get_idx(uint32_t instr) {
    for (uint16_t i = UNDEFINED + 1; i < ENC_MAX; ++i) {
        if (matches_bits(instr, encoding_bits[i])) {
            return i;
        }
    }
    return UNDEFINED;
}

constexpr uint16_t get_idx_unrolled(uint32_t instr) {
#pragma unroll 4
    for (uint16_t i = UNDEFINED + 1; i < ENC_MAX; ++i) {
        if (matches_bits(instr, encoding_bits[i])) {
            return i;
        }
    }
    return UNDEFINED;
}

constexpr const char *get_name(uint32_t instr) {
    return encoding_names[get_idx(instr)];
}

constexpr const char *get_mnemonic(uint32_t instr) {
    return encoding_mnemonics[get_idx(instr)];
}

constexpr uint16_t get_num_matching(uint32_t instr) {
    uint16_t num = 0;
#pragma unroll 4
    for (uint16_t i = UNDEFINED + 1; i < ENC_MAX; ++i) {
        if (matches_bits(instr, encoding_bits[i])) {
            ++num;
        }
    }
    return num;
}

inline std::set<uint16_t> get_all_matching(uint32_t instr) {
    std::set<uint16_t> res;
    for (uint16_t i = UNDEFINED + 1; i < ENC_MAX; ++i) {
        if (matches_bits(instr, encoding_bits[i])) {
            res.emplace(i);
        }
    }
    return res;
}

} // namespace whodis
