: 
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

3. Create a string parser that creates dicts from slash sepparated strings. Keywords sepparated by slashes represent a new level in a dict. 
Note that with this tool, / should be changeable with , or .

```
./solution1.3 /test1/key1/word abcd
{
   test1 : {
      key1 :{
         work : abcd
      }
   } 
}
```

4. Given a dict,  print each element with separators used in 3.

```
cat sample.json
-----------------------
{
   test1: {
      key1 :{
         work: 1,
         sleep 2,
         idle 3
      }
   }
}
-----------------------
./solution1.4 sample.json
/test1/key1/work 1
/test1/key1/sleep 2
/test1/key1/idle 3

```
