# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from io import StringIO
import json
import tempfile

from etl.executors.batch_work_executor import BatchWorkExecutor

from etl.jobs.base_job import BaseJob
from etl.jobs.exporters.base_exporter import BaseExporter
from etl.jobs.importers.base_importer import BaseImporter
from etl.jobs.importers.oracle_importer import OracleImporter


# Exports contracts bytecode
class DwEtlJob(BaseJob):
    def __init__(
            self,
            job_id: str,
            batch_size: int,
            max_workers: int,
            item_importer: BaseImporter,
            item_exporter: BaseExporter):
        self.brcd_paginations_iterable = [
            ['1000', '1200'],
            ['1201', '2200']
        ]

        self.job_id = job_id

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        
        self.item_importer = item_importer
        self.item_exporter = item_exporter
        self.data_state_db = OracleImporter()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(self.brcd_paginations_iterable, self._export_data)

    def _export_data(self, brcd_paginations):
        job_data = self.data_state_db.import_item(f"select * from DS_JOB where id = {self.job_id}")
       
        query = job_data["SQL"]
        query = query.replace(':from_brcd', brcd_paginations[0])
        query = query.replace(':to_brcd', brcd_paginations[1])

        data = self.item_importer.import_item(query=job_data['SQL'])
        
        self.item_exporter.export_item(data)

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
