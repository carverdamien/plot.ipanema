DIR_IN_STORAGE=$(wildcard ~/storage/*/*/*/*)
STORAGE=storage.csv
FILES=$(shell find $(STORAGE))

push: README.md
	git commit -am update
	git push origin master

README.md: $(ALL_HTML)
	./README.sh $^ > $@

$(STORAGE): $(FILES)
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

clean:
	rm -f *.csv

.PHONY: clean all_html
