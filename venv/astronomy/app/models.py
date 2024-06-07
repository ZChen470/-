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
    description: bytes
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
disciptions: Dict[str, str] = {
    "Disturbed":"The adjective ‘disturbed’ refers to the physical (rather than mental) state of a galaxy. Disturbed galaxies have a morphology that has been altered by an interaction with another galaxy. Disturbances can take many forms including; warps, tidal tails and asymmetries.\nThe importance of interactions between galaxies has only recently been realised. In particular, disturbances to galaxies provide astronomers with a means to investigate both ongoing and recently completed interactions, and can also be used to probe the dynamics of the galaxies involved.",
    "Merging":"Astronomers see galaxy interaction and merging throughout the universe. In particular, large galaxies formed by merging with smaller galaxies over billions of years. The largest galaxies in the cosmos, the giant ellipticals, almost certainly got that way by mergers. Irregular galaxies, including our neighbors Large and Small Magellanic Clouds, probably got their distorted shapes through gravitational interactions with other galaxies. Since ellipticals make up about 15% of known galaxies and irregulars are an additional 5%, mergers and interactions play an obvious role in the types of galaxies we see.",
    "Round Smooth":"Elliptical galaxies are round collections of old stars. They contain very little gas and dust and have no features within them. They come in a range of different sizes and shapes. They can look circular, oval or even rugby-ball shaped.Ellipticals are classified by how squashed they look. Circular balls are called E0. The more squashed one looks, the higher the number it is given. The most flattened ellipticals are classed as E7.",
    "In-between Round Smooth":"Elliptical galaxies are round collections of old stars. They contain very little gas and dust and have no features within them. They come in a range of different sizes and shapes. They can look circular, oval or even rugby-ball shaped.Ellipticals are classified by how squashed they look.The most flattened ellipticals are classed as E7.These galaxies are somewhat elliptical and have a bulge-like feature visible at their centers.",
    "Cigar Shaped Smooth":"Lenticular galaxies are disc galaxies that have used up or lost most of their interstellar matter and therefore have very little ongoing star formation. They may, however, retain significant dust in their disks. As a result, they consist mainly of aging stars (like elliptical galaxies). Despite the morphological differences, lenticular and elliptical galaxies share common properties like spectral features and scaling relations. Both can be considered early-type galaxies that are passively evolving, at least in the local part of the Universe. Connecting the E galaxies with the S0 galaxies are the ES galaxies with intermediate-scale discs",
    "Barred Spiral":"A barred spiral galaxy is a spiral galaxy with a central bar-shaped structure made of stars.Bars are found in up to 65% of spiral galaxies. They affect the motions of stars, dust and gas. It is believed that bars act a bit like a funnel, pulling matter into the bulge from the disk. This leads to stars forming in bursts within the centre. The further back we go the fewer barred spirals we see. This might suggest that the bars form as the galaxies grow older.",
    "Unbarred Tight Spiral":"An unbarred spiral galaxy is a type of spiral galaxy without a central bar, or one that is not a barred spiral galaxy. It is designated with an SA in the galaxy morphological classification scheme.Barless spiral galaxies are one of three general types of spiral galaxies under the de Vaucouleurs system classification system, the other two being intermediate spiral galaxy and barred spiral galaxy. Under the Hubble tuning fork, it is one of two general types of spiral galaxy, the other being barred spirals.",
    "Unbarred Loose Spiral":"An unbarred spiral galaxyis a type of spiral galaxy without a central bar, or one that is not a barred spiral galaxy. It is designated with an SA in the galaxy morphological classification scheme.Barless spiral galaxies are one of three general types of spiral galaxies under the de Vaucouleurs system classification system, the other two being intermediate spiral galaxy and barred spiral galaxy. Under the Hubble tuning fork, it is one of two general types of spiral galaxy, the other being barred spirals.",
    "Edge-on without Bulge":"Disk galaxies seen at high angles to the line of sight, the so-called edge-on galaxies, are the only extragalactic objects where it is possible to study the vertical distribution of stars and gas. Thus the edge-on galaxies provide a unique opportunity to directly study the three-dimensional distribution of matter in galaxies.Very thin disk galaxies are an ideal laboratory for studying the formation and evolution of galactic disks.",
    "Edge-on with Bulge":"In astronomy, a galactic bulge (or simply bulge) is a tightly packed group of stars within a larger star formation. The term almost exclusively refers to the central group of stars found in most spiral galaxies (see galactic spheroid). Bulges were historically thought to be elliptical galaxies that happened to have a disk of stars around them, but high-resolution images using the Hubble Space Telescope have revealed that many bulges lie at the heart of a spiral galaxy. It is now thought that there are at least two types of bulges: bulges that are like ellipticals and bulges that are like spiral galaxies."
}

represents: Dict[str, Dict[str, str]] = {
    "Disturbed":{"name":"ESO 510-13","profile":"The galaxy ESO 510-13 is a disturbed galaxy exhibiting a pronounced warp in its disk.","source":"STScI/NASA"},
    "Merging":{"name":"NGC 2632","profile":"This image from NASA's Hubble Space Telescope shows the merging galaxies NGC 2623. The individual galaxies are being pulled apart, and the process is leading to the birth of new stars, seen here in bright blue.", "source":"ESA/Hubble & NASA"},
    "Round Smooth":{"name":"IC 2006","profile":"IC 2006 is an elliptical galaxy in the constellation Eridanus.An image taken by the Hubble Space Telescope in 2015 shows a characteristically smooth profile, with no spiral arms","source":"HST"},
    "In-between Round Smooth":{"name":"ESO 325-G004","profile":"ESO 325-G004 is an elliptical galaxy located approximately 416 million light-years away in the constellation Centaurus.","source":"HST"},
    "Cigar Shaped Smooth":{"name":"NGC 3593","profile":"NGC 3593 is a lenticular galaxy located in the constellation Leo. It has a morphological classification of SA(s)0/a,which indicates it is a lenticular galaxy of the pure spiral type","source":"HST"},
    "Barred Spiral":{"name":"NGC 1300","profile":"NGC 1300 is a barred spiral galaxy located about 61 million light-years away in the constellation Eridanus. The galaxy is about 110,000 light-years across.","source":"NASA/HST"},
    "Unbarred Tight Spiral":{"name":"NGC 4414","profile":"NGC 4414 is an unbarred spiral galaxy in the constellation Coma Berenices. It is a flocculent spiral galaxy, with short segments of spiral structure but without the dramatic well-defined spiral arms of a grand design spiral.","source":"HST"},
    "Unbarred Loose Spiral":{"name":"M99","profile":"M99, also known as NGC 4254 or St. Catherine's Wheel,a pure spiral shape with loosely wound arms. It has a peculiar shape with one normal looking arm and an extended arm that is less tightly wound.","source":"Schulman Telescope"},
    "Edge-on without Bulge":{"name":"NGC 2683","profile":"NGC 2683 also known as the UFO Galaxy, is one of the sky’s best “needles,” running three times as long as it is wide. It lies in Lynx.","source":"Adam Block/Mount Lemmon SkyCenter/University of Arizona"},
    "Edge-on with Bulge":{"name":"NGC 4565","profile":"A close-up of NGC 4565 (the Flying Saucer Galaxy), an edge-on spiral in Coma Berenices.","source":"ESO"}
}