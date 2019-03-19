# blockchain-simulator
A blockchain simulator based on SimPy in python 3. 

## Steps to Install:

1. Clone this project or download

2. Create a new virtualenv for this project

3. Install all the python package requirements:

        pip install -r requirements.txt

## Files:

1. transactions.py : A class for Transactions representation

2. blocks.py : A class for Block representation

3. network_state_graph.py: A class for creating network topology with latency

4. blockchain_simulation.py: Main script for running the simulator

## How to run:

Open Terminal(Linux) or Command(Windows) and type:
    
        python blockchain_simulation.py

## Parameters
Currently, for changing the parameters of the simulation, we need to change the value of parameters in the blockchain_simulation.py
   
## Format of Log:

        Time |  nodeID  |  Event   | Data Type  | Data ID  
        
## Contribution
If you would like to contribute on the BlockSIM project,
1. Fork this repository
2. Clone the repository
3. Make the changes and commit those changes
4. Push the committed work and
5. Send the pull request.

Our core developer team will review and merge the committed work into the main code base. Please make sure your contribution is useful and relevant before submitting.

## License
The BlockSIM project is licensed under [MIT License](https://opensource.org/licenses/MIT) and also included in our repository in the [LICENSE.md](https://github.com/RoseBay-Consulting/BlockSim/blob/master/LICENSE.md)
