##
#
# @file
# @version 0.1



# end
.DEFAULT_GOAL := help

.PHONY: build help workflow

OS=$(shell uname -s)

# OPEN launches the system command adapted to its parameter
ifeq ($(OS),Linux)
INTERACTIVE=
OPEN=xdg-open
ifndef DOCKER_COMPOSE_UID
export DOCKER_COMPOSE_UID=$(shell id -u)
export DOCKER_COMPOSE_GID=$(shell id -g)
endif
else ifeq ($(OS),Darwin)
INTERACTIVE=
OPEN=open
else ifeq ($(OS),CYGWIN_NT-10.0)
INTERACTIVE=winpty
OPEN=cmd /c start
else
INTERACTIVE=
OPEN=echo
endif

help: ## Display available commands in Makefile
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build dinstance
	@bash bin/build.sh

demo: ##  start a demo pymdext container to run it
	@bash bin/runInteractive.sh

# annote: ##  run annotation with main_regex
# 	@bash bin/annoteText.sh

# omop: ##  transform annotation to omop data
# 	@bash bin/annoteToOmop.sh

# omopdb: ## WARNING load data to omopdb. Need to be in the docker ( make demo)
# 	@bash bin/annoteToOmopDB.sh
