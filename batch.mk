BATCH_STORAGE=batch.csv
PUSH+=$(BATCH_STORAGE)

METRICS=time
include metric.mk
$(eval $(foreach m,$(METRICS),$(call metric,$(m))))

$(BATCH_STORAGE): $(FILES_IN_STORAGE)
	./src/storage.py -t batch -o $@ $(DIR_IN_STORAGE)

# MACHINE ENGINE ENGINE_VERSION
define batch
$1/$2/$3/batch.csv: $$(BATCH_STORAGE)
	@mkdir -p $$(dir $$@)
	./src/select.py -i $$< -o $$@ 'machine==$1' 'batch==$2 $3'
$(foreach metric,$(METRICS),
$1/$2/$3/$(metric).html: $1/$2/$3/batch.csv batch.json ./src/plotly/$(metric).py
	./src/plotly/$(metric).py -c batch.json -o $$@ $$<
$1/$2/$3/$(metric).pdf: $1/$2/$3/batch.csv batch.json ./src/seaborn/$(metric).py
	./src/seaborn/$(metric).py -c batch.json -o $$@ $$<
ALL+=$1/$2/$3/$(metric)
ALL_HTML+=$1/$2/$3/$(metric).html
ALL_PDF+=$1/$2/$3/$(metric).pdf
ALL_CSV+=$1/$2/$3/batch.csv
)
endef

$(eval $(call batch,i44,hackbench,1.0-3))
$(eval $(call batch,i44,kbuild,4.19))

$(eval $(call batch,i80,hackbench,1.0-3))
$(eval $(call batch,i80,kbuild,4.19))

