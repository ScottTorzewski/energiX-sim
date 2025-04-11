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


module risk_score_generator (
    input wire clk,
    input wire rst,
    input wire valid_in,
    input wire [2:0] predicted_label,         // 3-bit input supports up to 8 labels
    output reg valid_out,
    output reg [9:0] risk_score               // 10-bit output, range 0-1000
);

always @(posedge clk or posedge rst) begin
    if (rst) begin
        risk_score <= 0;
        valid_out <= 0;
    end else if (valid_in) begin
        valid_out <= 1;
        case (predicted_label)
            3'd0: risk_score <= 800;  // motor_overheat
            3'd1: risk_score <= 750;  // overload
            3'd2: risk_score <= 600;  // bearing_wear
            3'd3: risk_score <= 850;  // critical_overload
            3'd4: risk_score <= 700;  // bearing_wear_with_power_issue
            3'd5: risk_score <= 900;  // thermal_mechanical_failure
            3'd6: risk_score <= 950;  // impending_failure
            3'd7: risk_score <= 620;  // vibration_failure
            default: risk_score <= 500;
        endcase
    end else begin
        valid_out <= 0;
    end
end

endmodule



