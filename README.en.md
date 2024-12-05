# UnityChip For XiangShan Processor

English | [中文](/README.zh.md)

This project aims to perform unit testing (Unit Test, UT) on the Kunminghu architecture of the [XiangShan Processor](https://github.com/OpenXiangShan/XiangShan) through open-source crowdsourcing. Python is chosen as the primary verification language for this project. By participating in the verification, you will learn the following:

1. **Circuit Characteristics**: Observe the characteristics of circuits from a software perspective and gain an in-depth understanding of circuit design principles.
2. **High-Performance Processor Design**: Learn the Chisel hardware description language, study related code and papers, and master the latest architectural design concepts.
3. **Chip Verification Process**: Familiarize yourself with specification documents (Spec documents), learn how to perform UT verification, and evaluate the rationality of verification results.
4. **Python Verification**: Master advanced programming patterns such as asynchronous programming and callbacks, and use Python for chip verification.
5. **Linux Environment**: Learn basic Linux commands and set up the verification environment.

This project welcomes contributions in various aspects and will provide rewards (such as bonuses, certificates, internship opportunities, etc.) within a certain period. Specific types of contributions include:

- **# 1**: Write verification documents, including specification documents, instruction documents, functional description documents, etc., for the Design Under Test (DUT).
- **# 2**: Develop test cases, including test code and comments for each functional point, as well as related instruction documents.
- **# 3**: Discover and report bugs in the XiangShan Processor, and provide cause analysis and repair suggestions.
- **# 4**: Other contributions, such as adding new features to the tools provided by this project.

UnityChip project website: [https://open-verify.cc](https://open-verify.cc)

We look forward to your participation!

#### Quick Start

Refer to the [Environment Preparation](https://open-verify.cc/UnityChipForXiangShan/docs/01_verfiy_env/) to set up the basic environment, and then run the following commands:

```bash
git clone git@github.com:XS-MLVP/UnityChipForXiangShan.git
cd UnityChipForXiangShan
pip3 install -r requirements.txt
make all
```

The above commands will automatically perform the following operations:

1. Download the RTL code;
1. Compile all available modules to be verified;
1. Search for all Python files starting with `test_` in the `ut_*` directories and run the test cases starting with `test_` in them;
1. Generate test reports (the test reports are located in the `out` directory);
1. Update statistical data.


*By default, tests that are too time-consuming will be skipped. You can run all test cases by setting `CFG=configs/noskip.yaml`， eg:

```bash
make all CFG=configs/noskip.yaml
```

#### Display Docs and Data Locally

Follow the [Documentation Deployment Instructions](https://github.com/XS-MLVP/UnityChipForXiangShan/blob/main/documents/README.md) to set up the `hugo` environment, and then execute:

```bash
cd UnityChipForXiangShan
make doc
```

After executing the above commands, you will see output similar to:

```bash
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at //localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
```

At this point, you can access the provided address ([http://127.0.0.1:1313](http://127.0.0.1:1313/)) through your browser.

#### Test In Docker
To quickly run tests using Docker, you can execute the following commands:

```bash
sudo docker pull ghcr.io/xs-mlvp/uc4xs:latest                       # Pull the image
sudo docker run --rm ghcr.io/xs-mlvp/uc4xs:latest /home/run_ci.sh   # Run the tests
```

#### Additional Information

- **Code of Conduct:** [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- **How to Contribute:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Security Issues:** [SECURITY.md](SECURITY.md)


**For more information, please visit**: [https://open-verify.cc/UnityChipForXiangShan](https://open-verify.cc/UnityChipForXiangShan/docs/)


#### UnityChip QQ Group:

<image src="/.github/image/600480230.jpg" alt="600480230" width=300px />
