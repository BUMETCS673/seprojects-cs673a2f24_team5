# Development

## Git Branches

We have three dev branches: `dev/infra`, `dev/frontend`, `dev/backend`. The best working flow is like:

```bash
git clone https://github.com/BUMETCS673/seprojects-cs673a2f24_team5.git
cd seprojects-cs673a2f24_team5/
git switch dev/** # Based on the content of your PR
# do some change
git add fileA fileB # Replace the fileA,B to your changed files
git commit # Please follow the Conventional Commit rules, so that we can have a gentle CHANGELOG.md then.
git push
```

### Conventional Commit (For a gentle CHANGELOG file)

> ⚠️ An interactive terminal is needed.  

Our project is using the [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) to restrict the git commit message. Please learn more details on its official site.  

![git_commit_plugin](../images/git_commit_plugin.png)
![git_commit](../images/git_commit.png)

Then, visit the Github [PR page](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/pulls) to commit your PR.

The configuration manager(@adamma1024) will check out a release branch on the last Sunday before the iteration, so generally, you don't need to be aware of it.

## Working flows

### General

1. Install Node and pnpm

```bash
npm i -g pnpm
```

2. Install dependencise in the Root Path of project

```bash
pnpm i
```

3. Try the Git Commit in an interactive terminal

```bash
git commit # If it doesn't trigger the git commit plugin, please contact the @adamma1024
```

### Frontend

Reach out to the Adam(@adamma1024) if you have any questions.

#### Install dependencise

```bash
cd ./fe_repo
pnpm i
```

#### Build & start

```bash
pnpm dev # Then open the url it shows. Generally, it's http://localhost:5173/ if you don't change the default Vite configuration.
```

### Backend

@Stanford997 @andyasdd1

### Branch Rulesets

Every PR checking in `Main` branch needs at least one reviewer. The other rules are on [Git ruleset of Main](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/settings/rules/1954560)  
Every PR checking in `Release` branch needs at least two reviewers. The other rules are on [Git ruleset of Release](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/settings/rules/1954560)
