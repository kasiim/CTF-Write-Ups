`timescale 1ns/10ps

module tb_challenge ();
	reg clk;
	reg n_rst;
	reg en;
	reg[6:0] next_byte;
	reg[7:0] flag_byte;
	reg win;

	localparam CLK_PERIOD = 10ns;

	string flag = "pbctf{AHOY_PEKO_PEKO_shaak_nanodesu}";
	challenge CHAL (.clk(clk), .n_rst(n_rst), .en(en), .next_byte(next_byte), .win(win));

	always begin
		clk = 1'b0;
		#(CLK_PERIOD / 2.0);
		clk = 1'b1;
		#(CLK_PERIOD / 2.0);
	end

	integer i;

	initial begin
		en = 1'b0;
		next_byte = 7'b0000000;
		n_rst = 1'b0;
		@(negedge clk);
		@(posedge clk);
		n_rst = 1'b1;
		@(negedge clk);
		@(posedge clk);

		for (i = 0; i < flag.len(); i = i + 1) begin
			@(negedge clk);
			flag_byte = flag[i];
			next_byte = flag_byte[6:0];
			en = 1'b1;
		end
		@(negedge clk);
		en = 0;
		if (win == 1'b1) begin
			if (flag.len() != 49) begin
				$display("Close!!!");
			end else begin
				$display("Correct!");
			end
		end else begin
			$display("BUUBUUUUUUU DESU WA");
		end
		$finish;
	end
endmodule
