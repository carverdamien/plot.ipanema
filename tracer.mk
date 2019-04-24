ifndef TRACER_TGZ
TRACER_TGZ=$(shell find ~/storage/ -name tracer.tgz)
endif
ifndef RQSIZE_HDF5
RQSIZE_HDF5=$(TRACER_TGZ:%/tracer.tgz=%/rqsize.hdf5)
endif
ifndef IDLE_ITERVAL_HDF5
IDLE_ITERVAL_HDF5=$(RQSIZE_HDF5:%/rqsize.hdf5=%/idle_interval.hdf5)
endif
ALL_HDF5+=$(RQSIZE_HDF5) $(IDLE_ITERVAL_HDF5)

%/rqsize.hdf5: %/tracer.tgz | ./src/parse_rqsize.py
	./src/parse_rqsize.py $@.tmp $<
	mv $@.tmp $@

%/idle_interval.hdf5: %/rqsize.hdf5 | ./src/idle_time.py
	./src/idle_interval.py $@.tmp $<
	mv $@.tmp $@

# i80/all_idle_time: $(IDLE_TIME_NPZ)
# 	rm -rf $@
# 	mkdir -p $@
#	./src/plotly/all_idle_time.py $@ $^
