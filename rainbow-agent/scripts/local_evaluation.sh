export DOCKER_REGISTRY="retrocontestdsvwzyrakbiqhnom.azurecr.io"
docker login $DOCKER_REGISTRY \
  --username "retrocontestdsvwzyrakbiqhnom" \
  --password "n=IiSctm9l7Witb+EUlMW6sf6WbwNVGD"

docker build -f  rainbow-agent-cpu.docker -t $DOCKER_REGISTRY/rainbow-agent:v3 .&&

docker push $DOCKER_REGISTRY/rainbow-agent:v3 &&

retro-contest run --agent $DOCKER_REGISTRY/rainbow-agent:v3 \
    --results-dir results --no-nv  --use-host-data\
    SonicTheHedgehog-Genesis GreenHillZone.Act1
