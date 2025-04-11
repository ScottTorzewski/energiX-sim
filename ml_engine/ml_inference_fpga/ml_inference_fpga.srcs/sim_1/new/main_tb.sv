`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/09/2025
// Design Name: EnergiX Simulation
// Module Name: main_tb
// Project Name: EnergiX Sim Suite
// Target Devices: 
// Tool Versions: 
// Description: Hardware simulation with external CSV-driven input for testing.
//////////////////////////////////////////////////////////////////////////////////

module main_tb;

  // Inputs
  reg clk = 0;
  reg rst = 0;
  reg valid_in = 0;
  reg [15:0] temperature = 0;
  reg [15:0] power_draw = 0;
  reg [15:0] vibration = 0;

  // Outputs
  wire valid_out;
  wire [9:0] risk_score;
  wire [2:0] predicted_class;

  // File handlers
  integer results_file;
  integer input_file;
  integer scan_status;
  integer i;
  integer dynamic_risk = 0;

  // File data holders
  reg [15:0] temp_val, power_val, vib_val;

  // Instantiate the DUT (Device Under Test)
  main uut (
    .clk(clk),
    .rst(rst),
    .valid_in(valid_in),
    .temperature(temperature),
    .power_draw(power_draw),
    .vibration(vibration),
    .valid_out(valid_out),
    .risk_score(risk_score),
    .predicted_class(predicted_class)
  );

  // Clock generation (100MHz)
  always #5 clk = ~clk;

  // Task to apply one test vector
  task apply_inputs(input [15:0] t, input [15:0] p, input [15:0] v);
    begin
      @(negedge clk);
      valid_in = 1;
      temperature = t;
      power_draw = p;
      vibration = v;
      @(negedge clk);
      valid_in = 0;
    end
  endtask

  initial begin
    $display("🔧 Starting CSV-Driven Hardware Simulation...");

    input_file = $fopen("python_inputs.csv", "r");
    if (input_file == 0) begin
      $display("❌ ERROR: Could not open python_inputs.csv for reading.");
      $stop;
    end

    results_file = $fopen("C:/Users/torze/energiX-sim/results.txt", "w");
    if (results_file == 0) begin
      $display("❌ ERROR: Could not open results.txt for writing.");
      $stop;
    end
    $fwrite(results_file, "Test,Temp,Power,Vib,Class,Risk\n");

    // Reset
    rst = 1;
    repeat (2) @(negedge clk);
    rst = 0;


    i = 1;
    while (!$feof(input_file)) begin
        scan_status = $fscanf(input_file, "%d,%d,%d\n", temp_val, power_val, vib_val);

  if (scan_status == 3) begin
    apply_inputs(temp_val, power_val, vib_val);
    wait (valid_out);

    // Simulate dynamic FPGA risk score based on thresholds
    dynamic_risk = ((temp_val > 7500 ? (temp_val - 7500) / 2 : 0) +
                    (power_val > 8000 ? (power_val - 8000) / 2 : 0) +
                    (vib_val > 900 ? (vib_val - 900) * 2 : 0));
    if (dynamic_risk > 1000) dynamic_risk = 1000;

    $display("Test %0d -> Predicted Class: %0d, Risk Score: %0d (Dynamic: %0d)", i, predicted_class, risk_score, dynamic_risk);
    $fwrite(results_file, "%0d,%0d,%0d,%0d,%0d,%0d\n", i, temp_val, power_val, vib_val, predicted_class, dynamic_risk);
    i = i + 1;

  end else if (scan_status != -1) begin
    $display("⚠️  Skipped malformed line in input CSV. Status = %0d", scan_status);
  end
end


    $fclose(input_file);
    $fclose(results_file);
    $display("✅ Simulation Complete. File written.");
    $stop;
  end

endmodule
