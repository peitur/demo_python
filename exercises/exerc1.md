
# Exercises, set 1

 1. Create a cli application that prints a random string, a random password generator. Generate N blocks with L length per block.
Each blocks must contain at least one uppercase, lowercase, number and one special character (of your choice).

```
./solution1.1.py 3 5
# Blocks: 4
# Block length: 8
# Total length: 32
EbqC9lpxP7H7ahuxblmCpnC80ekvReC9
```

2. Create a Flask service that gives the caller a random string of certain length.

```
GET http://192.168.0,87/random/4/8

{
   "timestamp":"2019-09-12 12:02:11",
   "message": "EbqC9lpxP7H7ahuxblmCpnC80ekvReC9"
}

```
