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


import click

from dwetl.jobs.dw_etl_job import DwEtlJob
from etl.jobs.exporters.hadoop_exporter import HadoopExporter
from etl.jobs.importers.oracle_spark_importer import OracleSparkImporter
from spark.spark import Spark

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-sm', '--spark-master', default="local[1]", show_default=True, type=str, help='The spark master')
@click.option('-oracleurl', '--oracle-url', type=str, help='The oracle url')
@click.option('-oracleuser', '--oracle-user', type=str, help='The oracle user')
@click.option('-oraclepass', '--oracle-password', type=str, help='The oracle password')
@click.option('-b', '--batch-size', default=3, show_default=True, type=int, help='The number of blocks to filter at a time.')
@click.option('-w', '--max-workers', default=5, show_default=True, type=int, help='The maximum number of workers.')
def oracle_to_hudi(spark_master, oracle_url, oracle_user, oracle_password, batch_size, max_workers):
    spark = Spark(spark_master, "Test")
    item_importer = OracleSparkImporter(spark, oracle_url, oracle_user, oracle_password)
    item_exporter=HadoopExporter(spark)

    job = DwEtlJob(
        batch_size=batch_size, 
        max_workers=max_workers, 
        item_importer=item_importer,
        item_exporter=item_exporter
    )

    job.run()
