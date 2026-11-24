module bernstein_top_tb;
   logic clk = 0;
   logic rst;
   logic [10:0] t_thresh;
   logic [10:0] count;
   logic done;

    always #5 clk = ~clk;

    bernstein_top dut (.clk(clk), .rst(rst), .t_thresh(t_thresh),
    .count(count), .done(done));

    initial begin
        for (int j = 0; j <= 2; j++) begin
            t_thresh = j * 512;

            rst = 1;
            @(negedge clk);
            rst = 0;

            wait (done);
            @(negedge clk);

            $display("T_thresh: %0d, Count: %0d", t_thresh, count);
        end
        $finish;    
    end
endmodule