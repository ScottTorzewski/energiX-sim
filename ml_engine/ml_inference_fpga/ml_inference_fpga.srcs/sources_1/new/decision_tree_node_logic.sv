`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/09/2025 10:12:08 AM
// Design Name: 
// Module Name: decision_tree_node_logic
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

module decision_tree_node_logic (
    input wire clk,
    input wire rst,
    input wire [15:0] temperature,     
    input wire [15:0] power_draw,      
    input wire [15:0] vibration,       
    output reg [2:0] label_class       
);

    // Label Encoding:
    // 000 -> motor_overheat
    // 001 -> overload
    // 010 -> bearing_wear
    // 011 -> critical_overload
    // 100 -> bearing_wear_with_power_issue
    // 101 -> thermal_mechanical_failure
    // 110 -> impending_failure
    // 111 -> unknown / default

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            label_class <= 3'b111; // unknown
        end else begin
            // Updated decision tree logic for realistic sensor values
            if (temperature > 16'd7500 && power_draw > 16'd8000 && vibration > 16'd900) begin
                label_class <= 3'b110; // impending_failure
            end else if (temperature > 16'd7500 && power_draw > 16'd8000) begin
                label_class <= 3'b011; // critical_overload
            end else if (temperature > 16'd7500 && vibration > 16'd900) begin
                label_class <= 3'b101; // thermal_mechanical_failure
            end else if (power_draw > 16'd8000 && vibration > 16'd900) begin
                label_class <= 3'b100; // bearing_wear_with_power_issue
            end else if (temperature > 16'd7500) begin
                label_class <= 3'b000; // motor_overheat
            end else if (power_draw > 16'd8000) begin
                label_class <= 3'b001; // overload
            end else if (vibration > 16'd900) begin
                label_class <= 3'b010; // bearing_wear
            end else begin
                label_class <= 3'b111; // unknown
            end
        end
    end

endmodule
