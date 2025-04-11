`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/09/2025 01:18:27 PM
// Design Name: 
// Module Name: main
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

module main (
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [15:0] temperature,
    input wire [15:0] power_draw,
    input wire [15:0] vibration,
    output wire valid_out,
    output wire [9:0] risk_score,
    output wire [2:0] predicted_class
);

    // Internal wires
    wire [15:0] temp_buf, power_buf, vib_buf;
    wire [2:0] class_out;
    wire valid_mid;

    // 1. Input Buffer
    input_buffer inbuf (
        .clk(clk),
        .rst(rst),
        .valid_in(valid_in),
        .temperature(temperature),
        .power_draw(power_draw),
        .vibration(vibration),
        .valid_out(valid_mid),
        .temperature_out(temp_buf),
        .power_draw_out(power_buf),
        .vibration_out(vib_buf)
    );

    // 2. Decision Tree Logic
    decision_tree_node_logic dtree (
        .clk(clk),
        .rst(rst),
        .temperature(temp_buf),
        .power_draw(power_buf),
        .vibration(vib_buf),
        .label_class(class_out)
    );

    // 3. Risk Score Generator
    risk_score_generator scoregen (
        .clk(clk),
        .rst(rst),
        .valid_in(valid_mid),
        .predicted_label(class_out),
        .valid_out(valid_out),
        .risk_score(risk_score)
    );

    // Output predicted class
    assign predicted_class = class_out;

endmodule
