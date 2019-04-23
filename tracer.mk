TRACER_TGZ=$(shell find ~/storage/ -name tracer.tgz)
RQSIZE_NPZ=$(TRACER_TGZ:%/tracer.tgz=%/rqsize.npz)
ALL_NPZ+=$(RQSIZE_NPZ)

%/rqsize.npz: %/tracer.tgz ./src/parse_rqsize.py
	./src/parse_rqsize.py $@ $<
