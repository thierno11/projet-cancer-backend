from fastapi import APIRouter, UploadFile, File
import services.imagerie_service as im

analyse_router = APIRouter(prefix="/analyse",tags=["Analyse"])

@analyse_router.post("/")
async def effectuer_analyse(image: UploadFile = File(...)):

    return await im.effectuer_analyse(image)





# #Test
# img_with_boxes, mask_bin, num_det = predict_and_draw_boxes(
#     'dataset_mammo/b3/2018_BC0021822_ MLO_R.jpg',
#     model,
#     device,
#     threshold=0.99,
#     min_area=70
# )