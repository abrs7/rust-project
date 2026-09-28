#!/bin/sh
set -eu

task=/home/abraham/workspace/rustlabs/tasks/telemetry-frame-recovery/source
attack=/home/abraham/workspace/rustlabs/tasks/telemetry-frame-recovery/tooling/attacks/attack_solve.py
logs=/home/abraham/workspace/rustlabs/tasks/telemetry-frame-recovery/runs/attacks

for mode in lazy naive reward exit constant; do
    scratch="/tmp/thanos-attack-$mode"
    rm -rf "$scratch"
    mkdir -p "$scratch"
    cp -a "$task" "$scratch/telemetry-frame-recovery"
    cp "$attack" "$scratch/telemetry-frame-recovery/solution/solve.py"
    if [ "$mode" = constant ]; then
        mkdir -p "$scratch/telemetry-frame-recovery/solution/visible"
        cp "$task"/tests/expected/visible/* \
            "$scratch/telemetry-frame-recovery/solution/visible/"
    fi
    cat > "$scratch/telemetry-frame-recovery/solution/solve.sh" <<EOF
#!/bin/sh
set -eu
ATTACK_MODE=$mode exec python /solution/solve.py
EOF
    chmod +x "$scratch/telemetry-frame-recovery/solution/solve.sh"
    (
        cd "$scratch"
        harbor run --path "$scratch/telemetry-frame-recovery" --agent oracle
    ) > "$logs/$mode.log" 2>&1
done
