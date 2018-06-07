# https://contest.openai.com/details

export DOCKER_REGISTRY="retrocontestdsvwzyrakbiqhnom.azurecr.io"
docker login $DOCKER_REGISTRY \
  --username "retrocontestdsvwzyrakbiqhnom" \
  --password "nXrOZH1kYlk5loFEAVvZE/14zpeRs9kP"

docker build -f simple-agent.docker -t $DOCKER_REGISTRY/simple-agent:v1 .

docker push $DOCKER_REGISTRY/simple-agent:v1


echo "simple-agent:v1"
open https://contest.openai.com/user/job/submit
