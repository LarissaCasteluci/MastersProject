# Kubric Dataset Generation

Original Paper: 
Github: https://github.com/google-research/kubric

The Dataset Generation was made by using the Kubric.

Command for using kubric in this path, from the root of the project:

docker run --rm --interactive \
           --user $(id -u):$(id -g) \
           --volume "$(pwd)/original_repos/kubric:/kubric" \
           --volume "$(pwd)/1DatasetGeneration:/1DatasetGeneration" \
           kubricdockerhub/kubruntu \
           /usr/bin/python3 /1DatasetGeneration/helloworld.py