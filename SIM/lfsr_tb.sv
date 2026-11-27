module lfsr_tb; 
    
    logic clk = 0;
    logic rst;
    logic [9:0] q;

    localparam SEED = 10'd1;

    always #5 clk = ~clk; // flips every 5 tu

lfsr #(.SEED(SEED)) dut (.clk(clk), .rst(rst), .q(q));

    initial begin  
        rst = 1;
        @(negedge clk);  // hold rst for 1 clk edge
        rst = 0;

        for (int i = 1; i <= 1023; i++) begin
            @(negedge clk);
            if (i <= 10) $display("Cycle %0d: q = %0d", i, q);

            if (q == 0) $display("ERROR");
            if ((q == SEED) && (i != 1023)) $display("Repeated early at cycle %0d", i);

        end

        
    $display("q after 1023 cycles = %0d (should be the seed, 1)", q);
    $finish;
  end

endmodule