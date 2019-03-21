DIR_IN_STORAGE=$(wildcard ~/storage/*/*/*/*)
FILES_IN_STORAGE=
PUSH?=
ALL?=
ALL_HTML?=
ALL_CSV?=
ALL_PDF?=

default: push

files_in_storage.mk:
	@echo Building $@
	@echo FILES_IN_STORAGE=$$(find $(DIR_IN_STORAGE)) > $@
.PHONY: files_in_storage.mk

include files_in_storage.mk
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
