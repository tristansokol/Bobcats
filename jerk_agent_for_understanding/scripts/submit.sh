# https://contest.openai.com/details

export TAG_NAME=$1

export DOCKER_REGISTRY="retrocontestdsvwzyrakbiqhnom.azurecr.io"
docker login $DOCKER_REGISTRY \
  --username "retrocontestdsvwzyrakbiqhnom" \
  --password "n=IiSctm9l7Witb+EUlMW6sf6WbwNVGD" &&

docker build -f jerk-agent.docker -t $DOCKER_REGISTRY/$TAG_NAME . &&

docker push $DOCKER_REGISTRY/$TAG_NAME &&

retro-contest job submit -t '$TAG_NAME'
echo $TAG_NAME
