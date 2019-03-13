# MACHINE ENGINE ENGINE_VERSION METRIC
define func
$1/$2/$3/storage.csv: $$(STORAGE)
	@mkdir -p $$(dir $$@)
	./src/select.py -i $$< -o $$@ 'machine==$1' 'engine==$2 $3'
$1/$2/$3/$4.html: $1/$2/$3/storage.csv
	./src/plotly/$4.py -o $$@ $$<
ALL_HTML+=$1/$2/$3/$4.html
ALL_CSV+=$1/$2/$3/storage.csv
endef
