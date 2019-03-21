define metric
./src/plotly/$1.py: ./src/plotly/metric.py
	ln -sf ./metric.py $$@
./src/seaborn/$1.py: ./src/seaborn/metric.py
	ln -sf ./metric.py $$@
endef
