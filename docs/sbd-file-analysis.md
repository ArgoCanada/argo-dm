# SBD File Analysis

The goal of this document is the summarize file sizes for SBD files from
a variety or Argo floats (core, DOXY, 6 param BGC, etc.). Relevant information
for each float will be:

- Total size of SBD files
- Number of profiles and vertical resolution (# of pts)
- Argo program (BGC, core, deep) and parameters (DOXY, full BGC)
- Platform type (will likely be all ARVOR)

## Planned floats

Core:

- 4902543 (serial:AI2600-20CA028 IMEI:300534060128640)
- 4902544 (serial:AI2600-20CA029 IMEI:300534060125640)
- 4902545 (serial:AI2600-20CA030 IMEI:300534060125620)
- 4902546 (serial:AI2600-20CA031 IMEI:300534060227580)
- 4902547 (serial:AI2600-20CA032 IMEI:300534060224310)
- 6903075 (serial:AI3500-20FR001 IMEI:300534060228320) [SBD files for profile #6 courtesy of coriolis]

BGC:

- 4902549 (serial:AI2632-20CA034 IMEI:300534060229340)
- 4902550 (serial:AI2632-20CA035 IMEI:300534060120930)
- 4902551 (serial:AI2632-20CA036 IMEI:300534060223320)
- 4902552 (serial:AI2632-20CA037 IMEI:300534060221340)
- 4902553 (serial:AI2632-20CA038 IMEI:300534060229330)

## Findings

|wmo    |serial        |imei           |nsbd|sbd_size|nprof|nfile|nc_size|npts|program|nparam|platform|
|-------|--------------|---------------|----|--------|-----|-----|-------|----|-------|------|--------|
|4902543|AI2600-20CA028|300534060128640|64  |19200   |2    |3    |65040  |258 |core   |64    |arvor   |
|4902544|AI2600-20CA029|300534060125640|126 |37800   |20   |21   |467532 |2103|core   |64    |arvor   |
|4902545|AI2600-20CA030|300534060125620|123 |36900   |20   |21   |471660 |2097|core   |64    |arvor   |
|4902546|AI2600-20CA031|300534060227580|122 |36600   |20   |21   |467952 |2114|core   |64    |arvor   |
|4902547|AI2600-20CA032|300534060224310|125 |37500   |20   |21   |467340 |2091|core   |64    |arvor   |
|6903075|AI3500-20FR001|300534060228320|36  |10800   |1    |1    |59572  |994 |core   |64    |arvor   |
