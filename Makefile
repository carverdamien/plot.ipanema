DIR_IN_STORAGE=$(wildcard ~/storage/*/*/*/*)
FILES_IN_STORAGE=$(shell find $(DIR_IN_STORAGE))
STORAGE=storage.csv

default: push

$(STORAGE): $(FILES_IN_STORAGE)
	./src/storage.py -t sysbench -o $@ $(DIR_IN_STORAGE)

include functions.mk

$(eval $(call func,i44,mongo,v4.1.8,throughput))
$(eval $(call func,i44,mongo,v4.1.8,95th_latency))
$(eval $(call func,i44,mongo,v4.1.8,avg_latency))
$(eval $(call func,i44,mysql,8.0.15,throughput))
$(eval $(call func,i44,mysql,8.0.15,95th_latency))
$(eval $(call func,i44,mysql,8.0.15,avg_latency))
$(eval $(call func,i44,mysql,5.7.25,throughput))
$(eval $(call func,i44,mysql,5.7.25,95th_latency))
$(eval $(call func,i44,mysql,5.7.25,avg_latency))

$(eval $(call func,i80,mongo,v4.1.8,throughput))
$(eval $(call func,i80,mongo,v4.1.8,95th_latency))
$(eval $(call func,i80,mongo,v4.1.8,avg_latency))
$(eval $(call func,i80,mysql,8.0.15,throughput))
$(eval $(call func,i80,mysql,8.0.15,95th_latency))
$(eval $(call func,i80,mysql,8.0.15,avg_latency))
$(eval $(call func,i80,mysql,5.7.25,throughput))
$(eval $(call func,i80,mysql,5.7.25,95th_latency))
$(eval $(call func,i80,mysql,5.7.25,avg_latency))

README.md: $(ALL_HTML) $(ALL_PDF)
	./README.sh $(ALL) > $@

index.html: $(ALL_HTML) $(ALL_PDF)
	./index.sh $(ALL) > $@

PUSH=index.html README.md $(ALL_HTML) $(ALL_CSV) $(ALL_PDF) $(STORAGE)

nopush: $(PUSH)
	@echo done

push: $(PUSH)
	git pull origin master
	git add $^
	git commit -m update
	git push origin master
