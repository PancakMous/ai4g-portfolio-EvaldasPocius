## 7. Ethical reflection and data card

### Data card

| | |
|---|---|
| **Source** | Our own phone photos and videos. No images from the internet or external datasets. |
| **Collected by** | Haki Abdulovski |
| **Where and when** | Leidschendam, The Hague and Rijswijk, October 2026. Images cover daytime and nighttime conditions in autumn. |
| **What** | Pavements, gutters, drains, grass edges and verges. |
| **Size** | 601 images uploaded, including frames from seven videos. We labelled and used 599 images. |
| **Labels** | One class, `cigarette_butt`, annotated with bounding boxes. Gemini 4 Argon drafted the annotations, and every image underwent manual review. |
| **Split** | 419 training images, 120 validation images and 60 test images. The split is random, so frames from the same video can appear in different sets. |
| **Storage** | Private Roboflow project, with a COCO export in this repository. |
| **Known gaps** | Limited examples in grass and on dark surfaces. No rain or snow, coverage of only three municipalities, and frequent autumn leaves. |

### Risks, and who could be harmed

The main risk is **undercounting litter in green areas**, where cigarette butts can blend into grass, leaves and dark backgrounds. If a municipality trusted these counts without reviewing the photos, it could overlook areas that need cleaning. Comparisons could also be misleading: different lighting, camera distance or weather could change the number of detections even when the amount of litter stays the same.

The reported recall of **72%** shows that the model misses a substantial proportion of labelled cigarette butts. Its test results may also overestimate performance on new locations because similar frames from the same video can appear in both training and test sets. Other risks include false detections and overlapping boxes that count one butt more than once.

Photos could expose identifiable people or number plates. Counts could also support unfair targeting of places associated with particular groups. The prototype therefore needs human review and is **not reliable enough for enforcement, official litter totals or financial claims**.

### What we did about it

- **Visible bounding boxes:** the app shows which objects it counted, allowing users to review detections and identify mistakes.
- **Confidence control:** users can adjust the confidence threshold. Our reported examples and evaluation use thresholds around 0.40–0.42, so results should always state the setting.
- **Honest reporting:** we document missed objects, false detections and the possibility of overlap between video frames across dataset splits.
- **Privacy during collection:** we avoided faces and number plates and kept the Roboflow project private. Uploaded images still go to Roboflow for inference.
- **Human review:** we advise checking the original photo alongside the predictions before drawing conclusions.

For comparisons over time, we recommend photographing the same spots from a similar distance and angle, under similar lighting conditions.

### What it must not be used for

- Identifying or fining **individual smokers**.
- Targeting locations because of **who spends time there**.
- Producing **exact counts** for official reports or financial claims.
- Concluding that an area is clean simply because the model detects no cigarette butts.
- Analysing identifiable people. Users should point the camera at the ground.

### Personal reflection and next steps

My contribution focused on building the Streamlit app and preparing its deployment, while Haki handled data collection and model training. I learned that making predictions accessible also creates a responsibility to explain their limitations. A clear interface can make a model appear more trustworthy than its results justify, especially when it displays a precise count.

Our next steps are to collect more examples in grass and on dark surfaces, including white cigarette filters, and test tiling for small objects. We should investigate duplicate detections before adding box-merging logic. Most importantly, we should split the dataset by video and collection session, then evaluate on genuinely separate locations. Any future location-and-date logging should record cleanup sites without collecting unnecessary personal information.
