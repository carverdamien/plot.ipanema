DIR_IN_BATCH_STORAGE=$(foreach m,i44 i80,$(foreach b,kbuild hackbench,$(wildcard ~/storage/$m/$b/*/*)))
BATCH_STORAGE=batch.csv
PUSH+=$(BATCH_STORAGE)

METRICS=time nr_migrations nr_sleep nr_switches nr_wakeup
include metric.mk
$(foreach m,$(METRICS),$(eval $(call metric,$(m))))

$(BATCH_STORAGE):
	./src/storage.py -t batch -o $@.tmp.csv $(DIR_IN_BATCH_STORAGE)
	if ! diff -q $@.tmp.csv $@; then mv $@.tmp.csv $@; fi
	rm -f $@.tmp.csv

# MACHINE ENGINE ENGINE_VERSION
define batch
$1/$2/$3/batch.csv: $$(BATCH_STORAGE)
	@mkdir -p $$(dir $$@)
	./src/select.py -i $$< -o $$@ 'machine==$1' 'batch==$2 $3' 'st_mtime>=1553698800'
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

