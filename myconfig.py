_base_ = ['configs/_base_/default_runtime.py']

# model settings
num_classes = 4
clip_size = 32

model = dict(
    type='Recognizer2D',
    backbone=dict(
        type='ResNetTSM',
        pretrained='FER_ResNet50.pt',
        depth=50,
        out_indices=(2, 3),
        norm_eval=False,
        shift_div=8,
        frozen_stages = 4),
    neck=dict(
        type='TPN',
        in_channels=(1024, 2048),
        out_channels=1024,
        spatial_modulation_cfg=dict(
            in_channels=(1024, 2048), out_channels=2048),
        temporal_modulation_cfg=dict(downsample_scales=(clip_size, clip_size)),
        upsample_cfg=dict(scale_factor=(1, 1, 1)),
        downsample_cfg=dict(downsample_scale=(1, 1, 1)),
        level_fusion_cfg=dict(
            in_channels=(1024, 1024),
            mid_channels=(1024, 1024),
            out_channels=2048,
            downsample_scales=((1, 1, 1), (1, 1, 1))),
        aux_head_cfg=dict(out_channels=num_classes, loss_weight=0.5)),
    cls_head=dict(
        type='TPNHead',
        num_classes=num_classes,
        in_channels=2048,
        spatial_type='avg',
        consensus=dict(type='AvgConsensus', dim=1),
        dropout_ratio=0.5,
        init_std=0.01),
    # model training and testing settings
    train_cfg=None,
    test_cfg=dict(average_clips='prob', fcn_test=True),
)


base_data_root = "/rds/user/yl847/hpc-work/outlast/"

# base_data_root = "D:\\working-age-data\\videos"

# dataset settings
dataset_type = 'VideoDataset'
data_root = data_root_val = base_data_root
ann_file_train = './train_annotation.txt'
ann_file_val = './val_annotation.txt'
# ann_file_test = 'data/sthv1/sthv1_val_list_rawframes.txt'
img_norm_cfg = dict(
    mean=[86.067436, 92.065525, 121.146114], std=[54.645994, 53.534381, 58.450872], to_bgr=False)
train_pipeline = [
    dict(type="DecordInit"),
    dict(type='SampleFrames', clip_len=1, frame_interval=1, num_clips=clip_size),
    dict(type='DecordDecode'),
    dict(type='RandomResizedCrop'),
    dict(type='Resize', scale=(224, 224), keep_ratio=False),
    dict(type='Flip', flip_ratio=0.5),
    dict(type='ColorJitter'),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs', 'label'])
]
val_pipeline = [
    dict(type="DecordInit"),
    dict(
        type='SampleFrames',
        clip_len=1,
        frame_interval=1,
        num_clips=8,
        test_mode=True),
    dict(type='DecordDecode'),
    dict(type='Resize', scale=(-1, 256)),
    dict(type='CenterCrop', crop_size=224),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs'])
]
data = dict(
    videos_per_gpu=1,
    workers_per_gpu=1,
    test_dataloader=dict(videos_per_gpu=1),
    train=dict(
        type=dataset_type,
        ann_file=ann_file_train,
        data_prefix=data_root,
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file=ann_file_val,
        data_prefix=data_root_val,
        pipeline=val_pipeline),

)
evaluation = dict(
    interval=5, metrics=['top_k_accuracy', 'mean_class_accuracy'])

# optimizer
optimizer = dict(type = 'Adam', lr = 0.002, betas = (0.9, 0.999), weight_decay = 0.0001)
optimizer_config = dict(grad_clip=dict(max_norm=20, norm_type=2))
# learning policy
lr_config = dict(policy='step', step=[140])
total_epochs = 150

batch_size = 128

workflow = [("train", 1), ("val", 1)]

# runtime settings
work_dir = './work_dirs/tpn_tsm_r50_1x1x8_150e_kinetics400_rgb'
