import os, logging, json, parse
from common import *

class Batch:
    def _parse_path(self, path):
        st_ctime = os.stat(path).st_ctime
        with open(path, 'r') as fp:
            data = json.load(fp)
            data['st_ctime'] = st_ctime
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
                    values.append(self._parse_path(path=p))
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
        st_ctime = os.stat(path).st_ctime
        with open(path,'r') as fp:
            r = parse.search(self.SYSBENCH_EXPECTED_OUTPUT,fp.read())
            data = r.named
            data['file'] = path
            data['st_ctime'] = st_ctime
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
                    values.append(self._parse_path(path=p))
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
