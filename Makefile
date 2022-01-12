##
# gradeTracker
#
# @file
# @version 0.1

XDG_CONFIG_HOME ?= /home/${USER}/.config
XDG_DATA_HOME ?= /home/${USER}/.local/share
INSTALL_FOLDER ?= /home/${USER}/.local/bin

setup: requirements.txt
	pip install -r requirements.txt

install:
	cp gradeTracker ${INSTALL_FOLDER}/gradeTracker
	mkdir -p ${XDG_CONFIG_HOME}/gradeTracker
	mkdir -p ${XDG_DATA_HOME}/gradeTracker
	cp config.yml ${XDG_CONFIG_HOME}/gradeTracker/config.yml
	cp data.yml ${XDG_DATA_HOME}/gradeTracker/data.yml

uninstall:
	rm ${INSTALL_FOLDER}/gradeTracker
	rm -rf ${XDG_CONFIG_HOME}/gradeTracker
	rm -rf ${XDG_DATA_HOME}/gradeTracker

# end
