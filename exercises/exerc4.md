# Exercise 4

Putting it all togeather

1. Write a simple application that, based on a jinja template file serves a system health check REST page (json) using Flask.

2. Write a somple cli based tool to get the status of the page created in 1.
 - ping server (using ping command)
 - get health content
 - print status (green, yellow, red, gray) depending on the reply from server.

3. Optionally, store health status in alarm database (sqlite). If a status is reset, clear it.
