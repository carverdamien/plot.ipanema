DIR_IN_STORAGE=$(wildcard ~/storage/*/*/*/*)
FILES_IN_STORAGE=$(shell find $(DIR_IN_STORAGE))
PUSH?=
ALL?=
ALL_HTML?=
ALL_CSV?=
ALL_PDF?=

default: push

include sysbench.mk
include batch.mk

README.md: $(ALL_HTML) $(ALL_PDF)
	./README.sh $(ALL) > $@

index.html: $(ALL_HTML) $(ALL_PDF)
	./index.sh $(ALL) > $@

PUSH+=index.html README.md $(ALL_HTML) $(ALL_CSV) $(ALL_PDF)

nopush: $(PUSH)
	@echo done

push: $(PUSH)
	git pull origin master
	git add $^
	git commit -m update
	git push origin master
