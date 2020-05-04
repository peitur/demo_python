
# Exercises, set 2

 1. Create a cli application that counts each word and prints them sorted (separate on whitespaces for simplicity).
 For simplicity, assume all input files are text files.
 Bonus: print the 10 most common words only.

```
./exercise2.1.py somefile.txt
a : 131
something : 123
...
```

 2. Create a flask based status reporter. Create something that checks the system load, free memory and disk usage.
 Output the content as a json status message with Flask.

TIP: In this environment (demo project root), set virtualenv, install Flask.
```bash
make init
source bin/activate
pip3 install Flask
```

Output example:
```json
{
  "hostname":"host.name.se",
  "status":"green",
  "message":"ok"
}
```

```json
{
  "hostname":"host.name.se",
  "status":"red",
  "message":"memory full"
}
```

```json
{
  "hostname":"host.name.se",
  "status":"yellow",
  "message":"cpu load high"
}
```
