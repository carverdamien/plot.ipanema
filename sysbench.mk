DIR_IN_SYSBENCH_STORAGE=$(filter-out %.csv,$(foreach m,i80,$(foreach b,mongo mysql,$(wildcard ~/storage/$m/$b/*/*))))
SYSBENCH_STORAGE=sysbench.csv
PUSH+=$(SYSBENCH_STORAGE)

include metric.mk
METRICS=min_latency max_latency avg_latency p95th_latency throughput duration $(COMMON_METRICS)
$(foreach m,$(METRICS),$(eval $(call metric,$(m))))

define sysbench_csv
$1.csv:
	./src/storage.py -t sysbench -o $1.csv $1
endef

$(foreach d,$(DIR_IN_SYSBENCH_STORAGE),$(eval $(call sysbench_csv,$d)))

$(SYSBENCH_STORAGE): $(DIR_IN_SYSBENCH_STORAGE:%=%.csv)
	./src/concatenate.py $@ $^

# MACHINE ENGINE ENGINE_VERSION
define sysbench
$1/$2/$3/sysbench.csv: $$(SYSBENCH_STORAGE)
	@mkdir -p $$(dir $$@)
	./src/select_row.py -i $$< -o $$@ 'machine==$1' 'engine==$2 $3' 'st_mtime>=1553709600' 'duration<=400'
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

#$(eval $(call sysbench,i44,mongo,v4.1.8))
#$(eval $(call sysbench,i44,mysql,8.0.15))
#$(eval $(call sysbench,i44,mysql,5.7.25))

$(eval $(call sysbench,i80,mongo,v4.1.8))
$(eval $(call sysbench,i80,mysql,8.0.15))
$(eval $(call sysbench,i80,mysql,5.7.25))
