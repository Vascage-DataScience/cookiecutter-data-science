# {{ cookiecutter.project_name }} documentation!
{% if cookiecutter.project_description is not none %}
## Description

{{ cookiecutter.description}}
{% endif %}
## Commands

The Makefile contains the central entry points for common tasks related to this project.
{% if not cookiecutter.dataset_storage.none %}
### Syncing data to cloud storage

{% if cookiecutter.dataset_storage.s3 -%}
* `make sync_data_up` will use `mc cp --recursive` to recursively sync files in `data/` up to `s3://{{ cookiecutter.dataset_storage.s3.URI }}/{{ cookiecutter.project_name }}/`.
* `make sync_data_down` will use `mc cp --recursive` to recursively sync files from `s3://{{ cookiecutter.dataset_storage.s3.URI }}/{{ cookiecutter.project_name }}/` to `data/`.
{% endif %}
{% endif %}
