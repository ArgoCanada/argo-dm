# Argo Canada Sampling Strategy

This document summarizes the sampling strategy for Canadian Argo floats, both
core and DO. These floats operate on SBD transmission. Full BGC floats will
have a separate plan as they will transmit data via RUDICS. The document will
include the parameter settings required to achieve the described sampling for
NKE ARVOR floats.

## Core Program

### Spatial Resolution

The core floats have a capacity of  700pts on SSC data plan 3. To stay
safely within this plan without overages, they are set to collect 650-700
points. The vertical resolution with depth is as follows:

OPTION A

- 1 dbar bins from 0 to 250 dbar (250 points)
- 2 dbar bins from 250 to 500 dbar (125 points)
- 5 dbar bins below 500 dbar (300 pts)

Total points: 675

OPTION B

- 1 dbar bins from 0 to 500 dbar (500 pts)
- 5 dbar bins from 500 to 1000 dbar (100 pts)
- 10 dbar bins from below 1000 dbar (100 pts)

Total points: 700

OPTION C

- 1 dbar bins form 0 to 400 dbar (400 pts)
- 2 dbar bins from 500 to 1000 dbar (250 pts)
- 25 dbar bins below 1000 dbar (40 pts)

Total points: 690

### Temporal Resolution

Following the recommendation of *Johnson et al. (in prep.)* and the AST meeting
held March 2021, floats will profile every 10 days plus 5 hours in order to
collect profiles at various times of day. This allows the Argo fleet to resolve
diel cycles in temperature and oxygen, allowing for calculation of primary
production.

The relevant parameters for ARVOR floats are MC2 and MC3. MC3 will only matter
if there is a shift in float cycle timing after a certian number of profiles,
but for simplicity we will change both to 245 (hours). 

```text
!MC 2 245
!MC 3 245
```
