# DESCRIPTION

This is a collection of **Optimization Modulo Theories** examples
using the **Python API** interface of `OptiMathSAT`.

# REQUIREMENTS

This project requires **Python 3.X** and [**gmplib**](https://gmplib.org/).

# BUILDING

Download the package of the latest version of `OptiMathSAT` (v. `1.6.2` or superior)
inside the directory `optimathsat`, and unpack it. Then, run the `build.py` script
as follows:

    ~$ python3 build.py

This command builds the **Python API** of `OptiMathSAT`, and places the generated
`mathsat.py` file in the `include` directory and the generated `_mathsat.so` file
in the `lib` directory.

For convenience, you may want to permanently add both of these locations to your
`PYTHONPATH` environment variable:

    export PYTHONPATH=${PYTHONPATH}:.../omt_python_examples/include
    export PYTHONPATH=${PYTHONPATH}:.../omt_python_examples/lib

This step is useful to avoid import complaints with `pylint3`. The unit-test
scripts, however, are expected to work even without performing this step.

# USAGE

Run all unit-test examples with

    ~$ python3 run.py

or some unit-test example of interest with

    ~$ ./unit-tests/simple_omt.py
    
# NOTES

Please contact the author of this repository, or the current maintainer
of the [`OptiMathSAT`](http://optimathsat.disi.unitn.it/), in the case
that there is still any persisting issue with these unit-tests.


# Contributors

This project is authored by [Patrick Trentin](http://www.patricktrentin.com) (<patrick.trentin.88@gmail.com>).


