#!/bin/sh


# Function to handle SIGINT signal
cleanup() {
    echo "Caught SIGINT, cleaning up..."
    
    # Kill all background processes
    kill 0
    
    # Exit the script
    exit 1
}

# Trap SIGINT and call the cleanup function
trap cleanup SIGINT
cd "../Layer2/version2"
./packet_capture > "../Flow_L1/op.txt" 
cd -

wait

