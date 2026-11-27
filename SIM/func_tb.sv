// Sweeps t from 0 to 1 for one function.
// The coefficients B0..B4 are parameters set from the command line with iverilog -P.
module func_tb;
    parameter B0 = 0, B1 = 0, B2 = 0, B3 = 0, B4 = 0;

    logic        clk = 0, rst;
    logic [10:0] t_thresh;
    logic [10:0] count;
    logic        done;
    integer      fd, j;

    bernstein_top #(.B0(B0), .B1(B1), .B2(B2), .B3(B3), .B4(B4)) dut (
        .clk(clk), .rst(rst), .t_thresh(t_thresh), .count(count), .done(done));

    always #5 clk = ~clk;

    initial begin
        fd = $fopen("hw_func.csv", "w");
        $fdisplay(fd, "t_thresh,count");
        for (j = 0; j <= 16; j = j + 1) begin
            @(negedge clk); t_thresh = j * 64; rst = 1;
            @(negedge clk); rst = 0;
            wait(done); @(negedge clk);
            $fdisplay(fd, "%0d,%0d", t_thresh, count);
        end
        $fclose(fd);
        $finish;
    end
endmodule