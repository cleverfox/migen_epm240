# build.py

from migen import *
from migen.fhdl import verilog
from blink import Blink
from blinkpwm import BlinkPWM

class TopWrapper(Module):
    def __init__(self, green_max=128, red_max=255):
        # Create a clock domain without reset
        self.clock_domains.cd_sys_norst = ClockDomain("sys", reset_less=True)
        #cd = ClockDomain("sys")
        #dut.clock_domains.append(cd)

        # Top-level ports
        self.sysclk = Signal()   # Input clock (PIN_12)
        self.led_fast = Signal()  # Output LED (PIN_90)
        self.led_slow = Signal()  # Output LED (PIN_91)

        # Instantiate BlinkPWM
        self.submodules.blink = BlinkPWM(green_max=green_max, red_max=red_max)

        # Connect clock domain
        self.comb += [
            self.cd_sys_norst.clk.eq(self.sysclk),     # Drive clock
            self.blink.sys_clk.eq(self.cd_sys_norst.clk)  # Connect to BlinkPWM
        ]

        # Connect LEDs
        self.comb += [
            self.led_fast.eq(self.blink.led_fast),
            self.led_slow.eq(self.blink.led_slow)
        ]

if __name__ == "__main__":
    # 1) Instantiate the DUT
#    dut = Blink()
#    dut = BlinkPWM()
    dut = TopWrapper(green_max=80, red_max=255)

    # 2) Tell the converter which signals are I/Os
    ios = {dut.led_fast, dut.led_slow, dut.sysclk}

    # 3) Convert to Verilog

    v = verilog.convert(dut, ios=ios, create_clock_domains=False)

    # 4) Write the Verilog text to blink.v
    with open("blink.v", "w") as f:
        f.write(str(v))

    print("Generated blink.v")

