# Google Hashcode

## Car rides scheduling problem

See the <online_qualification_round_2018.pdf> for the full description of the challenge.

## Current scores

| Input                     |  Standard        | Specific tuning  |
|---------------------------|------------------|------------------|
| a_example.in              | 10               | 10               |
| b_should_be_easy.in       | 176 877          | 176 877          |
| c_no_hurry.in             | 13 156 456       | 15 818 350       |
| d_metropolis.in           | 8 427 162        | 12 139 521       |
| e_high_bonus.in           | 21 335 222       | 21 465 945       |
| Total                     | 43 095 727       | 49 600 703       | 


## Requirements
You will need Docker to run the script, or Python3/Pypy3 if you want to exec it directly.

## How to use it

You can use Docker to start the code.
```bash
docker-compose up
```

It will provide you the following output:

```bash
kevin@MBP-de-Kevin ~/P/hashcode> docker-compose up
Starting hashcode_code_1 ... done
Attaching to hashcode_code_1
code_1  | ###  a_example  ###
code_1  | Row: 3 Col: 4 Car nb: 2 Ride nb: 3 Bonus price: 2 Time: 10
code_1  |
code_1  | Done: 3 Early: 1 Dropped: 0 Early possible: 1 Not possible: 0
code_1  | Score: 10
code_1  |
code_1  | ###  b_should_be_easy  ###
code_1  | Row: 800 Col: 1000 Car nb: 100 Ride nb: 300 Bonus price: 25 Time: 25000
code_1  |
code_1  | Done: 294 Early: 288 Dropped: 6 Early possible: 288 Not possible: 6
code_1  | Score: 176877
code_1  |
code_1  | ###  c_no_hurry  ###
code_1  | Row: 3000 Col: 2000 Car nb: 81 Ride nb: 10000 Bonus price: 1 Time: 200000
code_1  |
code_1  | Done: 8113 Early: 0 Dropped: 1887 Early possible: 0 Not possible: 0
code_1  | Score: 13156456
code_1  |
code_1  | ###  d_metropolis  ###
code_1  | Row: 10000 Col: 10000 Car nb: 400 Ride nb: 10000 Bonus price: 2 Time: 50000
code_1  |
code_1  | Done: 7513 Early: 5791 Dropped: 2487 Early possible: 9827 Not possible: 12
code_1  | Score: 8427162
code_1  |
code_1  | ###  e_high_bonus  ###
code_1  | Row: 1500 Col: 2000 Car nb: 350 Ride nb: 10000 Bonus price: 1000 Time: 150000
code_1  |
code_1  | Done: 9877 Early: 9874 Dropped: 123 Early possible: 9877 Not possible: 16
code_1  | Score: 21335222
code_1  |
code_1  | Total score: 43095727
code_1  | Total time: 0:02:46.760090
hashcode_code_1 exited with code 0
```