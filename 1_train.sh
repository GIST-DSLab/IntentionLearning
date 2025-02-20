#!/bin/sh

TASK_NAME=$1
MODEL_NAME=$2
GPU_ID=$3

if [ -z "$TASK_NAME" ]; then
    TASK_NAME=dflip
fi

if [ -z "$MODEL_NAME" ]; then
    MODEL_NAME=default
fi

if [ -z "$GPU_ID" ]; then
    GPU_ID=0
fi

if [ -n "$GPU_ID" ]; then
    export CUDA_VISIBLE_DEVICES=$GPU_ID
fi

case "$TASK_NAME" in
    dflip)
        INTENTION_SIZE=8
        ;;
    stretch)
        INTENTION_SIZE=10
        ;;
esac

echo "Using task: $TASK_NAME"
echo "Using model: $MODEL_NAME"
echo "Using GPU: $GPU_ID"
echo "Intention size set to: $INTENTION_SIZE"

echo "Add Python PATH $(pwd)"
export PYTHONPATH=$(pwd)

echo "Start Training Task:$TASK_NAME with Model:$MODEL_NAME on GPU:$GPU_ID"
python src/train.py \
    --seed 123 \
    --context_length 6 \
    --epochs 400 \
    --learning_rate 5e-4 \
    --batch_size 192 \
    --max_timestep 200 \
    --data_dir_prefix "./dataset/${TASK_NAME}/" \
    --train_data_folder "train" \
    --ckpt_path "./model/${TASK_NAME}/" \
    --save_cycle 1 \
    --n_embd 256 \
    --n_layer 16 \
    --n_head 8  \
    --grid_x 5 \
    --grid_y 5 \
    --intention_size $INTENTION_SIZE \
    --task_name "$TASK_NAME" \
    --model_name "$MODEL_NAME" \
    --gpu_id $GPU_ID

echo "Finish Training Task:$TASK_NAME with Model:$MODEL_NAME on GPU:$GPU_ID"

echo "Copy Checkpoint Model to Final Model"
cp ./model/${TASK_NAME}/${TASK_NAME}_${MODEL_NAME}.pt ./model/${TASK_NAME}_${MODEL_NAME}.pt

./2_test.sh $TASK_NAME $MODEL_NAME 0 $GPU_ID

export CUDA_VISIBLE_DEVICES=0
