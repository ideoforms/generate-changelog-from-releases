# Generate CHANGELOG.md from GitHub releases

## Installation

```
pip3 install generate-changelog-from-releases
```

## Usage

To generate a changelog and write to `CHANGELOG.md`:

- `cd your-repo-path`
- `generate-changelog-from-releases.py`

The script automatically infers the GitHub project from the git repository's config, and parses the project's releases accordingly.

For occasional use, no GitHub token is required.

If you will be generating changelogs frequently, you should [generate a GitHub token](https://github.com/settings/tokens/new?description=Generate%20Changelog%20From%20Releases),  and pass it to the script with the `-t` flag or in the `GENERATE_CHANGELOG_FROM_RELEASES_TOKEN` environmental variable.
