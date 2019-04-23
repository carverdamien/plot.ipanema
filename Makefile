PUSH?=
ALL?=
ALL_HTML?=
ALL_CSV?=
ALL_PDF?=
ALL_NPZ?=

-include cache.mk

default: push

include sysbench.mk
include batch.mk
include tracer.mk

all_npz: $(ALL_NPZ)

i80/status.html: src/plotly/status.py sysbench.csv batch.csv config.json
	./$<
ALL_HTML+=i80/status.html
ALL+=i80/status


README.md: $(ALL_HTML) $(ALL_PDF)
	./README.sh $(ALL) > $@

index.html: $(ALL_HTML) $(ALL_PDF)
	./index.sh $(ALL) > $@

PUSH+=index.html README.md $(ALL_HTML) $(ALL_CSV) $(ALL_PDF)

nopush: $(PUSH)
	@echo done

http: $(PUSH)
	python -m http.server 80

push: $(PUSH)
	git pull origin master
	git add $^
	git commit -m update
	git push origin master
