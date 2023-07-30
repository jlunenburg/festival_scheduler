# Installation
* Clone the repo (if desired, in a [virtual environment](https://docs.python.org/3/library/venv.html))
* Install requirements:
```commandline
python3 -m pip install requirements.txt
```

# Running the application
* Go to the `src` folder
```commandline
cd src
```
* Run the application and pass the input file as an argument
```commandline
python3 -m festival_scheduler <input_file_name>
```
* E.g.,
```commandline
python3 -m festival_scheduler ../test/data/shows_example.txt
```
* N.B., input files are assumed to be formatted as in the example, e.g.,
```commandline
show_1 29 33
show_2 2 9
show_3 44 47
...
```