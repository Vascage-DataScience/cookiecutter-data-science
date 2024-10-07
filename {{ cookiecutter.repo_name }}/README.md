# {{cookiecutter.project_name}}

## Datastorage
If you are using the data-storage option, make sure you installed the monai client from [here]{https://min.io/docs/minio/linux/reference/minio-mc.html}
For Windows you can simply download the binary and link it in the PATH-Variable.
Download for Windows:
```
https://dl.min.io/client/mc/release/windows-amd64/mc.exe
```

For Linux you can download the application via CURL
```
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/

mc --help
```


<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

{{cookiecutter.description}}

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         {{ cookiecutter.module_name }} and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── {{ cookiecutter.module_name }}   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes {{ cookiecutter.module_name }} a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

# MONAI setup, configuration and deployability
## Deploy
### Overview
**Application:** An application represents a collection of computational tasks that together accomplish a meaningful goal in the healthcare domain. Typically, an app defines a workflow that reads medical imaging data from disk, processes it in one or more operators (some of which could be AI inference related), and produces output data. User implements an app by subclassing Application class. An app makes use of instances of Operators as stages in the application.

**Graph:** The SDK provides a mechanism to define a directed acyclic graph (through Graph classes) which can be composed of operators. This acyclic property is important, as it prevents the framework from running into circular dependencies between operators. The graph consists of one or more vertices and edges, with each edge directed from one vertex to another, such that there is no way to start at any vertex and follow a consistently directed sequence of edges that eventually loops back to the same vertex again. Each vertex in the graph represents an Operator. The edge between two operators contains connectivity information.

**Operator:** An operator is the smallest unit of computation. It is implemented by the user by inheriting a class from the Operator. An operator is an element of a MONAI Deploy Application. Each operator is typically designed to perform a specific function/analysis on incoming input data. Common examples of such functions are: reading images from disk, performing image processing, performing AI inference, writing images to disk, etc. The SDK comes with a bundled set of operators.

**Executor:** An executor in the SDK is an entity that ingests an Application, parses the Directed Acyclic Graph inside it, and executes the operators in the specified order. The SDK has provisions to support multiple types of Executors depending on single/multi-process and execution order needs. The same executor executes the application either directly on the host system or in a MAP as a containerized application.

### Run-Time Concepts

The core runtime concepts in the MONAI Deploy App SDK are the MONAI Application Package (MAP) and a MONAI Application Runner (MAR). A key design decision of the SDK is to make the framework runtime-agnostic. The same code should be runnable in various environments, such as on a workstation during development or on a production-ready workflow orchestrator during production.

**MONAI Application Packager:** Once an application is built using the MONAI App SDK, it can be packaged into a portable MONAI Application Package (MAP). A MAP contains an executable application and provides sufficient information to execute the application as intended. As such, it consists of a single container image with embedded metadata to describe the additional information about the application, along with a mechanism for extracting the contents. For example, it provides information about its expected inputs such that an external agent is able to determine if the MAP is capable of receiving a workload. The MAP container image also complies with Open Container Initiative (OCI) format standards. To ensure consistency and ease of use, the MONAI Application Packager utility is provided to help developers to package an app written using the SDK into a MAP.

**MONAI Application Runner:** The MONAI Application Runner (MAR) is a command-line utility that allows users to run and test their MONAI Application Package (MAP) locally. MAR is developed to make the running and testing of MAPs locally an easy process for developers by abstracting away the need to understand the internal details of the MAP. MAR allows users to specify input and output paths on the local file system which it maps to the input and output of MAP during execution.

### Directory Structure

A MONAI-Deploy is defined primarily as a directory with a set of specifically named subdirectories containing the model, input/output files and the application code. The root directory should be named for the project, given as “Project” in this example, and should contain the following structure:
```
ProjectName
┣━ input
   ┗━ * files{dcm,mhd,json,txt,csv,...}
┣━ output
   ┗━ * files{dcm,mhd,json,txt,csv,...}
┣━ models
┃  ┗━ model.pt
┣━ * scripts
     ┣━ *app.py
     ┗━ *operator1.py
┣━ * __init__.py
┣━ __main__.py
┣━ requirements.txt
┣━ app.yaml
┗━ docs
   ┣━ *README.md
   ┗━ *license.txt
```
You can checkout the files to have a reference.

### Create a deployable container
To create a deployable container into the monai-framework you have to first create a package called MAP. If you have setup your project structure correctly and your code is valid, you should be able to execute this command:
```
monai-deploy package . -c app.yaml -t {your-project}:latest --platform x64-workstation -l DEBUG
```
If this command was succesful try to execute:
```
monai-deploy run {your-project}-x64-workstation-dgpu-linux-amd64:1.0 -l DEBUG
```
You can also change the path to the input/output/model by setting the following flags
```
monai-deploy run {your-project}-x64-workstation-dgpu-linux-amd64:1.0 -i input -o output -m model -l DEBUG
```
If everything worked as expected, we are now trying to add the workflow to the monai-framework, therefor we are creating file called {your-project-name}-workflow.json with following content:

```
{
	"name": "mri-generation-cl",
	"version": "1.0.0",
	"description": "Generate a brain mri",
	"informatics_gateway": {
		"ae_title": "MRIGen-Cl",
		"data_origins": [
			"ORTHANC"
		],
		"export_destinations": [
			"ORTHANC"
		]
	},
	"tasks": [
		{
			"id": "router",
			"description": "router task",
			"type": "router",
			"task_destinations": [
				{
					"name": "mri-generation",
					"conditions": []
				}
			]
		},
		{
			"id": "mri-generation",
			"description": "Execute MRI Generation MAP",
			"type": "docker",
			"args": {
				"container_image": "vadskb/{your-project}:latest",
				"server_url": "unix:///var/run/docker.sock",
				"entrypoint": "/bin/bash,-c",
				"command": "python3 -u /opt/holoscan/app/__main__.py",
				"task_timeout_minutes": "5",
				"temp_storage_container_path": "/var/lib/mde/",
				"env_MONAI_INPUTPATH": "/var/holoscan/input/",
				"env_MONAI_OUTPUTPATH": "/var/holoscan/output/",
				"env_MONAI_MODELPATH": "/opt/holoscan/models/",
				"env_MONAI_WORKDIR": "/var/holoscan/"
			},
			"artifacts": {
				"input": [
					{
						"name": "env_MONAI_INPUTPATH",
						"value": " context.input.dicom "
					}
				],
				"output": [
					{
						"name": "env_MONAI_OUTPUTPATH",
						"mandatory": true
					}
				]
			},
			"task_destinations": [
				{
					"name": "export-mri-cl"
				}
			]
		},
		{
			"id": "export-mri-cl",
			"description": "Export Classification Storage Object",
			"type": "export",
			"export_destinations": [
				{
					"Name": "ORTHANC"
				}
			],
			"artifacts": {
				"input": [
					{
						"name": "export-dicom",
						"value": " context.executions.brain.artifacts.env_MONAI_OUTPUTPATH ",
						"mandatory": true
					}
				],
				"output": []
			}
		}
	]
}

```
Before you push that file to the Informatics Gateway,
open the config-ig.sh in the monai-deploy-va repository and add the following line:

```
echo "Informatics Gateway IP Address = $1"
echo "Informatics Gateway Port       = $2"

printf "\nAdding MONAI Deploy MRI-Generator AE Title\n"
curl --request POST "http://$1:$2/config/ae" --header "Content-Type: application/json" --data-raw "{\"name\": \"MRI Brain Generator\",\"aeTitle\": \"MRIGen-Cl\"}"  | jq
```

Push the workflow to the workflow manager by executing:
```
curl --fail-early --no-keepalive --show-error --header 'Content-Type: application/json'  --data "@{your-project-name}-workflow.json"  http://localhost:5001/workflows
```


## Bundle
### Overview
This is the specification for the MONAI Bundle (MB) format of portable described deep learning models. The objective of a MB is to define a packaged network or model which includes the critical information necessary to allow users and programs to understand how the model is used and for what purpose. A bundle includes the stored weights of a single network as a pickled state dictionary plus optionally a Torchscript object and/or an ONNX object. Additional JSON files are included to store metadata about the model, information for constructing training, inference, and post-processing transform sequences, plain-text description, legal information, and other data the model creator wishes to include.

This specification defines the directory structure a bundle must have and the necessary files it must contain. Additional files may be included and the directory packaged into a zip file or included as extra files directly in a Torchscript file.

### Directory Structure

A MONAI Bundle is defined primarily as a directory with a set of specifically named subdirectories containing the model, metadata files and license. The root directory should be named for the model, given as “ModelName” in this example, and should contain the following structure:
```
ModelName
┣━ LICENSE
┣━ configs
┃  ┗━ metadata.json
┣━ models
┃  ┣━ model.pt
┃  ┣━ *model.ts
┃  ┗━ *model.onnx
┗━ docs
   ┣━ *README.md
   ┗━ *license.txt
```
The following files are required to be present with the given filenames for the directory to define a valid bundle:
```
    LICENSE: a license for the software itself comprising the configuration files and model weights.

    metadata.json: metadata information in JSON format relating to the type of model, definition of input and output tensors, versions of the model and used software, and other information described below.

    model.pt: the state dictionary of a saved model, the information to instantiate the model must be found in the metadata file.
```
The following files are optional but must have these names in the directory given above:
```
    model.ts: the Torchscript saved model if the model is compatible with being saved correctly in this format.

    model.onnx: the ONNX model if the model is compatible with being saved correctly in this format.

    README.md: plain-language information on the model, how to use it, author information, etc. in Markdown format.

    license.txt: software license attached to the data, can be left blank if no license needed.
```
Other files can be included in any of the above directories. For example, configs can contain further configuration JSON or YAML files to define scripts for training or inference, overriding configuration values, environment definitions such as network instantiations, and so forth. One common file to include is inference.json which is used to define a basic inference script which uses input files with the stored network to produce prediction output files.

### metadata.json File
This file contains the metadata information relating to the model, including what the shape and format of inputs and outputs are, what the meaning of the outputs are, what type of model is present, and other information. The JSON structure is a dictionary containing a defined set of keys with additional user-specified keys. 

See the file for an example

### Project structure
The monai.bundle module supports building Python-based workflows via structured configurations.

The main benefits are threefold:
* it provides good readability and usability by separating system parameter settings from the Python code.
* it describes workflow at a relatively high level and allows for different low-level implementations.
* learning paradigms at a higher level such as federated learning and AutoML can be decoupled from the component details.

Components as part of a workflow can be specified using JSON or YAML syntax, for example, a network architecture definition could be stored in a demo_config.json file with the following content:
```
{
  "demo_net": {
    "_target_": "monai.networks.nets.BasicUNet",
    "spatial_dims": 3,
    "in_channels": 1,
    "out_channels": 2,
    "features": [16, 16, 32, 32, 64, 64]
  }
}
```
or alternatively, in YAML format (demo_config.yaml):
```
demo_net:
  _target_: monai.networks.nets.BasicUNet
  spatial_dims: 3
  in_channels: 1
  out_channels: 2
  features: [16, 16, 32, 32, 64, 64]
```
The configuration parser can instantiate the component as a Python object:
```
from monai.bundle import ConfigParser

config = ConfigParser()

config.read_config("demo_config.json")

net = config.get_parsed_content("demo_net", instantiate=True)
BasicUNet features: (16, 16, 32, 32, 64, 64).

print(type(net))
<class 'monai.networks.nets.basic_unet.BasicUNet'>
```
or additionally, tune the input parameters then instantiate the component:
```
config["demo_net"]["features"] = [32, 32, 32, 64, 64, 64]

net = config.get_parsed_content("demo_net", instantiate=True)
BasicUNet features: (32, 32, 32, 64, 64, 64).
```
For more details on the ConfigParser API, please see monai.bundle.ConfigParser.

### Hybrid solution
Instead of just using the command-line tool we can load the configuration and execute certain steps like the inference or generation by hand.
That gives us more freedom for debugging the application, seen in this example:

```
import os

import torch
import nibabel as nib
import numpy as np
from monai.bundle import config_parser

def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    model_config = config_parser.ConfigParser()
    model_config.read_config("./configs/inference.json")
    
    # we could change here the input or output files, but not necessary
    # it is important to do that before the initialization
    # model_config["output_dir"] = "./tmp"
    
    model_path = os.path.join("models","model.pt")
    
    
    #preprocessing = model_config.get_parsed_content("preprocessing")
    model = model_config.get_parsed_content("network").to(device)
    generator = model_config.get_parsed_content("generated_image")
    #postprocessing = model_config.get_parsed_content("postprocessing")
    #dataloader = model_config.get_parsed_content("dataloader")
    
    model.load_state_dict(torch.load(model_path,map_location=device))
    model.eval()
    
    generated = generator[0]
    generated = generated.cpu().numpy().squeeze()
    np_generated = np.stack(generated,dtype=np.float32)
    
    final_img = nib.Nifti1Image(np_generated, affine=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    nib.save(final_img, os.path.join("output", 'test.nii.gz'))
    
```

### Command line interface
In addition to the Pythonic APIs, a few command line interfaces (CLI) are provided to interact with the bundle. 

To predict or generate an image, just type in:
```
python -m monai.bundle run --config_file configs/inference.json
```

The primary usage is:
```
python -m monai.bundle COMMANDS
```
where COMMANDS is one of the following: run, verify_metadata, ckpt_export, … (please see python -m monai.bundle --help for a list of available options).

The CLI supports flexible use cases, such as overriding configs at runtime and predefining arguments in a file. To display a usage page for a command, for example run:
```
python -m monai.bundle run -- --help
```
The support is provided by Python Fire, please make sure the optional dependency is installed, for example, using pip install monai[fire] or pip install fire. Details on the CLI argument parsing is provided in the Python Fire Guide.


