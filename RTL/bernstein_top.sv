module bernstein_top #(
    parameter B0 = 11'd0,
    parameter B1 = 11'd724,
    parameter B2 = 11'd1024,
    parameter B3 = 11'd724,
    parameter B4 = 11'd0
) (
    input  logic clk, rst,
    input  logic [10:0] t_thresh,
    output logic [10:0] count,
    output logic done
);

    logic [3:0] x; // 4 input streams
    logic [4:0] z; // 5 coefficient streams
    logic [2:0] sel;// adder output, 0 to 4
    logic y;   // MUX output
    logic [10:0] cycles;  // cycle counter

    //Four input SNGs
    sng #(.SEED(10'd1)) u_in0 (.clk(clk), .rst(rst), .thresh(t_thresh), .stream(x[0]));
    sng #(.SEED(10'd111)) u_in1 (.clk(clk), .rst(rst), .thresh(t_thresh), .stream(x[1]));
    sng #(.SEED(10'd222)) u_in2 (.clk(clk), .rst(rst), .thresh(t_thresh), .stream(x[2]));
    sng #(.SEED(10'd333)) u_in3 (.clk(clk), .rst(rst), .thresh(t_thresh), .stream(x[3]));
   
    // Adder
    assign sel = x[0] + x[1] + x[2] + x[3];
    
    //five coefficient SNG
    sng #(.SEED(10'd400)) u_coef0 (.clk(clk), .rst(rst), .thresh(B0), .stream(z[0]));
    sng #(.SEED(10'd500)) u_coef1 (.clk(clk), .rst(rst), .thresh(B1), .stream(z[1]));
    sng #(.SEED(10'd600)) u_coef2 (.clk(clk), .rst(rst), .thresh(B2), .stream(z[2]));
    sng #(.SEED(10'd700)) u_coef3 (.clk(clk), .rst(rst), .thresh(B3), .stream(z[3]));
    sng #(.SEED(10'd800)) u_coef4 (.clk(clk), .rst(rst), .thresh(B4), .stream(z[4]));
    
    // MUX
    assign y = z[sel];


    // Cycle counter that counts clock ticks up to 1024
    always_ff @(posedge clk) begin
        if (rst)
            cycles <= 11'd0;     
        else if (!done)
            cycles <= cycles + 11'd1;
    end
    assign done = (cycles == 11'd1024); // done goes high after 1024 cycles

// output counter
    always_ff @(posedge clk) begin
        if (rst)
            count <= 11'd0;          
        else if (!done && y)
            count <= count + 11'd1;   
    end
endmodule