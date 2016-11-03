MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:
.SUFFIXES:

################
# Utilities

# Used for backups
date := $(shell date +%Y%m%d%H%M%S)

# Used for debugging
.PHONY: echo.%
echo.%:
	@echo $*=$($*)

# Used to make specific .env files
make-env = ./scripts/env.bash subst < $< > $@

# Used to load specific .env files
load-env = set -o allexport && unset $$(./scripts/env.bash variables) && source $< && set +o allexport

# Used to filter based on specific substrings. e.g.
#   $(call containing foo,bing bingfoobaz dingfoo foobang)
#     == bingfoobaz dingfoo foobang
containing = $(filter %,$(foreach v,$2,$(if $(findstring $1,$v),$v)))
not-containing = $(filter %,$(foreach v,$2,$(if $(findstring $1,$v),,$v)))

################
# Environment variables

################
# Sanity checks and local variables

################
# Exported variables

export DATE := $(date)

################
# Includes

################
# Standard targets

.PHONY: all
all: run

.PHONY: run
run: .depend.secondary
	./analyze.py raw/shuo_test335.py

.PHONY: depend
depend: .depend.secondary

.PHONY: check
check:

.PHONY: help
help:

.PHONY: clean
clean:

################
# Application specific targets

################
# Source transformations

.SECONDARY: .depend.secondary
.depend.secondary: requirements.txt | venv
	python -m pip install -r $<
	touch $@
