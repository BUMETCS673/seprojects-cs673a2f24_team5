# CVCoach

[![CI for FE](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/actions/workflows/ci_fe.yml/badge.svg)](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/actions/workflows/ci_fe.yml)
[![CD Pipeline](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/actions/workflows/cd.yml/badge.svg)](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/actions/workflows/cd.yml)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

<p>
  <!-- <img src="https://img.shields.io/github/license/BUMETCS673/seprojects-cs673a2f24_team5" alt="license"/> -->
  <img src="https://img.shields.io/docker/pulls/adamma1024/cvcoach_web" alt="docker-pull-count" />
  <a href="https://img.shields.io/badge/price-free-ff69b4"><img alt="Price" src="https://img.shields.io/badge/price-free-ff69b4?style=flat-square" /></a>
</p>

This repository is a project for METCS673. This project focuses on using AI to automate and improve the process of resume evaluation and interview preparation. By incorporating Retrieval-Augmented Generation (RAG), we ensure that our application can provide more accurate, context-relevant reviews.

## CHANGELOG

[📖 CHANGELOG.md](./CHANGELOG.md)

## How to start it with Docker?

> Learn the [Docker](https://www.docker.com/) commands here.

```bash
cd /rootPath
docker compose up --build -d # Make sure you've installed the Docker locally.
```

Then, open your browser with **<https://localhost:8081>** (The default port is 8081)  
The `-d` is detached session mode, you can check your docker container with command:  

```bash
docker ps
docker stop/kill <container_id> # And stop your service with container id
# Or docker compose down/stop directly
docker compose down/stop
```

## Design Docs

[📖 Design Docs](./doc/designs.md)  
[📖 SDD](https://docs.google.com/document/d/1EPiaG6P9PN608ExKb6kGQkfQGTZQFpuxr1Ox6fWw7uM/edit?usp=sharing)  

## How to contribute this project?

> Tips: Make sure there is no repeated issues or PRs before opening a new one.

[🎤 Commit an issue](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/issues/new/choose)  

[⌨️ Raise a PR](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/pulls)  

[📖 Development manual](./doc/development_manual.md)  

## What's the CI/CD processes of this project?

[📔 CI/CD Intro](./doc/CICD.md)

## Task Management

As per github's task tracking flow is difficult to use, we decide to use [JIRA](https://bu-cs673a2f24-team-5.atlassian.net/jira/software/projects/SCRUM/boards/1) to trace the progress and manage the risk.
