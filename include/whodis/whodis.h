#pragma once

#include <cstdint>

namespace whodis {

struct EncodingBits {
    uint32_t pos_mask;
    uint32_t pos_val;
    uint32_t neg_mask;
    uint32_t neg_val;
};

#include "encodings.h"

} // namespace whodis
