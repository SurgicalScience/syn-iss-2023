Do not make any changes to the scripts.

The following variables are to be pointed to using arguments via the command line:
* `test_csv_path = sys.argv[1] # READ IN`
* `predicted_masks_path = sys.argv[2] # READ IN`
* `groundtruth_masks_path = sys.argv[3] # READ IN` 
* `metrics_csv_path = sys.argv[4] # OUTPUT`

Example command line code for the binary task 1 script:
* `python evaluate-task1-binary.py .\binary\test.csv  .\binary\team-xyz\predictions .\binary\groundtruth .\binary\team-xyz\metrics`

Example command line code for the parts task 2 script:
* `evaluate-task2-parts.py .\parts\test.csv  .\parts\team-medhacker\predictions .\parts\groundtruth .\parts\team-medhacker\metrics`

Example of folders structure used by the organizers for challenge submissions:

```|__ binary/
    |
    |__ test.csv
    |
    |__ groundtruth/
    |   |__ b-qwrnkladsfsa.png
    |   |__ b-qwrnkladsfsa.png
    |   |__ ...
    |
    |__ inputs/
    |   |__ s-asdasdsadasd.png
    |   |__ s-qwrnkladsfsa.png
    |   |__ ...
    |
    |__ team-xyz/
    |   |__ metrics/
    |   |   
    |   |__ predictions/
    |       |__ pred-asdasdsadasd.png
    |       |__ pred-qwrnkladsfsa.png
    |       |__ ...
    |
    |__ team-medhacker/
        |__ ...
