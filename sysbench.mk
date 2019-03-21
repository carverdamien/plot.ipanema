SYSBENCH_STORAGE=sysbench.csv
PUSH+=$(SYSBENCH_STORAGE)

$(SYSBENCH_STORAGE): $(FILES_IN_STORAGE)
	./src/storage.py -t sysbench -o $@ $(DIR_IN_STORAGE)

# MACHINE ENGINE ENGINE_VERSION METRIC
define sysbench
$1/$2/$3/sysbench.csv: $$(SYSBENCH_STORAGE)
	@mkdir -p $$(dir $$@)
	./src/select.py -i $$< -o $$@ 'machine==$1' 'engine==$2 $3'
$1/$2/$3/$4.html: $1/$2/$3/sysbench.csv
	./src/plotly/$4.py -o $$@ $$<
$1/$2/$3/$4.pdf: $1/$2/$3/sysbench.csv
	./src/seaborn/$4.py -o $$@ $$<
ALL+=$1/$2/$3/$4
ALL_HTML+=$1/$2/$3/$4.html
ALL_PDF+=$1/$2/$3/$4.pdf
ALL_CSV+=$1/$2/$3/sysbench.csv
endef

$(eval $(call sysbench,i44,mongo,v4.1.8,throughput))
$(eval $(call sysbench,i44,mongo,v4.1.8,95th_latency))
$(eval $(call sysbench,i44,mongo,v4.1.8,avg_latency))
$(eval $(call sysbench,i44,mysql,8.0.15,throughput))
$(eval $(call sysbench,i44,mysql,8.0.15,95th_latency))
$(eval $(call sysbench,i44,mysql,8.0.15,avg_latency))
$(eval $(call sysbench,i44,mysql,5.7.25,throughput))
$(eval $(call sysbench,i44,mysql,5.7.25,95th_latency))
$(eval $(call sysbench,i44,mysql,5.7.25,avg_latency))

$(eval $(call sysbench,i80,mongo,v4.1.8,throughput))
$(eval $(call sysbench,i80,mongo,v4.1.8,95th_latency))
$(eval $(call sysbench,i80,mongo,v4.1.8,avg_latency))
$(eval $(call sysbench,i80,mysql,8.0.15,throughput))
$(eval $(call sysbench,i80,mysql,8.0.15,95th_latency))
$(eval $(call sysbench,i80,mysql,8.0.15,avg_latency))
$(eval $(call sysbench,i80,mysql,5.7.25,throughput))
$(eval $(call sysbench,i80,mysql,5.7.25,95th_latency))
$(eval $(call sysbench,i80,mysql,5.7.25,avg_latency))
