export TAG_NAME=$1
export DOCKER_REGISTRY="retrocontestdsvwzyrakbiqhnom.azurecr.io"

git add jerk_agent.py
git commit -m "running $TAG_NAME locally"

mkdir results/${TAG_NAME//:}

cp jerk_agent.py results/${TAG_NAME//:}/jerk_agent.py

# pip3 install -e "retro-contest/support[docker,rest]"

docker login $DOCKER_REGISTRY \
  --username "retrocontestdsvwzyrakbiqhnom" \
  --password "n=IiSctm9l7Witb+EUlMW6sf6WbwNVGD"&&

docker build -f  jerk-agent.docker -t $DOCKER_REGISTRY/$TAG_NAME . &&

retro-contest run --agent $DOCKER_REGISTRY/$TAG_NAME \
    --results-dir results/${TAG_NAME//:} --no-nv --use-host-data --timestep-limit 1000000\
    SonicTheHedgehog-Genesis GreenHillZone.Act1
