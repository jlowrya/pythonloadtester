 #!/bin/bash

docker build --no-cache . -t loadtester
docker run --rm --name load-test --network host -it loadtester:latest