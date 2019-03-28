DIR_IN_SYSBENCH_STORAGE=$(foreach m,i44 i80,$(foreach b,mongo mysql,$(wildcard ~/storage/$m/$b/*/*)))
SYSBENCH_STORAGE=sysbench.csv
PUSH+=$(SYSBENCH_STORAGE)

METRICS=min_latency max_latency avg_latency p95th_latency throughput duration nr_migrations nr_sleep nr_switches nr_wakeup
include metric.mk
$(foreach m,$(METRICS),$(eval $(call metric,$(m))))

$(SYSBENCH_STORAGE):
	./src/storage.py -t sysbench -o $@.tmp.csv $(DIR_IN_SYSBENCH_STORAGE)
	if ! diff -q $@.tmp.csv $@; then mv $@.tmp.csv $@; fi
	rm -f $@.tmp.csv

# MACHINE ENGINE ENGINE_VERSION
define sysbench
$1/$2/$3/sysbench.csv: $$(SYSBENCH_STORAGE)
	@mkdir -p $$(dir $$@)
	./src/select.py -i $$< -o $$@ 'machine==$1' 'engine==$2 $3' 'st_mtime>=1553698800'
$(foreach metric,$(METRICS),
$1/$2/$3/$(metric).html: $1/$2/$3/sysbench.csv sysbench.json ./src/plotly/$(metric).py
	./src/plotly/$(metric).py -c sysbench.json -o $$@ $$<
$1/$2/$3/$(metric).pdf: $1/$2/$3/sysbench.csv sysbench.json ./src/seaborn/$(metric).py
	./src/seaborn/$(metric).py -c sysbench.json -o $$@ $$<
ALL+=$1/$2/$3/$(metric)
ALL_HTML+=$1/$2/$3/$(metric).html
ALL_PDF+=$1/$2/$3/$(metric).pdf
ALL_CSV+=$1/$2/$3/sysbench.csv
)
endef

$(eval $(call sysbench,i44,mongo,v4.1.8))
$(eval $(call sysbench,i44,mysql,8.0.15))
$(eval $(call sysbench,i44,mysql,5.7.25))

$(eval $(call sysbench,i80,mongo,v4.1.8))
$(eval $(call sysbench,i80,mysql,8.0.15))
$(eval $(call sysbench,i80,mysql,5.7.25))
