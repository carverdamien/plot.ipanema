import os, logging, json, parse
from common import *

class ProcStat:
    # https://elixir.bootlin.com/linux/v4.19/source/fs/proc/stat.c
    PROC_STAT_EXPECTED_OUTPUT = """cpu  {user} {nice} {system} {idle} {iowait} {irq} {softirq} {steal} {guest} {guest_nice}"""
    def _parse_path(self, path):
        st_mtime = os.stat(path).st_mtime
        data = {
            'file' : path,
            'st_mtime' : st_mtime,
        }
        with open(path, 'r') as fp:
            r = parse.search(self.PROC_STAT_EXPECTED_OUTPUT,fp.read())
            data.update({
                k:int(r.named[k])
                for k in r.named
            })
            return data
        raise ParsingError()
    def parse(self, dirPath):
        try:
            begin = self._parse_path(dirPath+'/stat.begin')
            end = self._parse_path(dirPath+'/stat.end')
            return { k:end[k]-begin[k] for k in begin if k not in ['file','st_mtime'] }
        except FileNotFoundError as e:
            logging.warn('In ProcStat: {}'.format(e))
            pass
        return {}

class SchedMonitor:
    SCHED_MONITOR_EXPECTED_OUTPUT = {
        'sched' : """{total_ns:d}""",
        'idle'    : """Idle: {total_ns} ns ({total_hits} hits)""",
        'fair'    : """{:s}{event_name}: {event_ns} ns ({event_hits} hits)""",
        'ipanema' : """{:s}{event_name}: {event_ns} ns ({event_hits} hits)""",
    }
    def _parse_one_cpu(self, path, subsystem):
        expected_output = self.SCHED_MONITOR_EXPECTED_OUTPUT[subsystem]
        with open(path, 'r') as fp:
            data = {}
            for r in parse.findall(expected_output,fp.read()):
                if subsystem == 'sched':
                    return {
                        'total_ns': int(r.named['total_ns'])
                    }
                if subsystem == 'idle':
                    return {
                        'total_ns': int(r.named['total_ns']),
                        'total_hits': int(r.named['total_hits'])
                    }
                event_name = r.named['event_name']
                event_ns   = int(r.named['event_ns'])
                event_hits = int(r.named['event_hits'])
                data['total_ns'] = data.get('total_ns', 0) + event_ns
                data['total_hits'] = data.get('total_hits', 0) + event_hits
                data.update({
                    '{}_ns'.format(r.named['event_name']) : event_ns,
                    '{}_hits'.format(r.named['event_name']) : event_hits,
                })
            return data
        raise ParsingError()
    def parse(self, dirPath):
        all_data = {}
        for subsystem in self.SCHED_MONITOR_EXPECTED_OUTPUT:
            path = "/".join([dirPath, subsystem])
            if not os.path.isdir(path):
                logging.warn('SchedMonitor parser did not find {}'.format(path))
                continue
            data = {}
            for cpu in os.listdir(path):
                filepath = "/".join([path, cpu])
                cpu = self._parse_one_cpu(filepath, subsystem)
                for k in cpu:
                    data[k] = data.get(k, 0) + cpu[k]
            all_data.update({
                '{}_{}'.format(subsystem,k) : data[k]
                for k in data
            })
        return all_data

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
        if len(values) == 0:
            logging.warn('SchedDebug parser did not find sched_debug files in {}.'.format(dirPath))
            return {}
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
                    data.update(ProcStat().parse(dirPath+"/log/"+f))
                    data.update(SchedDebug().parse(dirPath+"/log/"+f))
                    data.update(SchedMonitor().parse(dirPath+"/log/"+f+"/sched_monitor"))
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
                    data.update(ProcStat().parse(dirPath+"/log/"+f))
                    data.update(SchedDebug().parse(dirPath+"/log/"+f))
                    data.update(SchedMonitor().parse(dirPath+"/log/"+f+"/sched_monitor"))
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
