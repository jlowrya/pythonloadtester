# Load Tester

## Project requirements

Your tool should offer the following features:
- Run for a specified duration
- Generate a report at the end containing
    - total requests made
    - counts by status code
    - median, 95th, and 99th percentile latency
    - overall throughput (QPS)


## How to run the application
To run this program, you will need to have [Docker](https://www.docker.com/) installed on your machine. Additionally, make sure the `QPSCounter` flask application provided via Google Drive is running on your local machine by following the instructions in that `README.md`. Once that is running on your machine, `cd` into the `loadtester` directory and run `sh run.sh` in the terminal, similar to how the flask app is run. This is the command for mac, but it may be different on Windows. This will build the required Docker image and run the program.

## Interacting with the program

The program runs a basic loop that asks the user how many threads they would like to use for the program, as well as how long they would like to run the load test for. These inputs can be provided via the terminal.

Once the test is complete, the required statistics will be output to the screen. The user will then be asked if they wish to run another test, accepting either `y` or `n` as a response. The program will run in this loop until it receives an `n` to that response, at which point it will terminate.

Basic input validation is performed when inputting the number of threads, seconds, and whether or not to continue the program.

## Considerations

When developing this program, I took the requirement of "control the number of concurrent requests" to mean control the number of threads used. This seemed to make the most sense when coupled with the requirement to run in a specific duration.

As well, I am manually printing out the various statistics required, although that could probably be consolidated into methods of their own.