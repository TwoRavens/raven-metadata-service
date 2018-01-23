
## General workflow


### A. Create an issue for the work to be done

- Or use an existing issue.
- Note the issue number.
  - e.g, Issue `#5`

### B. Create a new branch from master

- Name the new branch starting with the issue number
  - e.g. `5_islogical`

### C. Switch your dev machine to the new branch

- e.g. `git checkout 5_islogical`

### D. Merge as master is updated

1. Check in your changes on dev branch, `5_islogical`
1. Checkout the master branch
1. Pull changes from master
1. Checkout the dev branch
1. Merge and fix any conflicts

```
git push # dev branch
git checkout master
git pull
git checkout [dev branch]
git branch # make sure you're on the right branch
git merge origin # fix conflicts if needed
```

### E. All done with work

1. Merge with master, if needed (repeat step D)
1. Check that you've written/updated any needed tests
1. Make a pull request
1. Have someone review the pull request
1. Merge pull request!
