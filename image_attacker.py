import torch
from surrogates import (
    BlipFeatureExtractor,
    ClipFeatureExtractor,
    EnsembleFeatureLoss,
    VisionTransformerFeatureExtractor,
)
from utils import get_list_image, save_list_images
from tqdm import tqdm
from attacks import SSA_CommonWeakness
from attacks import MI_CommonWeakness
from torchvision import transforms
import os

images, image_names = get_list_image("./dataset/test_files")
resizer = transforms.Resize((224, 224))
images = [resizer(i).unsqueeze(0) for i in images]

blip = BlipFeatureExtractor().eval().cuda().requires_grad_(False)
clip = ClipFeatureExtractor().eval().cuda().requires_grad_(False)
vit = VisionTransformerFeatureExtractor().eval().cuda().requires_grad_(False)
models = [vit, blip, clip]


def ssa_cw_count_to_index(count, num_models=len(models), ssa_N=20):
    max = ssa_N * num_models
    count = count % max
    count = count // ssa_N
    return count


ssa_cw_loss = EnsembleFeatureLoss(models, ssa_cw_count_to_index, feature_loss=torch.nn.MSELoss())


attacker = SSA_CommonWeakness(
    models,
    epsilon=16 / 255,
    step_size=1 / 255,
    total_step=5,
    criterion=ssa_cw_loss,
)

# attacker = MI_CommonWeakness(
#     models,
#     epsilon=16 / 255,
#     step_size=1 / 255,
#     total_step=500,
#     criterion=ssa_cw_loss,
# )

dir = "./perturbed_images/"
if not os.path.exists(dir):
    os.mkdir(dir)
for i, x in enumerate(tqdm(images)):
    x = x.cuda()
    ssa_cw_loss.set_ground_truth(x)
    adv_x = attacker(x, None)
    save_list_images(adv_x, dir, begin_id=i, names=image_names)
