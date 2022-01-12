##
# gradeTracker
#
# @file
# @version 0.1

setup: requirements.txt
	pip install -r requirements.txt

install:
	cp gradeTracker /usr/local/bin/gradeTracker

uninstall:
	rm /usr/local/bin/gradeTracker

# end
