ifndef TRACER_TGZ
TRACER_TGZ=$(shell find ~/storage/ -name tracer.tgz)
endif
ifndef RQSIZE_NPZ
RQSIZE_NPZ=$(TRACER_TGZ:%/tracer.tgz=%/rqsize.npz)
endif
ifndef IDLE_TIME_NPZ
IDLE_TIME_NPZ=$(RQSIZE_NPZ:%/rqsize.npz=%/idle_time.npz)
endif
ALL_NPZ+=$(RQSIZE_NPZ) $(IDLE_TIME_NPZ)

%/rqsize.npz: %/tracer.tgz ./src/parse_rqsize.py
	./src/parse_rqsize.py $@ $<

%/idle_time.npz: %/rqsize.npz ./src/idle_time.py
	./src/idle_time.py $@ $<
