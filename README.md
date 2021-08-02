#AppleBottomGenius
A high-tech solution to a problem no one is facing.

##Processing overview
<sub>*Subject to change at any moment because we have no idea what we are doing</sub>

1. User inputs image -> image cleaned, normalized, and processed to fork of Matterport's infamous Mask-RCNN.

2. Mask R-CNN to semantically instances all apples in frame -> returns bounding boxes and mask polygon.

3. Mask polygon is fed through proprietory AppleGeometry algorithm to determine which way is up (#deepthoughts) -> returns <sup>o</sup> in angles to rotate smiley faces to align properly with apples.

4. Smiley faces are then scaled to original image proportions and then applied to original image user uploaded -> return picture with smiling, happy, and healthy apples.
