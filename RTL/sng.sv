
module sng #(parameter SEED = 10'd1) (
    input clk, rst,
    input [10:0] thresh,
    output stream
);

logic [9:0] r;

lfsr #(.SEED(SEED)) u_lfsr (.clk(clk), .rst(rst), .q(r));


assign stream = (r < thresh);

endmodule