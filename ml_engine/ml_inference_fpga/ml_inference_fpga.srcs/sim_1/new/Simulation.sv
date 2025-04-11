`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/09/2025 10:18:53 AM
// Design Name: 
// Module Name: Simulation
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////




module Simulation;

  // Inputs
  reg clk = 0;
  reg rst = 0;
  reg [15:0] temp_in = 0;
  reg [15:0] power_in = 0;
  reg [15:0] vib_in = 0;

  // Output
  wire [2:0] predicted_label;

  // Instantiate the Unit Under Test (UUT)
  decision_tree_node_logic uut (
    .clk(clk),
    .rst(rst),
    .temperature(temp_in),
    .power_draw(power_in),
    .vibration(vib_in),
    .label_class(predicted_label)
  );

  // Clock generation (10ns period = 100MHz)
  always #5 clk = ~clk;

  initial begin
    $display("⏳ Starting Testbench...");

    // Apply reset
    rst = 1;
    #20;
    rst = 0;

    // Test 1: Normal values - expect unknown
    temp_in = 16'd15360;   // 60°C
    power_in = 16'd12800;  // 50W
    vib_in  = 16'd5120;    // 20
    #50;
    $display("Test 1 - Label Class: %b", predicted_label);

    // Test 2: High temperature only
    temp_in = 16'd21760;   // 85°C
    power_in = 16'd12800;
    vib_in  = 16'd5120;
    #50;
    $display("Test 2 - Label Class: %b", predicted_label);

    // Test 3: High power and vibration
    temp_in = 16'd15360;
    power_in = 16'd25600;
    vib_in  = 16'd4096;
    #50;
    $display("Test 3 - Label Class: %b", predicted_label);

    // Test 4: All features high
    temp_in = 16'd23040;
    power_in = 16'd28160;
    vib_in  = 16'd4608;
    #50;
    $display("Test 4 - Label Class: %b", predicted_label);

    $display("✅ Testbench complete.");
    $stop;
  end
endmodule


