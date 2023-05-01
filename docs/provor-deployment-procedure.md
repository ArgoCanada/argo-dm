# PROVOR Deployment Procedure
Chris Gordon

Bedford Institute of Oceanography

## Required Equipment

- PROVOR float
- Squirt bottle w/ milli-q water
- Release hook

## Setup

Deployment is best done off the aft of the ship, with current running away from
the vessel so that the float. Remove the float from the box and stand it
upright. 

If usuing one, attach the release hook to the crane. The crew of the ship may
have other suggestions for deployment method which is fine. Suggest the float
not be deployed by hand however. 

## Float launch sequence

This section is effectively a reproduction of the manufacturer-provided launch
checklist, with some added comments. It is important that the launch sequence
is done outside and away from the superstructure of the ship if possible, as
the float will need to connect to the satellite before it will be ready to 
deploy. 

- Visually inspect the float to verify that is in good condition, remove
plugs/caps from all sensors (CTD caps, black cap on blue oxygen optode, white
plastic cap on bio-optical sensor), and introduce milli-q water into the CTD
cell.
- Record metadata of the float, IMEI and Serial Number being the most 
important.
- Remove the magnet from the on/off position (turning the float on).
- You should immediately hear 5 eV actions (clicks), followed by activation of
the hydraulic pump. The hydraulic pump may be active for as little as a few
seconds to as much as several minutes. If the float has been tested in water
already for example, it may take several minutes, as the float deploys at max
buoyancy and therefore may need time to refill the bladder.
- The float will then perform a full auto-test. During this time you should see
the water level in the CTD change, as well as the lights on the optical sensor
activate. The float will also acquire a GPS fix and RUDICS connection during 
this time. 
- The timing of the auto test can vary, as it will depend on satellite
visibility. 
- You should then hear 5 quick eV activations (same as when magnet was removed)
but faster. 
- If the previous step is reached, the float is ready to deploy.
- If the previous step is not reached within ~15 minutes, put the magnet back
on the on/off position and start again from the beginning.
- The 5 quick eV actions will be followed by a quick activation of the CTD pump
and the hydraulic pump. If the delay before mission parameter (PM1) is non-zero
(it is 0 by default), the float will wait PM1 minutes before the CTD pump or
hydraulic pump activate. It is still ok to deploy during this wait period.
- The NKE checklist states that you should not deploy the float before you can
confirm that it has sent a technical message via the RUDICS server. In my
experience, this can take a long time, and also is not practical at sea to be
checking an FTP server. So we forego this step. The 5 quick eV activations
serve as the threshold to deploy.

## Deployment with release hook

Put the release hook *up* through the black plastic collar of the float.
Close the hook and replace the safety pin. Slowly lift the float off the deck
with the crane. The collar should be located at the float's centre of gravity. 
Once the float is outboard, remove the safety pin. Ensure the rope attached to
the release hook is on board, but not taught so that the hook will not release
before intended. Lower the float to near sea-level, but do not put it in the
water. Pull the line on the release hook, and allow the float to fall into the
water, and float away to complete its mission.