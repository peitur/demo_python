
init:
	virtualenv .

reset:
	virtualenv -clear .

clean:
	rm -fR bin .Python include lib pip-selfcheck.json share

activate:
	source bin/activate
