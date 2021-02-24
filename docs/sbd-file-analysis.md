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

## Workflow

For each float above, get all SBD files for it's IMEI number from the 

## Initial Data

Raw data:

|wmo    |serial        |imei           |nsbd|sbd_size|nprof|nfile|nc_size|npts|program|nparam|platform|
|-------|--------------|---------------|----|--------|-----|-----|-------|----|-------|------|--------|
|4902543|AI2600-20CA028|300534060128640|64  |19200   |2    |3    |65040  |258 |core   |64    |arvor   |
|4902544|AI2600-20CA029|300534060125640|126 |37800   |20   |21   |467532 |2103|core   |64    |arvor   |
|4902545|AI2600-20CA030|300534060125620|123 |36900   |20   |21   |471660 |2097|core   |64    |arvor   |
|4902546|AI2600-20CA031|300534060227580|122 |36600   |20   |21   |467952 |2114|core   |64    |arvor   |
|4902547|AI2600-20CA032|300534060224310|125 |37500   |20   |21   |467340 |2091|core   |64    |arvor   |
|6903075|AI3500-20FR001|300534060228320|36  |10800   |1    |1    |59572  |994 |core   |64    |arvor   |

wmo, serial, imei: float identification numbers
nsbd: number of total sbd files
sbd_size: size of all sbd files in bytes
nprof: number of profiles for those sbd files
nfile: number of Argo files (nprof does not capture downcasts)
nc_size: size of all nc files in bytes
npts: sum of all `N_LEVELS` dimensions in the nc files
program: core or bgc Argo
nparam: number of variables in the nc files
platform: float type

Processed data:

|wmo    |pts_per_profile|bytes_per_sbd|sbd_bytes_per_data_pt|nc_bytes_per_data_pt|sbd_bytes_per_profile|
|-------|---------------|-------------|---------------------|--------------------|---------------------|
|4902543|129            |300          |74.41                |252.09              |9600                 |
|4902544|105            |300          |17.97                |222.31              |1890                 |
|4902545|104            |300          |17.59                |224.92              |1845                 |
|4902546|105            |300          |17.31                |221.35              |1830                 |
|4902547|104            |300          |17.93                |223.50              |1875                 |
|6903075|994            |300          |10.86                |59.93               |10800                |

pts_per_profile = npts / nprof
bytes_per_sbd = sbd_size / nsbd
sbd_bytes_per_data_pt = sbd_size / npts
nc_bytes_per_data_pt = nc_size / npts
sbd_bytes_per_profile = sbd_size / nprof

## Comments

The data requirements do of course go up with increased vertical resolution,
but it appears that they do not go up linearly (based on only the one float
for comparison though). The amount of data transmitted in the one coriolis
profile is about 10x more than in our current configuration, but the the data
cost is between 5-6x higher.

In terms of data budgeting, if we plan for ~1000 pts from an ARVOR-RBR float,
and perhaps a slighlty larger file size, then each profile will be about 12kB.
This would put us in plan GT. It is *pretty* right on the cusp. Early profiles
appear to need more bandwidth (see high usage per data in 4902543), so plan
GT would certainly be necessary for the first month say, but we may get away
with plan G for the remainder of the deployment.

In terms of rapid profiles, I would estimate plan GT would allow for up to
24 1000pt profiles per month, perhaps slightly fewer in the first month.
