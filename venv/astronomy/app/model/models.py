from pydantic import BaseModel, Field
from typing import List, Dict, Optional


# 请求体_坐标
class Coordinate(BaseModel):
    ra:float
    dec:float
    fov:float
    size:int
    surveyid:str


# 定义响应模型
class PredictOut(BaseModel):
    category: str
    confidence: str
    description: str
    represent: Dict[str, str]
    image: str


dataset_labels = [
    "Disturbed",
    "Merging",
    "Round Smooth",
    "In-between Round Smooth",
    "Cigar Shaped Smooth",
    "Barred Spiral",
    "Unbarred Tight Spiral",
    "Unbarred Loose Spiral",
    "Edge-on without Bulge",
    "Edge-on with Bulge"
]
'''
    Disturbed - 扰乱型
    Merging - 合并型
    Round Smooth - 圆滑型
    In-between Round Smooth - 中间圆滑型
    Cigar Shaped Smooth - 雪茄形滑型
    Barred Spiral - 条纹螺旋型
    Unbarred Tight Spiral - 无条纹紧密螺旋型
    Unbarred Loose Spiral - 无条纹松散螺旋型
    Edge-on without Bulge - 无突起的边缘型
    Edge-on with Bulge - 有突起的边缘型
'''