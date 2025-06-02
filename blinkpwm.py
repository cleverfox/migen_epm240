# blink.py

from migen import *
from migen.fhdl.structure import Signal

class BlinkPWM(Module):
    def __init__(self, green_max=128, red_max=255):
        """
        Fade/PWM “breathing” for two LEDs at 50 MHz.
        
        green_max, red_max: 8-bit integers (0..255)
            - green_max  = maximum brightness (duty) for the “fast” LED (PIN 90)
            - red_max    = maximum brightness (duty) for the “slow” LED (PIN 91)
        
        Ports (to map in your .qsf):
          - sys_clk       (input, 50 MHz on PIN 12)
          - led_fast    (output, green LED on PIN 90)
          - led_slow    (output, red LED on PIN 91)
        
        Internally:
          • A single 18-bit “step counter” runs at 50 MHz / 200 000 ≈ 250 Hz → 
            one brightness step every 0.004 s. With 255 steps up + 255 steps down,
            each full breathe cycle takes ~2 s.
          • An 8-bit PWM counter runs at 50 MHz / 256 ≈ 195 kHz, giving ~8-bit
            resolution for duty control.
        """

        # -------------- I/O ports --------------
        self.sys_clk    = Signal()  # 50 MHz input  (map to PIN 12)
        self.led_fast = Signal()  # PWM output    (map to PIN 90, “green”)
        self.led_slow = Signal()  # PWM output    (map to PIN 91, “red”)

        # -------------- Parameters --------------
        max_fast = green_max    # 0..255
        max_slow = red_max      # 0..255

        # -------------- Internal signals --------------
        # Current brightness (0..255) and direction bit (1=up, 0=down)
        bright_fast = Signal(8, reset=0)
        dir_fast    = Signal(reset=1)
        bright_slow = Signal(8, reset=0)
        dir_slow    = Signal(reset=1)

        # “Step” counter for fade speed (counts 200 000 clocks → ~0.004 s)
        # Needs 18 bits since 2^18=262 144 > 200 000
        step_ctr    = Signal(18, reset=0)
        step_period = 200_000   # ≈ 0.004 s at 50 MHz

        # 8-bit PWM counter for 0..255 duty cycles (≈195 kHz PWM)
        pwm_ctr     = Signal(8, reset=0)

        # -------------- Sync logic --------------
        # All in the “sys” clock domain (50 MHz)
        self.sync += [
            # Fade “step” logic: every time step_ctr hits 0, we update brightness
            If(step_ctr == 0,
                # Reload
                step_ctr.eq(step_period - 1),

                # Update “fast” (green) brightness up/down, clamped at max_fast
                If(dir_fast,
                    If(bright_fast < max_fast,
                        bright_fast.eq(bright_fast + 1)
                    ).Else(
                        dir_fast.eq(0)
                    )
                ).Else(
                    If(bright_fast > 0,
                        bright_fast.eq(bright_fast - 1)
                    ).Else(
                        dir_fast.eq(1)
                    )
                ),

                # Update “slow” (red) brightness up/down, clamped at max_slow
                If(dir_slow,
                    If(bright_slow < max_slow,
                        bright_slow.eq(bright_slow + 1)
                    ).Else(
                        dir_slow.eq(0)
                    )
                ).Else(
                    If(bright_slow > 0,
                        bright_slow.eq(bright_slow - 1)
                    ).Else(
                        dir_slow.eq(1)
                    )
                )

            ).Else(
                # Normal countdown
                step_ctr.eq(step_ctr - 1)
            ),

            # PWM counter always free-running 0..255
            pwm_ctr.eq(pwm_ctr + 1)
        ]

        # -------------- Combinatorial PWM output --------------
        # The LED is “1” whenever pwm_ctr < current brightness, else “0”
        self.comb += [
            self.led_fast.eq(pwm_ctr < bright_fast),
            self.led_slow.eq(pwm_ctr < bright_slow)
        ]

