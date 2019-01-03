About the data: 

The 'Data' folder contains four datasets to test on my algorithms. 



Running the Algorithms:


-----------------------------------------------------------------------------
RUNNING MST:

Open terminal and cd into the project directory. Run the following command:

python3 MST.py (filename)

e.g

python3 MST.py att48.tsp


considerations:
Please make sure you have the networkx python package.
----------------------------------------------------------------------------



---------------------------------------------------------------------------
RUNNING SIMULATED ANNEALING ALGORITHM

Open terminal and cd into the project directory. Run the following command:

python3 simulated_annealing.py (filename) cooling_method alpha iterations epsilon k

e.g (recommended parameters)

python3 simulated_annealing.py a280.tsp linear 1 100000 0.0001 1


considerations:
the algorithm prints the decreasing temperature every 100 iterations.
use the recommended parameters first ^
might take a while
----------------------------------------------------------------------------



----------------------------------------------------------------------------
RUNNING GENETIC ALGORITHM

Open terminal and cd into the project directory. Run the following command:

python3 GA.py (filename) population_size num_generations crossover_rate mutation_rate tournament_size

e.g

python3 GA.py att48.tsp 500 200 0.95 0.05 250


considerations:
use the recommended parameters first ^
might take a while to run using certain parameters
