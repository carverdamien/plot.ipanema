import os, logging
from common import *

class Oltp:

    def _parse_oltp_file_or_path(self, path=None, fp=None):
        if fp:
            return self._parse_oltp_file(fp)
        if path:
            with open(path, 'r') as fp:    
                return self._parse_oltp_file(fp)
        raise TypeError

    def _parse_oltp_file(self, fp):
        values = []
        for l in fp:
            s = l.strip().split()
            if 'Number of threads:' in l:
                if 'res' in locals():
                    if len(res) == 8:
                        values.append(res)
                res = { 'clients': int(s[3]),
                        'file':    fp.name }
            elif 'eps' in l:
                res['throughput'] = float(s[2])
            elif 'min:' in l:
                res['min_latency'] = float(s[1])
            elif 'avg:' in l:
                res['avg_latency'] = float(s[1])
            elif 'max:' in l:
                res['max_latency'] = float(s[1])
            elif '95th percentile:' in l:
                res['95th_latency'] = float(s[2])
            elif 'time elapsed:' in l:
                res['duration'] = float(s[2][:-1])
        if 'res' in locals():
            if len(res) == 8:
                values.append(res)
        return values

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
                values.extend(self._parse_oltp_file_or_path(path=p))

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
            logging.error("Oltp parser did not find {} file.".format(e.filename))
            raise ParsingError()
