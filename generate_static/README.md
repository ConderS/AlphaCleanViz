# Static Viz Generator 
Generates pre-customized, static Vega visualizations from a given .csv dataset 
## Parameters
### Location of data file (.csv):
    --data <data_file_location_with_respect_to_main.py>
__Ex__:
`--data examples/generic.csv`
    
### Chart Type:
__Available Types__:
- `bar`
- `scatter`
- `line`


    `--chart_type <chart_type>`

### Columns to be plotted (Optional):
User has the option to specify which columns to plot. Otherwise, the program will assume the following schema from the sequential order of the data file's columns. In the latter case, the program will assume that the data file *only* contains the relevant columns.

__Bar__:
- Column 1: X Axis
- Column 2: Y Axis

__Scatter__:
- Column 1: X Axis
- Column 2: Y Axis
- Column 3 (Optional): Size of Data Points

   `--columns <column1> <column2> <etc...>`

## Example Usage:
    python main.py --data examples/generic.csv --columns category amount --chart_type bar
