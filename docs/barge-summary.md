# Pre-Deployment Testing at DRDC Barge

Chris Gordon

## Scheduling

Logistics steps required to schedule time at DRDC barge:

1. Find a time that works for both parties, our contact is Mark Fotheringham
([Mark.Fotheringham@forces.gc.ca](mailto:Mark.Fotheringham@forces.gc.ca)).
2. The scheduled time will need to work for the Sigma-T to take you over to
the barge as well. Scheduling can be done by contacting
[SigmaT.CCGS@dfo-mpo.gc.ca](mailto:SigmaT.CCGS@dfo-mpo.gc.ca). A Google
calendar for the Sigma-T is also available to help select available times.
For any parties new to the vessel, a general statement of risk provided by the
ship must be signed and sent to the coxwain.
3. Ensure all COVID procedures are followed. From the DRDC side, a COVID
attestation for each party attending should be sent to Richard Pederson
([Richard.Pederson@ecn.forces.gc.ca](mailto:Richard.Pederson@ecn.forces.gc.ca))
a few days ahead of attending the barge. For joining a Canadian Coast Guard
vessel like the Sigma-T, a rapid test must be taken the day of.
4. Once scheduled times are settled circulate a detailed itinerary to all
parties involved. At this time, ensure all parties have proper PPE (life vest,
steel toed shoes, hard hat).

## Setup, Programming, and Deployment

The DRDC barge has 4 davits, one on each corner of the moon pool. which are 
about 3m above the surface of the water. The Bedford Basin in this area is 
42m deep. From each davit, a weighted line measuring 38m is hung, making the 
maximum profiling depth for the float 35m. For the ARVOR floats, they can be 
programmed to profile and drift at this depth, however for the PROVOR floats,
the minimum profile and drift depth is 100m. This means that for these floats,
you must attached them securely enough to the line that they cannot escape the
line at the bottom. We did this by putting the line through a small loop (I 
used a 
[butterfly loop](https://www.animatedknots.com/alpine-butterfly-loop-knot)) of 
nylon rope before securing the weight, and then tying the nylon rope securely 
around the plastic piece of the float used for deployment. A large shackle was 
used for the weight at the bottom of the line.

<p align="middle">
    <img src="../figures/loop.jpg" alt="Alpine Butterfly Loop" style="width:400px;"/>
    <img src="../figures/shackle.jpg" alt="Shackle weight" style="width:400px;"/>
</p>

For the programming of ARVOR floats, a shallow drift and profile depth is used.
The parameters for setting the time for initial surfacing should be set to a
sufficient time to allow the float to make its initial dive, which can take up
to 3 hours. The user may select a cycle time that allows for 2-4 profiles per
day. A file with the parameters used in our testing can be found [here]().

For the PROVOR floats, there are a great many more parameters to be changed. 
The file we used was based off pool tests performed at Ifremer in France, the
file containing all those parameters can be found [here]().

Communication can be a challenge on the barge (as will be discussed in further 
detail later), so it is recommended that the launch sequence is started
outside. Additionally, the file sent during the launch sequence may not be seen
on the RUDICS server immediately, so we used the "5 fast eV actions" as our
threshold on the NKE checklist as our "OK to deploy" step. At this point, the
full self check will have already been completed which includes getting a GPS
fix and connecting to Iridium.

For the PROVORS, we used the overhead hoist for deployment as they are quite
heavy. We lifted the floats using a 5ft strap, which we left on the float
during the test so it could easily be reused for recovery. The float was
lowered to water level on the lift, tied the nylon line looped onto the hanging
weigthed line to the plastic hook on the float, and then lowered the float into
the water.

## Data

## Recovery

## Conclusion and Lessons Learned
