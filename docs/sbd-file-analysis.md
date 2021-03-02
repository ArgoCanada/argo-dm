# SBD File Analysis

The goal of this document is the summarize file sizes for SBD files from
a variety or Argo floats (core, DOXY, 6 param BGC, etc.). Relevant information
for each float will be:

- Total size of SBD files
- Number of profiles and vertical resolution (# of pts)
- Argo program (BGC, core, deep) and parameters (DOXY, full BGC)
- Platform type (will likely be all ARVOR)

## Data Transmission Plan

### Shared Services Data Plans

- Plan B: 12kB/mo., $20.85/mo., all core floats
- Plan F: 17kB/mo., $25.26/mo., BGC (DOXY) floats
- Plan G: 30kB/mo., $38.59/mo.
- Plan GT: 300kB/mo. $170.89/mo., RBR floats (freq. profiling & high res.)

### Approximating Max Usage

Using the data in the table in the subsequent section, the following plot was
generated to approximate the size of SBD files transmitted via Iridium:

![data plan plot](https://github.com/ArgoCanada/argo-dm/blob/master/figures/approximate_data_usage.png)

The max data points based on a linear regression for each plan are:

- Plan B: 461 (core), 190 (bgc)
- Plan F: 710 (core), 307 (bgc)
- Plan G: 1357 (core), 611 (bgc)

## Background / Data Analysis

### NKE Data Estimates

The following data was generated using an NKE spreadsheet:

|npts|npacket|nsbd|data size (kB)|npacket_bgc|nsbd_bgc|bgc data size (kB)|
|----|-------|----|--------------|-----------|--------|------------------|
|0   |7      |3   |0.9           |11         |4       |1.2               |
|18  |9      |3   |0.9           |14         |5       |1.5               |
|22  |10     |4   |1.2           |15         |5       |1.5               |
|38  |11     |4   |1.2           |17         |6       |1.8               |
|98  |15     |5   |1.5           |26         |9       |2.7               |
|109 |16     |6   |1.8           |27         |9       |2.7               |
|152 |18     |6   |1.8           |34         |12      |3.6               |
|185 |21     |7   |2.1           |38         |13      |3.9               |
|218 |23     |8   |2.4           |43         |15      |4.5               |
|268 |26     |9   |2.7           |50         |17      |5.1               |
|352 |32     |11  |3.3           |62         |21      |6.3               |
|418 |36     |12  |3.6           |72         |24      |7.2               |
|518 |43     |15  |4.5           |86         |29      |8.7               |
|685 |54     |18  |5.4           |110        |37      |11.1              |
|1018|76     |26  |7.8           |157        |53      |15.9              |
|2018|143    |48  |14.4          |300        |100     |30.0              |

### Planned floats

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

### Workflow

For each float above, get all SBD files for it's IMEI number from the Argo
Canada email address. Look at the size of those files relative to the amount
of data transmitted by looking at the netCDF files.

### Initial Data

Raw data:

|wmo    |serial        |imei           |nsbd|sbd_size|nprof|nfile|nc_size|npts|program|nparam|platform|
|-------|--------------|---------------|----|--------|-----|-----|-------|----|-------|------|--------|
|4902543|AI2600-20CA028|300534060128640|64  |19200   |2    |3    |65040  |258 |core   |64    |arvor   |
|4902544|AI2600-20CA029|300534060125640|126 |37800   |20   |21   |467532 |2103|core   |64    |arvor   |
|4902545|AI2600-20CA030|300534060125620|123 |36900   |20   |21   |471660 |2097|core   |64    |arvor   |
|4902546|AI2600-20CA031|300534060227580|122 |36600   |20   |21   |467952 |2114|core   |64    |arvor   |
|4902547|AI2600-20CA032|300534060224310|125 |37500   |20   |21   |467340 |2091|core   |64    |arvor   |
|6903075|AI3500-20FR001|300534060228320|36  |10800   |1    |1    |59572  |994 |core   |64    |arvor   |
|4902549|AI2632-20CA034|300534060229340|206 |61800   |19   |20   |579772 |1999|bgc    |72    |arvor   |
|4902550|AI2632-20CA035|300534060120930|52  |15600   |2    |3    |84356  |256 |bgc    |72    |arvor   |
|4902551|AI2632-20CA036|300534060223320|204 |61200   |18   |19   |518872 |1800|bgc    |72    |arvor   |
|4902552|AI2632-20CA037|300534060221340|51  |14900   |3    |2    |84408  |257 |bgc    |72    |arvor   |
|4902553|AI2632-20CA038|300534060229330|53  |15500   |3    |2    |82292  |102 |bgc    |72    |arvor   |

- wmo, serial, imei: float identification numbers
- nsbd: number of total sbd files
- sbd_size: size of all sbd files in bytes
- nprof: number of profiles for those sbd files
- nfile: number of Argo files (nprof does not capture downcasts)
- nc_size: size of all nc files in bytes
- npts: sum of all `N_LEVELS` dimensions in the nc files
- program: core or bgc Argo
- nparam: number of variables in the nc files
- platform: float type

Processed data:

|wmo    |pts_per_profile|bytes_per_sbd|sbd_bytes_per_data_pt|nc_bytes_per_data_pt|sbd_bytes_per_profile|
|-------|---------------|-------------|---------------------|--------------------|---------------------|
|4902543|129            |300          |74.41                |252.09              |6400                 |
|4902544|105            |300          |17.97                |222.31              |1800                 |
|4902545|104            |300          |17.59                |224.92              |1757                 |
|4902546|105            |300          |17.31                |221.35              |1743                 |
|4902547|104            |300          |17.93                |223.50              |1785                 |
|6903075|994            |300          |10.86                |59.93               |10800                |
|4902549|105            |300          |30.92                |290.03              |3090                 |
|4902550|128            |300          |60.94                |329.51              |5200                 |
|4902551|100            |300          |34.00                |288.26              |3221                 |
|4902552|85             |300          |57.97                |328.46              |4967                 |
|4902553|34             |300          |151.96               |806.78              |5167                 |

- pts_per_profile = npts / nprof
- bytes_per_sbd = sbd_size / nsbd
- sbd_bytes_per_data_pt = sbd_size / npts
- nc_bytes_per_data_pt = nc_size / npts
- sbd_bytes_per_profile = sbd_size / nfile (to account for downcasts as a profile)

### Comments

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
