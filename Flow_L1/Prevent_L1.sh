#!/bin/sh
# Function to handle SIGINT signal
cleanup (){
    echo "Caught SIGINT, cleaning up..."
    
    # Kill all background processes
    kill 0

    make clean
    
    # Exit the script
    exit 1

    cd -
    cd 
}
cd "../Layer 1"
python3 Process_TTL_Deviation.py

cd "../Prevention/ttl"
make
make rm
make ins
cd -
cd "../Layer 1"
python3 Inject_kernel_object.py
cd -

echo "TTL Prevention Active"

cd "../tcp_timestamp"
make
make ins

cd "-"





wait