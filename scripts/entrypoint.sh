#!/bin/sh

echo "Starting Failover script ..."

while true;
do
    python /tmp/scripts/ipfailover.py
done