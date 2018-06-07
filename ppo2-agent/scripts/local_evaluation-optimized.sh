export DOCKER_REGISTRY="retrocontestdsvwzyrakbiqhnom.azurecr.io"
docker login $DOCKER_REGISTRY \
  --username "retrocontestdsvwzyrakbiqhnom" \
  --password "n=IiSctm9l7Witb+EUlMW6sf6WbwNVGD"

docker build -f  ppo2-cpu-optimized.docker -t $DOCKER_REGISTRY/ppo2-agent-cpu:v1 .&&

docker push $DOCKER_REGISTRY/ppo2-agent-cpu:v1 &&

retro-contest run --agent $DOCKER_REGISTRY/ppo2-agent-cpu:v1 \
    --results-dir results --no-nv  --use-host-data\
    SonicTheHedgehog-Genesis GreenHillZone.Act1
