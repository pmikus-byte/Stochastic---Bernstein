module smoke_tb ;

int count = 0;
int b[5] ;
int t_thresh;

initial begin

    t_thresh = 500;

    b[0] = 0;
    b[1] = 707;
    b[2] = 1000;
    b[3] = 707;
    b[4] = 0;

    for (int i = 0; i < 1000; i++) begin
         int sel;
         sel = 0;

        for (int k = 0; k < 4; k++) begin
            if (($urandom % 1000) < t_thresh) 
                sel = sel + 1;  
      end

      if (($urandom % 1000) < b[sel]) 
        count = count + 1;

      if (i < 10) $display("cycle %0d: sel = %0d", i, sel);  // peek at the first 10 cycles

    end
    $display("Output count: %0d / 1000", count);


$finish;
end
endmodule