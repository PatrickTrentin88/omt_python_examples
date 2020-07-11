# Python Timeout Wrapper for OptiMathSAT

This is a project that implements a hard timeout and best-solution-so-far
extraction using the **Python API** interface of `OptiMathSAT` built from the
C/C++ library. It is mostly based on the
[`omt_python_examples`](https://github.com/PatrickTrentin88/omt_python_examples),
which is a collection of examples using this interface.


## Dependencies

This project requires

- Python (v3.6+)
- python3-setuptools (v47.1.1)
- gcc (v9.3.0)
- g++ (v9.3.0)
- [gmplib](https://gmplib.org/) (v6.2.0)


# Build it Yourself

Download the package of the latest version of `OptiMathSAT` (v`1.7.0` or superior)
inside the directory `optimathsat`, and unpack it. Then, run the `build.py` script
as follows:

    ~$ python3 build.py

This command builds the **Python API** of `OptiMathSAT`, and places the generated
`optimathsat.py` file in the `include` directory and the generated `_optimathsat.so`
file in the `lib` directory.

For convenience, you may want to permanently add both of these locations to your
`PYTHONPATH` environment variable:

    export PYTHONPATH=${PYTHONPATH}:.../omt_python_timeout_wrapper/include
    export PYTHONPATH=${PYTHONPATH}:.../omt_python_timeout_wrapper/lib

This step is useful to avoid import complaints with `pylint3`. The unit-test
scripts, however, are expected to work even without performing this step.


# Usage

To run `OptiMathSAT` on an example run the `benchmark_timeout.py` script. This
reads two arguments from the CLI. The first is the hard timeout as integer in
milliseconds and the problem formulation (without optimization and configuration
parts) as string. This string has to conform to the SMT-LIB v2 format:

    It can't contain commands other than functions and type declarations,
    definitions, and assertions

The script can be called from the shell using

```zsh
python3 benchmark_timeout.py [Milliseconds] [ProblemFormulation]
```

Another script `example_benchmark_timeout.py` reads files from disk and takes no
arguments. The hard timeout and filepath has to be set in the script and can
then simply be called using

```zsh
python3 example_benchmark_timeout.py
```
