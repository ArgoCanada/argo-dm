# ARVOR Parameter Values for RBR Pilot Project

## Action Items

### Summary

All changes applied with the following commands:

```text
!MC 1 5
!MC 2 24
!MC 3 48
!MC 17 400
!MC 18 1400
!MC 19 1
!MC 20 2
!MC 21 5
!MC 28 0
```

### Vertical Sampling Scheme

Use the same vertical sampling scheme as floats 6903075 and 6903076. These
belong to the coriolis DAC and collect approximately 1000pts per profile
(usually a little less, as the 1dbar bins tend to be more like 1.1-1.2).
The sampling intervals are:

|Depth Range     |Bin Size|Number of pts|
|----------------|--------|-------------|
|Surface-400 dbar|1 dbar  |400          |
|400-1400 dbar   |2 dbar  |500          |
|1400-2000 dbar  |5 dbar  |120          |
|Total           |        |1020         |

The parameters to set this up are:

|Mission Parameter|Description                            |Value|
|-----------------|---------------------------------------|-----|
|MC17             |Threshold surface/Intermediate Pressure|400  |
|MC18             |Threshold Intermediate/Bottom Pressure |1400 |
|MC19             |Thickness of the surface slices        |1    |
|MC20             |Thickness of the intermediate slices   |2    |
|MC21             |Thickness of the bottom slices         |5    |

Commandline:

```text
!MC 17 400
!MC 18 1400
!MC 20 2
!MC 21 5
```

MC19 is 1 by default but you can check this with `?MC 19`, and if it responds
as not 1, change it to 1 with `!MC 19 1`.

### Profile Frequency

Take 5 daily profiles upon deployment, then profile every second day. The
parameter values will be:

|Mission Parameter|Description                         |Value|
|-----------------|------------------------------------|-----|
|MC1              |Number of cycles with cycle period 1|5    |
|MC2              |Cycle period 1                      |24   |
|MC3              |Cycle period 2                      |48   |

Commandline:

```text
!MC 1 5
!MC 2 24
!MC 3 48
```

### Change Pump Turnoff Depth

Change MC28, CTD sensor Cut-Off pressure (Pump stop), to 0. I think the float
continues to collect despite the pump turning off so this might basically do
nothing since there is no pump to turn off.

Comandline:

```text
!MC 28 0
```

## Planning

### Initial Rapid Sampling

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

### Alternate Binning Schemes

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

### Keep CTD on all the way to Surface

Relevant parameters:

- MC28: CTD sensor Cut-Off pressure (Pump stop) (default 5)

Suggested example: RBR CTD is unpumped, so no need to turn it off near-surface.

Pseudocode: Set MC28 = 0

Commandline:

```text
!MC 28 0
>>> <MC28 0>
```
