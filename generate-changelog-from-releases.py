#!/usr/bin/env python3

"""
Generate CHANGELOG from GitHub releases

To generate a token: 
https://github.com/settings/tokens/new?description=Generate%20Changelog%20From%20Releases
"""

import os
import re
import sys
import github
import argparse
import subprocess

parser = argparse.ArgumentParser(description="Generate a CHANGELOG.md from GitHub releases")
parser.add_argument("--token", "-t", type=str, help="GitHub token", default=os.getenv("GENERATE_CHANGELOG_FROM_RELEASES_TOKEN"))
parser.add_argument("--output-file", "-o", type=str, help="Output path. For stdout, use -o -", default="CHANGELOG.md")
parser.add_argument("--force", "-f", action="store_true", help="Force overwriting file")
args = parser.parse_args()

try:
    #---------------------------------------------------------------------------
    # Parse output of git to obtain the repo path corresponding to the
    # current directory.
    #---------------------------------------------------------------------------
    origin = subprocess.check_output([ "git", "remote", "get-url", "origin" ])
    origin = origin.strip().decode("utf8")
    prefix, repo_name = origin.split(":")
    if not prefix.endswith("github.com"):
        raise Exception("Origin isn't a GitHub URL")
    repo_name = re.sub(".git$", "", repo_name)
except subprocess.CalledProcessError:
    #---------------------------------------------------------------------------
    # Current directory doesn't appear to be a git repo. Bail.
    #---------------------------------------------------------------------------
    sys.exit(1)

gh = github.Github(args.token)

#---------------------------------------------------------------------------
# Extract releases from current repo.
# Releases must be explicitly sorted by the tag's created-at date, which
# may differ from when the GH release was published.
#---------------------------------------------------------------------------
repo = gh.get_repo(repo_name)
releases = list(repo.get_releases())
releases = sorted(releases, key=lambda release: release.created_at, reverse=True)

if len(releases) == 0:
    raise Exception("No releases found")

#---------------------------------------------------------------------------
# Output markdown.
#---------------------------------------------------------------------------
if args.output_file == "-":
    output_fd = sys.stdout
else:
    if os.path.exists(args.output_file) and not args.force:
        print("Output file %s exists. Overwrite? [y/N] " % args.output_file, end="")
        confirmation = input()
        if not re.match("^[yY]$", confirmation):
            sys.exit(1)
    output_fd = open(args.output_file, "w")

output_fd.write("# Changelog\n\n")

for release in releases:
    output_fd.write("## [%s](%s) (%s)\n\n" % (release.title, release.html_url, release.created_at.strftime("%Y-%m-%d")))
    output_fd.write("%s\n\n" % release.body)

output_fd.close()
