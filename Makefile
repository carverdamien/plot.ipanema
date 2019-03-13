DIR_IN_STORAGE=$(wildcard ~/storage/*/*/*/*)
FILES_IN_STORAGE=$(shell find $(DIR_IN_STORAGE))
STORAGE=storage.csv

default: push

$(STORAGE): $(FILES_IN_STORAGE)
	./src/storage.py -o $@ $(DIR_IN_STORAGE)

include functions.mk

$(eval $(call func,i44,mongo,v4.1.8,throughput))
#$(eval $(call func,i44,mongo,v3.6.3,throughput))
$(eval $(call func,i44,mysql,8.0.15,throughput))
$(eval $(call func,i44,mysql,5.7.25,throughput))

$(eval $(call func,i80,mongo,v4.1.8,throughput))
#$(eval $(call func,i80,mongo,v3.6.3,throughput))
$(eval $(call func,i80,mysql,8.0.15,throughput))
$(eval $(call func,i80,mysql,5.7.25,throughput))

README.md: $(ALL_HTML)
	./README.sh $^ > $@

index.html: $(ALL_HTML)
	./index.sh $^ > $@

push: index.html README.md $(ALL_HTML) $(ALL_CSV)
	git add $^
	git commit -m update
	git push origin master
