# Argo Canada Meeting

June 10, 2022
Chris Gordon

## Pre-deployment Float Testing

- DRDC Barge in Halifax is available to us for float testing. Has a moon pool,
with arms on each corner so can test 4 floats at a time.
- Tested 1 ARVOR float on the barge, setup with weighted line worked well, and
learned a lot about the deployment procedure.
- Set float to profile to 30m (Bedford Basin is 42m deep in that spot) and
drift at 30m. For our initial test, we set the profile frequency to the minimum
(1 hour), however in the future we plan to leave the floats for a few days and
so will have them profile less frequently than that (say, 2-3 times per day)
- Will also program floats to perform a certain number of profiles so it will
be waiting at surface in end of life mode for recovery when we go to retrieve
it.
- Flushed CTD with Triton X solution and then distilled water following
recovery, allowed to dry in the box and then replaced plugs days later.
- May have discovered some communication issues with ARVOR floats delivered
in 2022, as sbd messages did not arrive to Argo Canada email accounts but were
received by NKE. [note: testing tomorrow, update this bullet pt.]
- Planning to test 2 PROVOR floats later in June, Antoine Poteau at LOV sending
configuration they use for Ifremer pool testing. Plan to deploy these floats on
Fall AZMP mission, which will go in late September. 

## Real Time QC for BGC Floats

- All required python packages are already installed on MEDS server, so IT
challenges shouldn't crop up. Able to run script through BATMAN app on MEDS
server. 
- Code written for chlorophyll and backscatter tests. Working on testing.
- Backscatter code may need to be substantially updated following ADMT - saw an
update from Giorgio Dall'Olmo last month that had major changes from currently
published RTQC manual (only does range check and negative spike test).

### Outstanding items: 

- How files and WMO numbers get passed to python script.
- Where to store parameter LAST_DARK_COUNT, the CHLA dark count that may be
recalculated with each profile, and needs to be fetched from the previous
profile each time the RTQC is ran.
- Exhaustive testing.
