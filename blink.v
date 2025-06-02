/* Machine-generated using Migen */
module top(
	input sysclk,
	output led_fast,
	output led_slow
);

wire sys_clk;
wire sys_clk_1;
wire led_fast1;
wire led_slow1;
reg [7:0] bright_fast = 8'd0;
reg dir_fast = 1'd1;
reg [7:0] bright_slow = 8'd0;
reg dir_slow = 1'd1;
reg [17:0] step_ctr = 18'd0;
reg [7:0] pwm_ctr = 8'd0;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign sys_clk = sysclk;
assign sys_clk_1 = sys_clk;
assign led_fast = led_fast1;
assign led_slow = led_slow1;
assign led_fast1 = (pwm_ctr < bright_fast);
assign led_slow1 = (pwm_ctr < bright_slow);

always @(posedge sys_clk) begin
	if ((step_ctr == 1'd0)) begin
		step_ctr <= 18'd199999;
		if (dir_fast) begin
			if ((bright_fast < 7'd80)) begin
				bright_fast <= (bright_fast + 1'd1);
			end else begin
				dir_fast <= 1'd0;
			end
		end else begin
			if ((bright_fast > 1'd0)) begin
				bright_fast <= (bright_fast - 1'd1);
			end else begin
				dir_fast <= 1'd1;
			end
		end
		if (dir_slow) begin
			if ((bright_slow < 8'd255)) begin
				bright_slow <= (bright_slow + 1'd1);
			end else begin
				dir_slow <= 1'd0;
			end
		end else begin
			if ((bright_slow > 1'd0)) begin
				bright_slow <= (bright_slow - 1'd1);
			end else begin
				dir_slow <= 1'd1;
			end
		end
	end else begin
		step_ctr <= (step_ctr - 1'd1);
	end
	pwm_ctr <= (pwm_ctr + 1'd1);
end

endmodule

