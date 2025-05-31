from transnetv2 import TransNetV2

# location of learned weights is automatically inferred
# add argument model_dir="/path/to/transnetv2-weights/" to TransNetV2() if it fails
model = TransNetV2()
video_frames, single_frame_predictions, all_frame_predictions = \
    model.predict_video("./videos/00001.mp4")

print(single_frame_predictions, all_frame_predictions)