
import os
import sys
import traceback

from airflow import DAG
from importlib import  import_module

# initialize airflow base dir
AIRFLOW_BASE =  os.path.dirname(
                os.path.dirname(
                os.path.abspath(__file__)))
sys.path.append(AIRFLOW_BASE)


class DAGFactory(object):
"""
  Dag factory: collect dags from all sub folders under ./airflow/projects
"""

    def __init__(self):
        self.project_base = os.path.join(
                                  AIRFLOW_BASE 
                                , 'projects' )

    @property
    def projects(self):
        return list(
                    filter( lambda x : x not in ['__pycache__', '.idea'] ,
                            [dirs for _, dirs, _ in os.walk(self.project_base) ][0]) )

    def get_modules_from_all_projects(self):

        for project_name in self.projects:
            try:
                module_name = "projects.{}.DAG".format(project_name)
                prj_mod = import_module(module_name)
                no_of_project_dags = 1

                for dag in prj_mod.DAGS:
                    var_name = '{}-{}'.format(project_name, no_of_project_dags)

                    # create unique name for project in global namespace
                    globals()[var_name] = dag

                    no_of_project_dags += 1
            except Exception as e:
                print( traceback.format_exc() )



dags = DAGFactory()
print( dags.projects )

dags.get_modules_from_all_projects()
