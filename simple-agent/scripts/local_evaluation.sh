export DOCKER_REGISTRY="retrocontestdsvwzyrakbiqhnom.azurecr.io"
docker login $DOCKER_REGISTRY \
    --username "retrocontestdsvwzyrakbiqhnom" \
    --password "nXrOZH1kYlk5loFEAVvZE/14zpeRs9kP"

retro-contest run --agent $DOCKER_REGISTRY/simple-agent:v1 \
    --results-dir results --no-nv Airstriker-Genesis Level1
