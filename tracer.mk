ifndef TRACER_TGZ
TRACER_TGZ=$(shell find ~/storage/ -name tracer.tgz)
endif
ifndef RQSIZE_HDF5
RQSIZE_HDF5=$(TRACER_TGZ:%/tracer.tgz=%/rqsize.hdf5)
endif
# ifndef IDLE_TIME_NPZ
# IDLE_TIME_NPZ=$(RQSIZE_NPZ:%/rqsize.npz=%/idle_time.npz)
# endif
ALL_HDF5+=$(RQSIZE_HDF5) # $(IDLE_TIME_NPZ)

%/rqsize.hdf5: %/tracer.tgz ./src/parse_rqsize.py
	rm -f $@
	./src/parse_rqsize.py $@ $<

# %/idle_time.npz: %/rqsize.npz ./src/idle_time.py
# 	./src/idle_time.py $@ $<

# i80/all_idle_time: $(IDLE_TIME_NPZ)
# 	rm -rf $@
# 	mkdir -p $@
#	./src/plotly/all_idle_time.py $@ $^
