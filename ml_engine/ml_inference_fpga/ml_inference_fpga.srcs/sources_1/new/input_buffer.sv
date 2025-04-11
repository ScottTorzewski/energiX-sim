`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/09/2025 10:12:38 AM
// Design Name: 
// Module Name: risk_score_generator
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


module input_buffer (
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [15:0] temperature,
    input wire [15:0] power_draw,
    input wire [15:0] vibration,
    output reg valid_out,
    output reg [15:0] temperature_out,
    output reg [15:0] power_draw_out,
    output reg [15:0] vibration_out
);

always @(posedge clk or posedge rst) begin
    if (rst) begin
        temperature_out <= 0;
        power_draw_out <= 0;
        vibration_out <= 0;
        valid_out <= 0;
    end else if (valid_in) begin
        temperature_out <= temperature;
        power_draw_out <= power_draw;
        vibration_out <= vibration;
        valid_out <= 1;
    end else begin
        valid_out <= 0;
    end
end

endmodule

