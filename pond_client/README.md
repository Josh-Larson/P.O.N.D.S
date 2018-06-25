# Pond Clients

The two pond Pis have the ideal requirements:

1. Clients (Pond Pis) connect to the central controller to serve status information
    * Sends LED status, and pond status to the controller
    * Sends other status information?
2. Ideally, both of the pond Pis will share the exact same codebase.
3. Configure Pi's to start their python programs as daemons, so they *must* start their programs on boot. This will prevent users from having to manually restart the script on each boot. 

