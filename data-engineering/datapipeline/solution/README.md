# Solution README

- [Solution README](#solution-readme)
  - [Solution overview and discussion](#solution-overview-and-discussion)
  - [Setup and running](#setup-and-running)
    - [venv/pip](#venvpip)
    - [uv](#uv)
  - [Cloud providers](#cloud-providers)
  - [Use of AI](#use-of-ai)

## Solution overview and discussion

I have undertaken the stretch goals:

- Unit tests, and an end-to-end test, are included under `solution/tests/`. These are done with pytest
- A short discussion about cloud providers (at the end of this readme)

The gist of the solution is:

- Read in the source data
- Convert missing race times to midnight
- Create the race `datetime` column from `date` and `time`
- Aggregate the results so that for each race we know the winner and fastest lap time
- Combine the aggregated results with the race information
- For each year, filter the combined data, format to match the example in the README, and write the JSON

The JSON is not pretty-indented because Polars doesn't have an option for that. If you want to spot check any of them by eye you can do e.g. `python3 -m json.tool results/stats_2018.json`.

I've attempted to keep functions short and they are all unit tested for the happy path at minimum.

Functions have been organised into:

- `pipeline.py`: these form the majority of the data handling logic
- `logging_config.py`: a single function for setting up the logging
- `schemas.py`: data input and output schemas
- `main.py`: the orchestrator, just has `main()`

There are behaviours I'd like to have put into the pipeline but decided not to. I was told
the task should only take a few hours and I already overshot that a bit (I wanted to impress!). The behaviours would be things like: more assertions about the data (e.g. are all race IDs unique?), schema
enforcement (using `pandera` or similar), and consideration of idempotency/append-only
paths.

Aside from time, I also think there's crucial missing context that could mean implementing those listed behaviours would be over-engineering. For example, the data is incredibly small
(and likely always will be), and infrequently updated, so in terms of keeping a codebase lean and readable re-processing the whole dataset every time there's a new race might be fine. But if there are plans to incorporate more datasets, similar to the results ones, then batch processing and keeping a tracking index of previously-processed data could be the better call despite adding more logic to the program.

Ultimately I thought these would be fun points to discuss during the interview, so I won't say more here!

## Setup and running

To run my solution you can use `uv` or plain Python. Instructions for both are provided below.

> [!IMPORTANT]
> Both options require setting your working directory (or workspace) to `optima-data-eng-submission/data-engineering/datapipeline`.

You should end up with a `.venv` directory with polars and pytest installed.

`main.py` should run and populate `results/` with the JSON outputs, and logs will appear under `results/logs/`. Tests should all pass.

### venv/pip

Installation:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install polars pytest
```

Run the pipeline:

```shell
python solution/main.py
```

Run the tests:

```shell
pytest
```

### uv

If you don't have `uv` installed already see [installation methods](https://docs.astral.sh/uv/getting-started/installation/).

Set up venv and dependencies:

```shell
uv sync
```

Run the pipeline:

```shell
uv run solution/main.py
```

Run the tests:

```shell
uv run pytest
```

## Cloud providers

I have some familiarity with AWS but haven't had much chance to use it in the past two years of work (being mostly confined to an air-gapped Trusted Research Environment), so forgive me if things have moved on or I'm missing obvious services or considerations.

- My instinct is that the code would be well suited to a Lambda. It would run at most twice a month (given race frequency) and the process time is measured in seconds, so a transient, on-demand service would be a good fit. My experience is mostly with container-based Lambdas but I think that was starting to change a couple of years ago with containerless Python Lambdas becoming available, and if I had to pick now I'd probably go with the latter - the project is simple so "works on my machine" problems would (hopefully!) not be an issue and make a Containerfile irrelevant.
- It would need some CI/CD. Probably GitHub Actions to at least run pytest on push.
- I'd need to know about data storage and validation
  - Presumably some sort of Lambda would run to hit an API or scrape data in the first instance. I'd expect that to land in S3, a lakehouse, or a plain Aurora database like a Postgres instance
  - Where it gets stored and what kind of validation is done to it would dictate how this codebase would need to change in response. I have a strong preference that data is ingested and kept raw, then checked for integrity (schema validation, constraints).
  - At the moment the results are just local JSON. But this would need to feed something else, meaning it must be stored accessibly. As it is JSON I'm guessing it would go to S3? Or are there specialised services that store JSON for lightning fast app access?
- I'd need to know if the client was using Infrastructure as Code or doing ClickOps. With IaC there's a lot more self-documentation given the declarative nature of the configuration, but if it's ClickOps then clients really need to be left with more documentation and a runbook. I've used AWS CDK (TypeScript version), but understand people might prefer Terraform if they've got multiple providers or want the flexibility to move in the future.

## Use of AI

I used Claude as more-or-less an advanced search engine for most of this task.

The one place I allowed it to generate code was for the tests, because they are quite straightforward and tedious to write in this instance. **I checked everything that it wrote**, and indeed deleted and modified several of the tests.

It's really important to me that I'm in control of the code and the decisions being made, because at the end of the day it is my responsibility. I need to be able to explain all the decisions and how the code works.
