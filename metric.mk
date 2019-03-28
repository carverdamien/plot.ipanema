SCHED_DEBUG_METRICS=nr_migrations nr_sleep nr_switches nr_wakeup
SCHED_MONITOR_METRICS=sched_total_ns idle_total_ns fair_total_ns ipanema_total_ns
COMMON_METRICS=$(SCHED_DEBUG_METRICS) $(SCHED_MONITOR_METRICS)
define metric
./src/plotly/$1.py: ./src/plotly/metric.py
	ln -sf ./metric.py $$@
./src/seaborn/$1.py: ./src/seaborn/metric.py
	ln -sf ./metric.py $$@
endef
