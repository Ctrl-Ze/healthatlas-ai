<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Ctrl-Ze/healthatlas-ai">
  <!-- TODO make a logo -->
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">healthatlas-ai (Chiron)</h3>

  <p align="center">
    AI-powered blood test analysis platform with LLM-assisted insights.
    <br />
    <a href="https://github.com/Ctrl-Ze/healthatlas-ai"><strong>Explore the docs »</strong></a>
    <!-- TODO add here View Demo, Report Bug, Request Feature -->
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#usage">Testing and Code Coverage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

**Codename**: Chiron — *the advisor of the HealthAtlas*.

Chiron is an AI-assisted health platform that provides:
* AI-powered lifestyle suggestions based on lab results using OpenAI
* Easy-to-use FastAPI backend with OpenAPI docs


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python-shield]][Python-url]
* [![Fast][FastAPI-shield]][FastAPI-url]
* [![OpenAI][OpenAI-shield]][OpenAI-url]
* [![Pydantic][Pydantic-shield]][Pydantic-url]
* [![Uvicorn][Uvicorn-shield]][Uvicorn-url]
* [![pytest][Pytest-shield]][Pytest-url]
* [![coverage][Coverage-shield]][Coverage-url]
* [![python-dotenv][Dotenv-shield]][Dotenv-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Follow these steps to get the project running locally.

### Prerequisites

* Python 3.9+
* Git
* OpenAI API key (for AI features)

### Installation

1. Get a OpenAI API Key at [OpenAI](https://platform.openai.com)
2. Clone the repo
   ```bach
   git clone https://github.com/Ctrl-Ze/healthatlas-ai.git
   ```
   ```bash
   cd healthatlas-ai
   ```
3. Install dependencies:
    ```bach
   pip install -r requirements.txt
   ```
    ```bach
   pip install pytest coverage
   ```
4. Set up environment variables in .env:
    ```
    OPENAI_API_KEY="sk-..."
    OPENAI_MODEL="gpt-4o-mini"
    PORT="8000"
    ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

Start the FastAPI server:
```
uvicorn chiron.app:app --reload --host 0.0.0.0 --port 8000
```

Access the interactive API docs:

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Testing and Code Coverage

We use pytest for testing and coverage.py for code coverage visualization.

### Run Tests
```bash
coverage run -m pytest
```

### Generate Reports
```bash
coverage report
```

```bash
coverage xml
```

```bash
coverage html
```
Open HTML report 
```bash
open htmlcov/index.html
```

### View Coverage in VS Code

1. Install Coverage Gutters extension.
2. Open Command Palette → Coverage Gutters: Display Coverage.
3. Covered lines: 
    * Green: Code line was executed (covered).
    * Red: Code line was missed (not covered).
    * Yellow: Code line was partially covered (e.g., one branch of an if/else was missed).

### Coverage Threshold

The .coveragerc is configured to enforce a minimum of 85% coverage. Adjust as needed in .coveragerc

<!-- ROADMAP -->
## Roadmap

- [x]
- [ ]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/Ctrl-Ze/healthatlas-ai?style=for-the-badge
[contributors-url]: https://github.com/Ctrl-Ze/healthatlas-ai/graphs/contributors

[Python-shield]: https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff
[Python-url]: https://www.python.org/

[FastAPI-shield]: https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/

[OpenAI-shield]: https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white
[OpenAI-url]: https://openai.com/

[Pydantic-shield]: https://img.shields.io/badge/Pydantic-E92063?logo=Pydantic&logoColor=white
[Pydantic-url]: https://docs.pydantic.dev/

[Uvicorn-shield]: https://img.shields.io/badge/Uvicorn-4EC9B0?logo=python&logoColor=white
[Uvicorn-url]: https://www.uvicorn.org/

[Pytest-shield]: https://img.shields.io/badge/Pytest-fff?logo=pytest&logoColor=000
[Pytest-url]: https://docs.pytest.org/

[Coverage-shield]: https://img.shields.io/badge/Coverage-1B9A5B?logo=coverage&logoColor=white
[Coverage-url]: https://coverage.readthedocs.io/

[Dotenv-shield]: https://img.shields.io/badge/python--dotenv-2F4633?logo=python&logoColor=white
[Dotenv-url]: https://pypi.org/project/python-dotenv/