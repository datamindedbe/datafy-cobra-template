from airflow import DAG
from datafy_airflow_plugins.datafy_container_plugin.datafy_container_operator import (
    DatafyContainerOperator,
)
from datetime import datetime, timedelta


{% set start_date = cookiecutter.workflow_start_date.split('-') -%}
default_args = {
    "owner": "Datafy",
    "depends_on_past": False,
    "start_date": datetime(year={{ start_date[0] }}, month={{ start_date[1].lstrip("0") }}, day={{ start_date[2].lstrip("0") }}),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}


image = "{% raw %}{{ macros.image('{% endraw %}{{ cookiecutter.project_name }}{% raw %}') }}{% endraw %}"

dag = DAG(
    "{{ cookiecutter.project_name }}",
    default_args=default_args,
    schedule_interval="{{ cookiecutter.workflow_schedule }}",
    max_active_runs=1
)

preprocessing = DatafyContainerOperator(
    dag=dag,
    task_id="preprocessing",
    name="preprocessing",
    image=image,
    arguments=["--date", "{% raw %}{{ ds }}{% endraw %}", "--jobs", "preprocessing", "--env", "{% raw %}{{ macros.env() }}{% endraw %}"],
    service_account_name="{{ cookiecutter.project_name }}",
)

pig_tables = DatafyContainerOperator(
    dag=dag,
    task_id="pig_tables",
    name="pig_tables",
    image=image,
    arguments=["--date", "{% raw %}{{ ds }}{% endraw %}", "--jobs", "pig_tables", "--env", "{% raw %}{{ macros.env() }}{% endraw %}"],
    service_account_name="{{ cookiecutter.project_name }}",
)

model_train = DatafyContainerOperator(
    dag=dag,
    task_id="model_train",
    name="model_train",
    image=image,
    arguments=["--date", "{% raw %}{{ ds }}{% endraw %}", "--jobs", "model_training", "--env", "{% raw %}{{ macros.env() }}{% endraw %}"],
    service_account_name="{{ cookiecutter.project_name }}",
)

model_run = DatafyContainerOperator(
    dag=dag,
    task_id="model_run",
    name="model_run",
    image=image,
    arguments=["--date", "{% raw %}{{ ds }}{% endraw %}", "--jobs", "model_run", "--env", "{% raw %}{{ macros.env() }}{% endraw %}"],
    service_account_name="{{ cookiecutter.project_name }}",
)

preprocessing >> pig_tables
preprocessing >> model_train >> model_run