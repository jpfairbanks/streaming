# Streams Analysis
This package is for analyzing the structure of streaming algorithms.
The plan is to make a family of operators that take a stream of bytes 
and emits another stream of bytes in an common interface.
Then a cicuit can be built that uses them and the performance of the circuit can be analyzed.

# IPC
The processes will have a primary channel to read and write data.
This is where the data streams will go.
In order to have higher order streaming algoirthms, they will need to inspect 
each others internal state and modify it. This will call for running an IPC 
method to communicate this data and call state manipulating functions.
I think that having a control channel on each processing element is the way to go.
This could be performed by having a command set that comes in through the input channel.
However, this will force the PE to check whether an incoming datum is a command or data.
Each PE will publish an api for its control channel and listen on a port for commands that fit the api.

# Data formats

So far everything is built to work with UNIX pipes and ascii text. 
This is good for portability but will need to change for efficiency.
It also allows unix tools to work in the middle of a python pipe.

# Streams.py library
There is another approach that has already been built for this. 
They are concerned with adding pipes to python. 
And are heavily inspired by a book on streams written using lisp.
[[http://www.trinhhaianh.com/stream.py/#how-it-works]]

This library will be tested to see if it is fast and useful.
The only network that is there is a DAG with parralel blocks.
Perhaps by subclassing the Streams class we can make more complex networks

## Storm by twitter
Storm is a java framework for building these networks that is used by twitter.
They seem to be more advanced use a distribution system based on topologies. 
It might be better to work on that for applications but it might also have a lot of hidden logic
that muddles performance analysis. 
