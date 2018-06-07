# https://contest.openai.com/details

export TAG_NAME='ppo2-agent:v7'

export DOCKER_REGISTRY="retrocontestdsvwzyrakbiqhnom.azurecr.io"
docker login $DOCKER_REGISTRY \
  --username "retrocontestdsvwzyrakbiqhnom" \
  --password "n=IiSctm9l7Witb+EUlMW6sf6WbwNVGD" &&

docker build -f ppo2-gpu.docker -t $DOCKER_REGISTRY/$TAG_NAME . &&

docker push $DOCKER_REGISTRY/$TAG_NAME &&

retro-contest job submit -t $TAG_NAME

# echo "ppo2-agent:v1"
# open https://contest.openai.com/user/job/submit
