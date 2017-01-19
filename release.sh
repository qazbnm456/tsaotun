#! /bin/bash
#
# Create the official release
#

VERSION=$1
REPO=qazbnm456/tsaotun
GITHUB_REPO=git@github.com:$REPO

if [ -z $VERSION ]; then
    echo "Usage: $0 VERSION [upload]"
    exit 1
fi

echo "##> Tagging the release as $VERSION"
git tag $VERSION || exit 1
if  [[ $2 == 'upload' ]]; then
    echo "##> Pushing tag to github"
    git push $GITHUB_REPO $VERSION || exit 1
    echo "##> Uploading sdist to pypi"
    python setup.py sdist bdist_wheel upload
fi
