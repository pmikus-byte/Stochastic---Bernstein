module bernstein_top_tb;
   logic clk = 0;
   logic rst;
   logic [10:0] t_thresh;
   logic [10:0] count;
   logic done;
   int fd;

    always #5 clk = ~clk;

    bernstein_top dut (.clk(clk), .rst(rst), .t_thresh(t_thresh),
    .count(count), .done(done));

    initial begin
        fd = $fopen("results/rtl_sin.csv", "w");
        $fdisplay(fd, "t_thresh,count");

        for (int j = 0; j <= 16; j++) begin
            t_thresh = j * 64;

            rst = 1;
            @(negedge clk);
            rst = 0;

            wait (done);
            @(negedge clk);

            $display("T_thresh: %0d, Count: %0d", t_thresh, count);
            $fdisplay(fd, "%0d,%0d", t_thresh, count);   //one row per t
        end

        $fclose(fd);                             
        $finish;
    end
endmodule