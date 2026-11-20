module lfsr #(parameter SEED =  10'd1 ) (
    input clk, rst,
    output logic [9:0] q
);

logic feedback;
assign feedback = q[9] ^ q[6];

always_ff @(posedge clk) 
    if (rst) 
        q <= SEED;
    else
        q <= {q[8:0], feedback};

endmodule