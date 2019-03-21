# MACHINE ENGINE ENGINE_VERSION METRIC
define func
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
