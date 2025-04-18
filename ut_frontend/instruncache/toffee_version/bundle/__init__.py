from toffee import Bundle, Signals, Signal

class InstrUncacheIOBundle(Bundle):

    clock, \
    reset, \
    auto_client_out_a_ready, \
    auto_client_out_a_valid, \
    auto_client_out_a_bits_address, \
    auto_client_out_d_ready, \
    auto_client_out_d_valid, \
    auto_client_out_d_bits_source, \
    auto_client_out_d_bits_data, \
    io_req_ready, \
    io_req_valid, \
    io_req_bits_addr, \
    io_resp_valid, \
    io_resp_bits_data = Signals(14)

