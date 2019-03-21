BATCH_STORAGE=batch.csv
PUSH+=$(BATCH_STORAGE)

$(BATCH_STORAGE): $(FILES_IN_STORAGE)
	./src/storage.py -t batch -o $@ $(DIR_IN_STORAGE)

# MACHINE ENGINE ENGINE_VERSION METRIC
define batch
$1/$2/$3/batch.csv: $$(BATCH_STORAGE)
	@mkdir -p $$(dir $$@)
	./src/select.py -i $$< -o $$@ 'machine==$1' 'engine==$2 $3'
$1/$2/$3/$4.html: $1/$2/$3/batch.csv
	./src/plotly/$4.py -o $$@ $$<
$1/$2/$3/$4.pdf: $1/$2/$3/batch.csv
	./src/seaborn/$4.py -o $$@ $$<
ALL+=$1/$2/$3/$4
ALL_HTML+=$1/$2/$3/$4.html
ALL_PDF+=$1/$2/$3/$4.pdf
ALL_CSV+=$1/$2/$3/batch.csv
endef
