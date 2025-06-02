# Migen MAX II CPLD Breathing LED Template

This project implements a template for written in migen for Altera MAX II CPLD. The design is written in Migen (Python-based HDL) and compiled to Verilog for Quartus synthesis.

## Prerequisites

- [ ] Migen: `pip install migen`
- [ ] Quartus: [no2chem/quartuslite-docker](https://github.com/no2chem/quartuslite-docker)
- [ ] Optional: openFPGAloader for programming

## Project Structure

```
.
├── blinkpwm.py # Main PWM breathing LED module
├── build.py # Verilog generation script
├── project.qsf # Quartus settings and pin assignments
├── blink.v # Generated Verilog output
└── README.md # This file
```

## Build and Program Instructions

### 1. Generate Verilog from Migen

```bash
$ python build.py
```

Output: `blink.v` (Verilog implementation)

### 2. Compile with Quartus

```bash
$ quartus_sh --flow compile project.qsf
```

Outputs: 

- `project.pof` (Programmer Object File)

### 3 OPTIONAL Generate SVF file

```
$ quartus_cpf -c -q 12MHz -g 3.3 -n p project.pof project.svf
```

Outputs: 

- `project.svf` (Serial Vector Format)

### 4 OPTIONAL Program the CPLD (with USB Blaster)

```bash
openFPGALoader -c usb-blaster project.svf
```

### Alternative Programming Methods:

- Use Quartus Programmer GUI
- Use `quartus_pgm` command line:
  
```bash
quartus_pgm -m jtag -c USB-Blaster -o "p;project.pof" 
```

## Pin Assignments (project.qsf)

| Signal   | Pin | Description        |
| -------- | --- | ------------------ |
| sys_clk  | 12  | 50 MHz clock input |
| led_fast | 90  | "Fast" LED (green) |
| led_slow | 91  | "Slow" LED (red)   |

## Troubleshooting

- **Clock not working**: Verify 50 MHz input on PIN 12
- **LEDs not lighting**: Check polarity (code assumes active-high LEDs)
- **Programming fails**: 
  - Verify USB Blaster connection
  - Check voltage settings (3.3V LVCMOS)
  - Ensure CPLD is powered

## Dependencies

- [Migen](https://github.com/m-labs/migen) (Python hardware description library)
- [Quartus Prime Lite](https://www.intel.com/content/www/us/en/software-kit/666222.html)
- [openFPGALoader](https://github.com/trabucayre/openFPGALoader) (optional)

## License

MIT License - Free for personal and commercial use


