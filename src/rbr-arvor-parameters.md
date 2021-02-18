# ARVOR Parameter Values for RBR Pilot Project

## Initial Rapid Sampling

Relevant parameters:

- MC1: Number of cycles with cycle period 1 (default 300)
- MC2: Cycle period 1 (default 240)
- MC3: Cycle period 2 (default 240)

Suggested example: for the first 10 cycles, sample once a day, then transition
to typical Argo 10-day sampling period.

Pseudocode: Set MC1 = 10 and MC2 = 24

Commandline - the float should respond with the new parameter value. The float
will respond even if the change is unsuccessful, showing the currently set value:

```text
!MC 1 10
>>> <MC1 10>
!MC 2 24
>>> <MC2 24>
```

## Alternate Binning Schemes

Relevant parameters:

- MC17: Threshold surface/Intermediate Pressure (default 1)
- MC18: Threshold Intermediate/Bottom Pressure (default 200)
- MC19: Thickness of the surface slices (default 1)
- MC20: Thickness of the intermediate slices (default 10)
- MC21: Thickness of the bottom slices (default 25)

Suggested example: Sample an area of interest between 100-250dbar with 1dbar
bins. Note that this (I believe) will be the lower limit as all parameter
values must be integers. From surface to 100dbar use sample bins of 5dbar,
and below 250dbar use bins of 25dbar.

Pseudocode: Change MC17 to 100, and MC18 to 250. Change MC19 to 5, MC20 to 1.
MC21 can stay at its default value.

Commandline:

```text
!MC 17 100
>>> <MC17 100>
!MC 18 250
>>> <MC18 250>
!MC 19 5
>>> <MC19 5>
!MC 20 1
>>> <MC20 1>
```
