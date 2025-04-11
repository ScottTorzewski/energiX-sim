### Clock Signal
#set_property PACKAGE_PIN W5 [get_ports clk]
#set_property IOSTANDARD LVCMOS33 [get_ports clk]

### Input Switches for Features
#set_property PACKAGE_PIN V17 [get_ports temp_in]       ; SW0
#set_property IOSTANDARD LVCMOS33 [get_ports temp_in]

#set_property PACKAGE_PIN V16 [get_ports power_in]      ; SW1
#set_property IOSTANDARD LVCMOS33 [get_ports power_in]

#set_property PACKAGE_PIN W16 [get_ports vib_in]        ; SW2
#set_property IOSTANDARD LVCMOS33 [get_ports vib_in]

### Button to Trigger Inference
#set_property PACKAGE_PIN U18 [get_ports start_btn]     ; BTN0
#set_property IOSTANDARD LVCMOS33 [get_ports start_btn]

### Output LEDs for Alerts (3 bits)
#set_property PACKAGE_PIN U16 [get_ports {alert_leds[0]}] ; LED0
#set_property PACKAGE_PIN E19 [get_ports {alert_leds[1]}] ; LED1
#set_property PACKAGE_PIN U19 [get_ports {alert_leds[2]}] ; LED2

#set_property IOSTANDARD LVCMOS33 [get_ports {alert_leds[*]}]

create_clock -name clk -period 10.000 [get_ports clk]

