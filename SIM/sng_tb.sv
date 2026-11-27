module sng_tb; 
    
    logic clk = 0;
    logic rst;
    logic [10:0] thresh;
    logic stream;
    int count;
    localparam SEED = 10'd1;

    always #5 clk = ~clk; // flips every 5 tu

    sng #(.SEED(SEED)) dut (.clk(clk), .rst(rst), .thresh(thresh), .stream(stream));
   
    initial begin  
    
        for (int j = 0; j <= 2; j++) begin
            thresh = j * 512;
            rst = 1;
            @(negedge clk);  // hold rst for 1 clk edge
            rst = 0;
            count = 0;

        for (int i = 1; i <= 1023; i++) begin
            @(negedge clk);
            if (stream == 1) count = count + 1;
        end

        $display("Threshold: %0d, Count: %0d ", thresh, count);
        end
        $finish;

  end
endmodule