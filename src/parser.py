import os, logging, json, parse
from common import *

class SchedDebug:
    SCHED_DEBUG_EXPECTED_OUTPUT="""
cpu#{}, {} MHz
  .nr_running                    : {}
  .load                          : {}
  .nr_switches                   : {nr_switches}
  .nr_migrations                 : {nr_migrations}
  .nr_sleep                      : {nr_sleep}
  .nr_wakeup                     : {nr_wakeup}
  .nr_load_updates               : {nr_load_updates}
  .nr_uninterruptible            : {nr_uninterruptible}
  .next_balance                  : {}
  .curr->pid                     : {}
  .clock                         : {}
  .clock_task                    : {}
  .cpu_load[0]                   : {}
  .cpu_load[1]                   : {}
  .cpu_load[2]                   : {}
  .cpu_load[3]                   : {}
  .cpu_load[4]                   : {}
  .avg_idle                      : {}
  .max_idle_balance_cost         : {}
"""
    def _parse_path(self, path):
        st_mtime = os.stat(path).st_mtime
        data = {
            'file' : path,
            'st_mtime' : st_mtime,
        }
        with open(path, 'r') as fp:
            for r in parse.findall(self.SCHED_DEBUG_EXPECTED_OUTPUT,fp.read()):
                for k in r.named:
                    v = int(r.named[k])
                    data[k] = data.get(k,0) + v
            return data
    def parse(self, dirPath):
        values = []
        for f in os.listdir(dirPath):
            if 'sched_debug' not in f:
                continue
            p = dirPath+"/"+f
            values.append(self._parse_path(p))
        if len(values) != 2:
            logging.error('SchedDebug did not find exactly two dumps in {}.'.format(dirPath))
            return {}
        if values[0]['st_mtime'] < values[1]['st_mtime']:
            old, new = values
        else:
            new, old = values
        return { k:new[k]-old[k] for k in new if k not in ['file','st_mtime'] }

class Batch:
    def _parse_path(self, path):
        st_mtime = os.stat(path).st_mtime
        with open(path, 'r') as fp:
            data = json.load(fp)
            data['st_mtime'] = st_mtime
            data['file'] = path
            return data
    def parse(self, dirPath):
        try:
            values = []
            with open(dirPath+"/machine") as fp:
                machine = fp.read().strip()
            with open(dirPath+"/batch") as fp:
                batch = fp.read().strip()
            with open(dirPath+"/scheduler") as fp:
                scheduler = fp.read().strip()
            with open(dirPath+"/kernel") as fp:
                kernel = fp.read().strip()
            for f in os.listdir(dirPath+"/data/"):
                p = dirPath+"/data/"+f
                try:
                    data = self._parse_path(path=p)
                    data.update(SchedDebug().parse(dirPath+"/log/"+f))
                    values.append(data)
                except json.decoder.JSONDecodeError as e:
                    logging.error("Batch parser failed on file {}.".format(p))
                    pass
            return {
                'machine': machine,
                'batch':  batch,
                'scheduler': scheduler,
                'kernel': kernel,
                'data': values,
            }
        except FileNotFoundError as e:
            logging.error("Batch parser did not find {} file.".format(e.filename))
            raise ParsingError()
        
class Sysbench:
    SYSBENCH_EXPECTED_OUTPUT="""
Number of threads:{:s}{clients}
{}
Throughput:
    events/s (eps):{:s}{throughput}
    time elapsed:{:s}{duration}s
    total number of events:{:s}{events}

Latency (ms):
         min:{:s}{min_latency}
         avg:{:s}{avg_latency}
         max:{:s}{max_latency}
         95th percentile:{:s}{p95th_latency}
         sum:{:s}{sum_latency}
"""
    def _parse_path(self, path):
        st_mtime = os.stat(path).st_mtime
        with open(path,'r') as fp:
            r = parse.search(self.SYSBENCH_EXPECTED_OUTPUT,fp.read())
            data = r.named
            data['file'] = path
            data['st_mtime'] = st_mtime
            return data

    def parse(self, dirPath):
        try:
            values = []
            with open(dirPath+"/machine") as fp:
                machine = fp.read().strip()
            with open(dirPath+"/engine") as fp:
                engine = fp.read().strip()
            with open(dirPath+"/engine_scheduler") as fp:
                engine_scheduler = fp.read().strip()
            with open(dirPath+"/client") as fp:
                client = fp.read().strip()
            with open(dirPath+"/client_scheduler") as fp:
                client_scheduler = fp.read().strip()
            with open(dirPath+"/kernel") as fp:
                kernel = fp.read().strip()
            for f in os.listdir(dirPath+"/data/"):
                p = dirPath+"/data/"+f
                try:
                    data = self._parse_path(path=p)
                    data.update(SchedDebug().parse(dirPath+"/log/"+f))
                    values.append(data)
                except AttributeError as e:
                    logging.error("Sysbench parser failed on file {}.".format(p))
                    pass
            return {
                'machine': machine,
                'engine':  engine,
                'engine_sched': engine_scheduler,
                'client': client,
                'client_sched': client_scheduler,
                'kernel': kernel,
                'data': values
            }
        except FileNotFoundError as e:
            logging.error("Sysbench parser did not find {} file.".format(e.filename))
            raise ParsingError()
