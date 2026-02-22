# **Phase 1: Manual Annotation Interface for Cryo‑TEM Liposomes**

## **Introduction**

Phase 1 serves as the essential starting point for the entire liposome
quality‑control pipeline. Cryo‑TEM images contain a wide variety of
vesicle structures, and although a trained human can easily distinguish
between empty vesicles, drug‑loaded vesicles, multilamellar vesicles,
and ruptured vesicles, a machine learning model cannot learn these
distinctions without a curated set of examples. The purpose of this
phase is to create a simple, reliable, and intuitive interface that
allows a human annotator to draw circles or ellipses around individual
liposomes and assign a structural label to each one. These annotations
become the ground truth that drives every later phase of the project,
including the teacher model, the student model, and the final
quality‑control metrics. Without this initial phase, the rest of the
pipeline would have no biologically meaningful foundation.

## **Purpose and Motivation**

Cryo‑TEM datasets are large, visually complex, and often noisy.
Automated segmentation models require a set of human‑verified examples
before they can begin to generalize. Phase 1 exists to provide this
initial set of examples. The goal is not to annotate thousands of images
but to create a small, high‑quality seed dataset that captures the
diversity of vesicle structures. Even a handful of carefully annotated
images can produce dozens or hundreds of labeled vesicles, which is
enough to begin training the teacher model and testing the pipeline.
This phase ensures that the dataset entering the later stages is clean,
consistent, and grounded in real biological structure rather than
assumptions or synthetic labels.

## **Design of the Annotation Tool**

The annotation tool developed in this phase is intentionally lightweight
and easy to use. It runs locally in a browser and loads each Cryo‑TEM
image one at a time, allowing the annotator to focus on a single frame
without distraction. The interface displays the raw image and provides a
drawing canvas on top of it, enabling the user to outline vesicles
directly using the mouse. The tool supports both circles and ellipses,
which is important because liposomes in Cryo‑TEM images are rarely
perfect circles. Many appear slightly elongated or distorted due to
imaging angle, membrane tension, or interactions with neighboring
vesicles. Allowing ellipses gives the annotator the flexibility to
capture these shapes accurately without forcing a rigid geometry onto
structures that are naturally variable.

Before drawing each shape, the annotator selects a label that describes
the vesicle's structural state. The four categories used in this
project---Empty, Loaded, Multilamellar, and Ruptured---capture the major
morphological variations that appear in Cryo‑TEM datasets. Empty
vesicles typically show a thin, uniform membrane with a clear interior.
Loaded vesicles contain dense material inside, which appears darker in
grayscale images. Multilamellar vesicles have multiple concentric
membrane layers, giving them a characteristic onion‑like appearance.
Ruptured vesicles show broken or collapsed membranes and often appear
irregular or partially open. These categories are biologically
meaningful and directly relevant to drug‑delivery research, where the
structural integrity and loading state of liposomes determine their
therapeutic behavior.

## **Automatic Feature Extraction**

As the annotator draws each shape, the tool automatically computes the
mean grayscale intensity inside the region. This feature is valuable
because intensity often correlates with loading state. A vesicle filled
with drug material tends to appear darker than an empty one, and
multilamellar vesicles often show alternating dark and light rings. By
capturing intensity at the moment of annotation, the tool enriches the
dataset with quantitative information that can later help the model
distinguish between subtle structural differences. This intensity
measurement is computed on the displayed image, and although it can be
mapped back to the original resolution later, the immediate value lies
in giving each annotation a numerical descriptor that complements the
label.

## **Annotation Output and Data Structure**

Once the annotator finishes marking all vesicles in an image, the tool
saves the annotations as a JSON file. Each image receives its own JSON
file, named after the image itself, and stored in a dedicated
annotations directory. The JSON file contains the image dimensions, the
number of annotations, and a list of all annotated vesicles. For each
vesicle, the file records the center coordinates, the radii of the
ellipse or circle, the assigned label, and the computed mean intensity.
This structured format makes the annotations easy to parse, validate,
and feed into later phases of the pipeline. It also ensures that the
annotations are reproducible and can be reloaded into the tool for
editing if needed.

## **User Workflow and Navigation**

The tool includes simple navigation controls that allow the annotator to
move forward or backward through the dataset. This is especially useful
when working with large collections of images, because it allows the
annotator to review previous work, correct mistakes, or skip images that
do not contain useful structures. The interface is designed to be
non‑destructive, meaning that saved annotations can always be reopened
and modified. This flexibility is important because annotation is often
an iterative process. The annotator may refine their labeling criteria
as they gain experience, or they may want to revisit earlier images
after seeing new patterns in later ones.

## **Importance of Phase 1 in the Pipeline**

The significance of Phase 1 extends far beyond the act of drawing shapes
on images. These annotations form the backbone of the entire machine
learning pipeline. The teacher model in Phase 3 relies on these
human‑verified examples to learn what each class looks like. The student
model in Phase 4 uses the teacher's pseudo‑labels, which are grounded in
the annotations created here. The quality‑control metrics in Phase 5
depend on accurate segmentation and classification, both of which trace
back to the initial human annotations. Even the JSON schema in Phase 2
is built around the structure of the annotation files produced in this
phase. In other words, Phase 1 is the only part of the pipeline where
human expertise directly enters the system, and everything that follows
is shaped by the quality and consistency of this initial work.

## **Human Insight and Dataset Familiarity**

Another important aspect of Phase 1 is that it helps the researcher
develop an intuitive understanding of the dataset. By manually examining
and labeling vesicles, the annotator becomes familiar with the natural
variability of liposomes, the subtle differences between classes, and
the challenges that the model will eventually need to overcome. This
insight becomes useful later when interpreting model outputs, evaluating
segmentation quality, or analyzing quality‑control metrics. In this
sense, Phase 1 is not just a technical step but also a conceptual one,
grounding the researcher in the biological reality of the system they
are modeling.

## **Conclusion**

Phase 1 provides the essential human‑verified annotations that make the
entire liposome quality‑control pipeline possible. It offers a simple
and intuitive interface for drawing circles and ellipses around
vesicles, assigning structural labels, and capturing intensity
information. It produces clean, structured JSON files that feed directly
into later phases. It requires only a small number of images to begin
producing meaningful results, and it gives the researcher a deeper
understanding of the dataset. Phase 1 is the anchor point for the entire
project, and its outputs form the foundation upon which every subsequent
phase is built.
