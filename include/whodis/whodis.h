#pragma once

#include <cstdint>

namespace whodis {

enum enc_t : uint16_t;

struct EncodingBits {
    uint32_t pos_mask;
    uint32_t pos_val;
    uint32_t neg_mask;
    uint32_t neg_val;
};

#include "encodings.h"

constexpr uint16_t get_idx(uint32_t instr) {
    for (uint16_t i = UNDEFINED + 1; i < ENC_MAX; ++i) {
        if (((instr & encoding_bits[i].pos_mask) == encoding_bits[i].pos_val) &&
            ((instr & encoding_bits[i].neg_mask) != encoding_bits[i].neg_val)) {
            return i;
        }
    }
    return UNDEFINED;
}

constexpr uint16_t get_idx_unrolled(uint32_t instr) {
#pragma unroll
    for (uint16_t i = UNDEFINED + 1; i < ENC_MAX; ++i) {
        if (((instr & encoding_bits[i].pos_mask) == encoding_bits[i].pos_val) &&
            ((instr & encoding_bits[i].neg_mask) != encoding_bits[i].neg_val)) {
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
        if (((instr & encoding_bits[i].pos_mask) == encoding_bits[i].pos_val) &&
            ((instr & encoding_bits[i].neg_mask) != encoding_bits[i].neg_val)) {
            ++num;
        }
    }
    return num;
}

} // namespace whodis
