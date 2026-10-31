module smoke_tb ;

int count = 0;
int b[5] ;
int t_thresh;

initial begin

int fd;
fd = $fopen("results.csv", "w");

$fdisplay(fd, "t_thresh,count");


    b[0] = 0;
    b[1] = 707;
    b[2] = 1000;
    b[3] = 707;
    b[4] = 0;

for ( t_thresh = 0; t_thresh <= 1000; t_thresh += 100) begin
        count = 0;
           
    for (int i = 0; i < 1000; i++) begin
        int sel;
        sel = 0;

        for (int k = 0; k < 4; k++) begin
            if (($urandom % 1000) < t_thresh) 
                sel = sel + 1;   
        end

        if (($urandom % 1000) < b[sel]) 
            count = count + 1;
    end
    
$fdisplay(fd, "%0d, %0d", t_thresh, count);
$display("T Threshold = %0d, Count =  %0d", t_thresh, count);

end
$fclose(fd);
$finish;
end
endmodule