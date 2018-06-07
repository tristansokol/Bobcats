# https://contest.openai.com/details

export DOCKER_REGISTRY="retrocontestdsvwzyrakbiqhnom.azurecr.io"
docker login $DOCKER_REGISTRY \
  --username "retrocontestdsvwzyrakbiqhnom" \
  --password "n=IiSctm9l7Witb+EUlMW6sf6WbwNVGD"

docker build -f jerk-agent.docker -t $DOCKER_REGISTRY/jerk-agent:v4 .

docker push $DOCKER_REGISTRY/jerk-agent:v4


echo "jerk-agent:v4"
open https://contest.openai.com/user/job/submit
