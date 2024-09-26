# Development

## Git Branches

We have three dev branches: `dev/infra`, `dev/frontend`, `dev/backend`. The best working flow is like:

```bash
git clone https://github.com/BUMETCS673/seprojects-cs673a2f24_team5.git
cd seprojects-cs673a2f24_team5/
git switch dev/** # Based on the content of your PR
# do some change
git add fileA fileB # Replace the fileA,B to your changed files
git commit -m "feat: xxx" # Please follow the semver rules, so that we can have a gentle CHANGELOG.md then.
git push
```

Then, visit the Github [PR page](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/pulls) to commit your PR.

The configuration manager(@adamma1024) will check out a release branch on the last Sunday before the iteration, so generally, you don't need to be aware of it.

## Working flows

### Frontend

Reach out to the Adam(@adamma1024) if you have any questions.

#### Install dependencise

```bash
cd ./fe_repo
pnpm i
```

#### Debug

```bash
pnpm dev # Then open the url it shows. Generally, it's http://localhost:5173/ if you don't change the default Vite configuration.
```

### Backend

@Stanford997 @andyasdd1

### Branch Rulesets

Every PR checking in `Main` branch needs at least one reviewer. The other rules are on [Git ruleset of Main](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/settings/rules/1954560)  
Every PR checking in `Release` branch needs at least two reviewers. The other rules are on [Git ruleset of Release](https://github.com/BUMETCS673/seprojects-cs673a2f24_team5/settings/rules/1954560)