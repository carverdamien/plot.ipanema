STACK_METRICS=time_stack enQ_stack deQ_stack
SCHED_DEBUG_METRICS=enQ_no_reason enQ_new enQ_wakeup enQ_wakeup_mig enQ_lb_mig deQ_no_reason deQ_sleep enQ_wc_no_reason enQ_wc_new enQ_wc_wakeup enQ_wc_wakeup_mig enQ_wc_lb_mig deQ_wc_no_reason deQ_wc_sleep
SCHED_MONITOR_METRICS=sched_total_ns idle_total_ns fair_total_ns ipanema_total_ns
COMMON_METRICS=$(SCHED_DEBUG_METRICS) $(SCHED_MONITOR_METRICS) $(STACK_METRICS)
define metric
./src/plotly/$1.py:
	ln -s ./metric.py $$@
./src/seaborn/$1.py:
	ln -s ./metric.py $$@
endef
