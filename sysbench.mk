SYSBENCH_STORAGE=sysbench.csv
PUSH+=$(SYSBENCH_STORAGE)

$(SYSBENCH_STORAGE): $(FILES_IN_STORAGE)
	./src/storage.py -t sysbench -o $@ $(DIR_IN_STORAGE)

# MACHINE ENGINE ENGINE_VERSION
define sysbench
$1/$2/$3/sysbench.csv: $$(SYSBENCH_STORAGE)
	@mkdir -p $$(dir $$@)
	./src/select.py -i $$< -o $$@ 'machine==$1' 'engine==$2 $3'
$(foreach metric,throughput 95th_latency avg_latency,
$1/$2/$3/$(metric).html: $1/$2/$3/sysbench.csv
	./src/plotly/$(metric).py -o $$@ $$<
$1/$2/$3/$(metric).pdf: $1/$2/$3/sysbench.csv
	./src/seaborn/$(metric).py -o $$@ $$<
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
