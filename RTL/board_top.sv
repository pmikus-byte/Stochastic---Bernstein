module board_top (
    input logic CLK100MHZ,
    input logic [15:0] SW,
    input logic BTNC,
    output logic [15:0] LED
);

bernstein_top u_top (.clk(CLK100MHZ), .rst(BTNC), .t_thresh(SW[10:0]),
.count(LED[10:0]), .done(LED[15]));

assign LED[14:11] = 4'b0;

endmodule