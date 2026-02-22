# **Quantitative Quality Control of Liposomal Drug Formulations via AI‑Driven Cryo‑TEM Analysis**

## **Abstract**

Liposomal drug formulations have become an important part of modern
therapeutics because they can carry drugs in a protected and controlled
way. Their structure allows them to encapsulate hydrophilic drugs in the
aqueous core and hydrophobic drugs in the membrane. This flexibility
makes them useful for chemotherapy, vaccines, and many other treatments.
But the performance of a liposomal drug depends on the physical
properties of the vesicles. The size of the vesicle, the thickness of
the membrane, the number of bilayers, and the degree of drug loading all
influence how the drug behaves in the body. Even small changes in these
properties can change circulation time, release rate, and therapeutic
effect. Because of this, manufacturers need reliable ways to measure
these properties during production.

Cryogenic transmission electron microscopy (Cryo‑TEM) is one of the few
imaging methods that can directly visualize liposomes in their hydrated,
near‑native state. The technique freezes the sample so quickly that
water forms a glass‑like solid instead of ice crystals. This preserves
the vesicles without distortion. The electron beam passes through the
thin layer of vitrified sample, and the resulting image shows the
vesicles with high spatial resolution. Cryo‑TEM can reveal membrane
thickness, lamellarity, and the presence of dense drug crystals inside
the core. These features make it a powerful tool for evaluating
liposomal drug formulations.

The problem is that Cryo‑TEM images are difficult to analyze manually.
They contain many overlapping vesicles, and the images are noisy because
low electron doses are used to avoid damaging the sample. Analysts must
identify each vesicle, classify it as empty or loaded, measure its
diameter, and detect structural defects. This process is slow and
subjective. Different analysts may classify the same vesicle
differently, especially when the contrast is subtle. Manual analysis
becomes a bottleneck when manufacturers need to analyze thousands of
vesicles per batch.

This paper presents a complete AI‑driven pipeline for quantitative
quality control of liposomal drug formulations using Cryo‑TEM images.
The system integrates a human annotation interface, a structured JSON
data format, a multimodal teacher model, and a Mask R‑CNN instance
segmentation model. The human interface allows experts to draw circles
or ellipses around vesicles and assign labels. The JSON format keeps the
data organized and easy to parse. The teacher model uses multimodal
reasoning to detect vesicles and classify them. The student model uses
instance segmentation to identify individual vesicles and measure their
diameters. The pipeline measures encapsulation efficiency, size
distribution, and structural defects.

The system is grounded in the physics of Cryo‑TEM imaging and the
biology of liposomal drug delivery. It uses mass‑thickness contrast to
distinguish between empty and loaded vesicles. It uses instance
segmentation to count vesicles and measure their sizes. It uses
knowledge distillation and semi‑supervised learning to improve
performance when labeled data is limited. The pipeline is designed to be
practical, scalable, and easy to integrate into existing workflows.

The paper also compares the liposome workflow to a metallurgy pipeline.
The comparison shows how different physical principles shape the design
of AI systems. Metallurgy relies on diffraction contrast and thin,
winding grain boundaries. Liposome analysis relies on mass‑thickness
contrast and circular vesicles. These differences influence the choice
of model architecture and quality metrics.

The goal of this work is to create a reliable method for high‑throughput
quality control in pharmaceutical manufacturing. The pipeline reduces
human workload, increases consistency, and provides quantitative
measurements that support regulatory requirements. It also shows how AI
can bridge the gap between noisy scientific images and practical
manufacturing needs.

# **1. Introduction**

Liposomal drug formulations have become an important part of modern
therapeutics because they can carry drugs in a protected and controlled
way. Their structure allows them to encapsulate hydrophilic drugs in the
aqueous core and hydrophobic drugs in the membrane. This flexibility
makes them useful for chemotherapy, vaccines, gene delivery, and many
other treatments. But the performance of a liposomal drug depends on the
physical properties of the vesicles. The size of the vesicle, the
thickness of the membrane, the number of bilayers, and the degree of
drug loading all influence how the drug behaves in the body. Even small
changes in these properties can change circulation time, release rate,
and therapeutic effect. Because of this, manufacturers need reliable
ways to measure these properties during production.

Quality control is especially important for liposomal formulations
because they are sensitive to manufacturing conditions. Small changes in
temperature, pH, lipid composition, or mixing speed can change the size
distribution or the encapsulation efficiency. These changes may not be
visible to the naked eye, but they can influence how the drug is
released in the body. Regulatory agencies expect manufacturers to
monitor these properties carefully. This creates a need for methods that
can measure vesicle size, membrane structure, and drug loading in a
consistent and repeatable way.

Cryogenic transmission electron microscopy (Cryo‑TEM) is widely used for
this purpose because it preserves the native structure of liposomes
without staining or dehydration. The technique involves rapidly freezing
the sample so that water forms a glass‑like solid. This preserves the
vesicles in a state that is close to how they exist in solution. The
electron beam passes through the thin layer of vitrified sample, and the
resulting image shows the vesicles with high spatial resolution.
Cryo‑TEM can reveal membrane thickness, lamellarity, and the presence of
dense drug crystals inside the core. These features make it a powerful
tool for evaluating liposomal drug formulations.

The challenge is that Cryo‑TEM images are difficult to analyze manually.
They contain many overlapping vesicles, and the images are noisy because
low electron doses are used to avoid damaging the sample. Analysts must
identify each vesicle, classify it as empty or loaded, measure its
diameter, and detect structural defects. This process is slow and
subjective. Different analysts may classify the same vesicle
differently, especially when the contrast is subtle. Manual analysis
becomes a bottleneck when manufacturers need to analyze thousands of
vesicles per batch.

Deep learning offers a way to automate this process. Models such as
U‑Net (Ronneberger et al., 2015) and Mask R‑CNN (He et al., 2017) have
shown strong performance in biomedical image segmentation. These models
can detect objects, segment them, and classify them. Large multimodal
models can interpret images and follow instructions. They can detect
vesicles, classify them, and return structured outputs. Knowledge
distillation (Hinton et al., 2015; Sanh et al., 2019; Xie et al., 2020)
and semi‑supervised learning (Chapelle et al., 2006) make it possible to
train accurate models even when labeled data is limited. These
developments create an opportunity to build a hybrid system that uses
human expertise, multimodal reasoning, and instance segmentation to
analyze liposomes at scale.

This paper presents such a system. It includes a human annotation
interface, a JSON‑based data structure, a multimodal teacher model, a
Mask R‑CNN student model, and a set of biological and computational
quality metrics. The human interface allows experts to draw circles or
ellipses around vesicles and assign labels. The JSON format keeps the
data organized and easy to parse. The teacher model uses multimodal
reasoning to detect vesicles and classify them. The student model uses
instance segmentation to identify individual vesicles and measure their
diameters. The pipeline measures encapsulation efficiency, size
distribution, and structural defects.

The system is grounded in the physics of Cryo‑TEM imaging and the
biology of liposomal drug delivery. It uses mass‑thickness contrast to
distinguish between empty and loaded vesicles. It uses instance
segmentation to count vesicles and measure their sizes. It uses
knowledge distillation and semi‑supervised learning to improve
performance when labeled data is limited. The pipeline is designed to be
practical, scalable, and easy to integrate into existing workflows.

The paper also compares the liposome workflow to a metallurgy pipeline.
The comparison shows how different physical principles shape the design
of AI systems. Metallurgy relies on diffraction contrast and thin,
winding grain boundaries. Liposome analysis relies on mass‑thickness
contrast and circular vesicles. These differences influence the choice
of model architecture and quality metrics.

The goal of this work is to create a reliable method for high‑throughput
quality control in pharmaceutical manufacturing. The pipeline reduces
human workload, increases consistency, and provides quantitative
measurements that support regulatory requirements. It also shows how AI
can bridge the gap between noisy scientific images and practical
manufacturing needs. The system is flexible and can be adapted to
different types of vesicles or imaging conditions. It provides a
foundation for future work in automated analysis of nanoscale
structures.

# **2. Biological and Physical Background**

Understanding how liposomes behave in Cryo‑TEM images requires a clear
view of both the biology of the vesicles and the physics of electron
imaging. Liposomes are simple in structure, but their behavior in
solution and under the electron beam is shaped by many small physical
details. These details matter for quality control because they influence
how the vesicles look in the final images. This section explains the
structure of liposomes, how they encapsulate drugs, how Cryo‑TEM forms
contrast, and why these principles make automated analysis possible.

## **2.1 Liposome Structure and Function**

Liposomal vesicles are spherical structures formed by phospholipid
molecules. Each phospholipid has a hydrophilic head and hydrophobic
tails. When placed in water, these molecules spontaneously arrange
themselves into bilayers. The bilayer curves to form a closed sphere,
creating an aqueous core surrounded by a membrane. This structure allows
liposomes to encapsulate hydrophilic drugs in the core and hydrophobic
drugs in the membrane.

The membrane is usually made of phosphatidylcholine or similar lipids.
Cholesterol is often added to make the membrane more rigid. The exact
lipid composition influences the stability of the vesicle. For example,
saturated lipids create more rigid membranes, while unsaturated lipids
create more flexible ones. These differences affect how the vesicle
behaves in the bloodstream.

The size of the vesicle is another important factor. Small vesicles
circulate longer because they are less likely to be cleared by the
immune system. Large vesicles may release the drug more slowly because
the diffusion path is longer. The size distribution is usually measured
by dynamic light scattering (DLS), but Cryo‑TEM provides a direct view
of the vesicles and can reveal details that DLS cannot.

The number of bilayers also matters. Unilamellar vesicles have a single
bilayer. Multilamellar vesicles have multiple concentric bilayers.
Multilamellar vesicles release drugs more slowly because the drug must
diffuse through multiple layers. They also scatter electrons
differently, which affects how they appear in Cryo‑TEM images.

Ruptured vesicles are another concern. These vesicles have lost part of
their membrane and may release their contents prematurely. Ruptured
vesicles can be caused by mechanical stress, temperature changes, or
poor manufacturing conditions. Detecting ruptured vesicles is important
for quality control because they indicate instability in the
formulation.

## **2.2 Drug Loading and Encapsulation Mechanisms**

Liposomal drug formulations rely on the ability of the vesicles to
encapsulate drugs. Hydrophilic drugs such as Doxorubicin accumulate
inside the aqueous core. Hydrophobic drugs embed in the membrane. The
loading method depends on the type of drug.

For hydrophilic drugs, passive loading is often used. The drug is
dissolved in the aqueous phase, and the vesicles form around it. This
method is simple but may result in low encapsulation efficiency.

Active loading methods can achieve higher encapsulation efficiency. One
common method uses a pH gradient. The vesicles are formed with an acidic
interior. The drug is added to the outside, and it diffuses into the
vesicle. Once inside, the drug becomes protonated and trapped. This
method is used for Doxorubicin and other weakly basic drugs.

The presence of drug crystals inside the core changes the density of the
vesicle. This creates a strong contrast in Cryo‑TEM images. Loaded
vesicles appear darker because the drug crystals absorb more electrons.
Empty vesicles appear lighter because the core has the same density as
the surrounding buffer. This difference in contrast makes it possible to
classify vesicles automatically.

## **2.3 Cryo‑TEM Imaging and Contrast Formation**

Cryo‑TEM forms images by transmitting electrons through a thin layer of
vitrified sample. The contrast arises from differences in
mass‑thickness. Regions with more mass or thickness absorb more
electrons and appear darker. This principle is simple, but it creates a
powerful way to distinguish between empty and loaded vesicles.

The sample is prepared by placing a small drop of solution on a grid,
blotting away most of the liquid, and plunging the grid into liquid
ethane. The water freezes so quickly that it forms a glass‑like solid
instead of ice crystals. This preserves the vesicles without distortion.
The grid is then placed in the electron microscope at liquid nitrogen
temperature.

The electron beam passes through the thin layer of vitrified sample. The
electrons interact with the atoms in the sample. Regions with more mass
or thickness scatter more electrons. The detector records the electrons
that pass through. The resulting image shows the vesicles with high
spatial resolution.

Cryo‑TEM images are noisy because low electron doses are used to avoid
damaging the sample. The noise can obscure the boundaries of the
vesicles and make it difficult to distinguish between empty and loaded
vesicles. Automated methods must be robust to this noise.

## **2.4 Why Cryo‑TEM Enables Automated Classification**

The contrast between empty and loaded vesicles is strong enough that
automated methods can classify them. Loaded vesicles contain dense drug
crystals that absorb more electrons. This makes the core appear darker.
Empty vesicles have a core with the same density as the surrounding
buffer, so the interior appears similar in intensity.

This difference in contrast is consistent across images. It does not
depend on staining or other chemical treatments. It is a direct result
of the physics of electron scattering. This makes it a reliable feature
for automated classification.

The circular shape of the vesicles also helps. The membrane forms a
clear boundary that can be detected by edge‑finding algorithms. The
circular shape makes it easier to measure the diameter. These features
make liposomes well suited for instance segmentation.

## **2.5 Encapsulation Efficiency as a Quality Metric**

Encapsulation efficiency is defined as the ratio of loaded vesicles to
total vesicles. It reflects how well the manufacturing process traps the
drug inside the vesicles. High encapsulation efficiency means that most
vesicles contain the drug. Low encapsulation efficiency means that many
vesicles are empty.

Cryo‑TEM provides a direct way to measure this ratio by counting
dark‑core vesicles. Automating this measurement reduces human bias and
increases throughput. It also provides a way to detect changes in the
manufacturing process. For example, a drop in encapsulation efficiency
may indicate a problem with the pH gradient or the mixing conditions.

# **3. Technical Pipeline**

The technical pipeline is the core of this project. It connects the
biological and physical principles of liposomes with the computational
tools that analyze them. The pipeline is designed to be simple enough
for practical use but detailed enough to capture the complexity of
Cryo‑TEM images. It combines human expertise, multimodal reasoning, and
instance segmentation. Each part of the pipeline plays a specific role,
and the parts work together to create a complete system for quantitative
quality control.

The pipeline has four main components:

1.  A human annotation interface

2.  A structured JSON data format

3.  A multimodal teacher model

4.  A Mask R‑CNN student model

Each component is explained in detail below.

## **3.1 Human Annotation Interface**

The first step in the pipeline is a human annotation interface built
with Streamlit. The interface displays a Cryo‑TEM image and allows the
user to draw circles or ellipses around vesicles. The user assigns a
label to each vesicle, such as "Empty," "Loaded," "Multilamellar," or
"Ruptured." The interface also computes the mean pixel intensity of the
core to verify the label. This step creates high‑quality gold data for
training and evaluation.

The interface is designed to be simple and intuitive. It uses a drawable
canvas and a dropdown menu. The user can adjust the size and position of
the circles. The interface displays the computed intensity values so the
user can confirm the classification. This reduces labeling errors and
improves the quality of the dataset.

The interface also supports batch processing. The user can load multiple
images and annotate them one by one. The interface saves the annotations
automatically. This makes it easy to create a large dataset.

The interface is flexible. It can be extended to include additional
labels or features. For example, it can include a label for vesicles
that are partially loaded. It can include a tool for measuring membrane
thickness. It can include a tool for detecting ice contamination. These
features can be added as needed.

The interface is important because it creates the ground truth for the
model. The quality of the annotations influences the performance of the
model. The interface makes it easy to create consistent and accurate
annotations.

## **3.2 JSON Data Structure**

Each annotated image is stored in a structured JSON format. The JSON
file includes the image ID, the total number of vesicles, the number of
loaded vesicles, the encapsulation efficiency, the size distribution,
and the number of defects. This structure keeps the data consistent and
easy to parse. It also supports downstream analysis and model training.

The JSON format is flexible and can be extended to include additional
fields. For example, it can store the coordinates of the bounding
circles, the pixel intensity values, or the confidence scores from the
model. This makes it easy to integrate the data into other systems.

The JSON format also supports versioning. Each file can include a
version number that indicates the format of the data. This makes it easy
to update the format without breaking existing code.

The JSON format is important because it keeps the data organized. It
makes it easy to load the data into Python or other programming
languages. It makes it easy to share the data with other researchers. It
makes it easy to train the model.

## **3.3 Teacher Model: Multimodal AI**

A multimodal model such as Gemini 2.5 Pro or Flash acts as a teacher.
The model receives a Cryo‑TEM image and a prompt that asks it to detect
vesicles, classify them, and return a JSON list of bounding boxes and
labels. Multimodal models can handle noisy images and follow
instructions well. Their ability to generalize across domains is similar
to the way end‑to‑end systems learn complex tasks in other fields
(Bojarski et al., 2016).

The teacher model provides high‑quality pseudo‑labels for unlabeled
images. This is useful because labeled data is limited. Knowledge
distillation (Hinton et al., 2015; Sanh et al., 2019; Xie et al., 2020)
allows the student model to learn from the teacher's predictions.
Semi‑supervised learning (Chapelle et al., 2006) and active learning
(Settles, 2009) help improve performance when labeled data is scarce.

The teacher model is not perfect. It may make mistakes, especially when
the contrast is subtle. But it provides a strong starting point for the
student model. The student model can learn from the teacher's
predictions and improve over time.

The teacher model is important because it reduces the need for manual
annotations. It makes it possible to train the student model on a large
dataset. It also provides a way to incorporate multimodal reasoning into
the pipeline.

## **3.4 Student Model: Mask R‑CNN**

The student model is a Mask R‑CNN instance segmentation network with a
ResNet‑50 backbone pre‑trained on COCO (Lin et al., 2014). Mask R‑CNN is
well suited for this task because it identifies individual objects
rather than just labeling pixels. This is important for counting
vesicles and measuring their diameters. The model is fine‑tuned on the
annotated dataset and the teacher‑generated labels.

Mask R‑CNN outputs a bounding box, a class label, and a segmentation
mask for each vesicle. The segmentation mask allows precise measurement
of the vesicle diameter. The class label indicates whether the vesicle
is empty or loaded. The bounding box helps with visualization and
post‑processing.

The model is trained using a combination of supervised and
semi‑supervised learning. The supervised part uses the human
annotations. The semi‑supervised part uses the teacher's predictions.
This combination improves performance when labeled data is limited.

The model is evaluated using the F1‑score, the size distribution, and
the encapsulation efficiency. These metrics provide a clear way to
evaluate performance.

The student model is important because it provides the final
predictions. It is the part of the pipeline that will be used in
production. It must be accurate, fast, and reliable.

# **4. Quality Control Metrics**

Quality control is the central purpose of this entire pipeline. The
biological and physical background explains why liposomes behave the way
they do. The technical pipeline explains how the system detects and
classifies vesicles. But none of that matters unless the system can
produce quantitative measurements that are meaningful, repeatable, and
useful for manufacturing decisions. Quality control metrics turn raw
detections into actionable information.

In this section, each metric is expanded in detail. The goal is to show
not only what the metric measures, but why it matters, how it is
computed, and how it fits into the broader context of pharmaceutical
quality control.

The three main metrics are:

1.  **Detection Accuracy**

2.  **Size Distribution**

3.  **Encapsulation Efficiency**

Each metric captures a different aspect of liposome quality. Together,
they provide a complete view of the formulation.

## **4.1 Detection Accuracy**

Detection accuracy measures how well the model identifies vesicles in
the Cryo‑TEM images. This is the foundation of the entire pipeline. If
the model cannot detect vesicles reliably, then every downstream
measurement becomes unreliable. For example, if the model misses large
vesicles, the size distribution will shift. If it misclassifies empty
vesicles as loaded, the encapsulation efficiency will be inflated.

Detection accuracy is measured using the **F1‑score**, which is the
harmonic mean of precision and recall.

**Precision** measures how many detected objects are true vesicles.

High precision means the model makes few false positives.

-   This is important because false positives inflate the vesicle count
    > and distort the encapsulation efficiency.

**Recall** measures how many real vesicles were found.

High recall means the model finds most of the vesicles.

-   This is important because missing vesicles shifts the size
    > distribution and reduces the accuracy of the encapsulation
    > efficiency.

The **F1‑score** balances these two values. It is a single number that
captures the trade‑off between precision and recall. A high F1‑score
means the model is both accurate and consistent.

The F1‑score is computed by comparing the model's predictions to the
human annotations. The human annotations serve as the ground truth. The
model's predictions are matched to the ground truth using an
intersection‑over‑union (IoU) threshold. If the IoU is above the
threshold, the prediction is considered correct.

The F1‑score is important because it provides a clear way to evaluate
the model. It shows whether the model is ready for production. It also
shows whether the model needs more training data or better
hyperparameters.

## **4.2 Size Distribution**

The size distribution is one of the most important quality control
metrics for liposomal drug formulations. The size of the vesicles
influences how the drug behaves in the body. Small vesicles circulate
longer. Large vesicles release the drug more slowly. A shift in the size
distribution can indicate a problem with the manufacturing process.

The size distribution is computed from the diameters of the segmented
vesicles. The segmentation mask from the Mask R‑CNN model provides a
precise outline of each vesicle. The diameter is computed by fitting a
circle or ellipse to the mask. The diameters are then collected into a
histogram.

The histogram shows how many vesicles fall into each size range. The
mean diameter and the standard deviation are computed from the
histogram. These values provide a simple summary of the size
distribution.

The size distribution is compared to the human‑generated distribution.
If the AI‑generated distribution matches the human‑generated one, then
the model is performing well. If the AI‑generated distribution is
shifted, then the model may be missing certain vesicles.

For example:

-   If the AI misses large vesicles, the mean diameter will be lower.

-   If the AI misses small vesicles, the mean diameter will be higher.

-   If the AI misclassifies multilamellar vesicles, the distribution may
    > become wider.

The size distribution is important because it provides a direct measure
of the physical properties of the vesicles. It is also important for
regulatory compliance. Manufacturers must show that the size
distribution is consistent across batches.

## **4.3 Encapsulation Efficiency**

Encapsulation efficiency is defined as the ratio of loaded vesicles to
total vesicles. It reflects how well the manufacturing process traps the
drug inside the vesicles. High encapsulation efficiency means that most
vesicles contain the drug. Low encapsulation efficiency means that many
vesicles are empty.

Cryo‑TEM provides a direct way to measure this ratio by counting
dark‑core vesicles. Loaded vesicles contain dense drug crystals that
absorb more electrons. This makes the core appear darker. Empty vesicles
have a core with the same density as the surrounding buffer, so the
interior appears similar in intensity.

The model classifies each vesicle as empty or loaded based on the mean
pixel intensity of the core. The classification is verified using the
segmentation mask. The number of loaded vesicles is divided by the total
number of vesicles to compute the encapsulation efficiency.

Encapsulation efficiency is important because it reflects the
performance of the manufacturing process. A drop in encapsulation
efficiency may indicate a problem with the pH gradient or the mixing
conditions. It may also indicate that the vesicles are leaking.

Encapsulation efficiency is also important for regulatory compliance.
Manufacturers must show that the encapsulation efficiency is consistent
across batches. Automated measurement reduces human bias and increases
throughput.

# **5. Comparison to Metallurgy Pipeline**

Comparing the liposome pipeline to a metallurgy pipeline helps show how
different physical principles shape the design of AI systems. At first
glance, both pipelines involve microscopy images, segmentation models,
and quality control metrics. But the similarities end there. The
underlying physics, the shapes of the objects, the sources of contrast,
and the goals of the analysis are completely different. These
differences influence every part of the pipeline, from the choice of
model architecture to the way the data is labeled.

This section explains the metallurgy pipeline in detail and compares it
to the liposome pipeline. The goal is to show how the physics of the
sample determines the structure of the AI system.

## **5.1 Metallurgy Pipeline Overview**

A metallurgy pipeline focuses on the microstructure of metals. Metals
are made of grains, which are small crystals that form during
solidification. The boundaries between the grains are thin, winding
lines. These lines influence the mechanical properties of the metal. For
example, smaller grains make the metal stronger because the grain
boundaries block the movement of dislocations.

Metallurgists use electron microscopy to study the grain boundaries. The
images show thin, winding lines that trace the edges of the grains. The
contrast in these images comes from diffraction. When the electron beam
hits the metal, the electrons scatter in different directions depending
on the orientation of the crystal. This creates bright and dark regions.
The grain boundaries appear as thin lines where the orientation changes.

The goal of the metallurgy pipeline is to detect the grain boundaries
and measure the grain size. The grain size is an important quality
control metric because it influences the strength of the metal. The
grain boundaries are thin and continuous, so the pipeline uses semantic
segmentation. The model labels each pixel as either "grain boundary" or
"not grain boundary." The grain boundaries are then traced to compute
the grain size.

## **5.2 Liposome Pipeline Overview**

The liposome pipeline focuses on spherical vesicles. The vesicles are
circular in shape, and the contrast comes from mass‑thickness. Loaded
vesicles contain dense drug crystals that absorb more electrons. This
makes the core appear darker. Empty vesicles have a core with the same
density as the surrounding buffer, so the interior appears similar in
intensity.

The goal of the liposome pipeline is to detect the vesicles, classify
them as empty or loaded, measure their diameters, and detect structural
defects. The vesicles are distinct objects, so the pipeline uses
instance segmentation. The model identifies each vesicle as a separate
object. This is important for counting the vesicles and measuring their
sizes.

## **5.3 Differences in Target Shape**

The most obvious difference between the two pipelines is the shape of
the objects.

In metallurgy, the objects of interest are **thin, winding lines**.

-   These lines trace the boundaries between grains. They are continuous
    > and irregular.

In liposome analysis, the objects of interest are **circles or
ellipses**.

-   These shapes are closed and compact.

This difference in shape influences the choice of model architecture.

For metallurgy, a **U‑Net** is used because it performs semantic
segmentation.

-   It labels each pixel as "boundary" or "not boundary."

For liposomes, a **Mask R‑CNN** is used because it performs instance
segmentation.

-   It identifies each vesicle as a separate object.

The shape of the objects also influences the labeling process. In
metallurgy, the user draws lines. In liposome analysis, the user draws
circles.

## **5.4 Differences in Physics**

The physics of the sample determines the source of contrast in the
images.

In metallurgy, the contrast comes from **diffraction**.

The electron beam interacts with the crystal lattice.

The orientation of the crystal determines how the electrons scatter.

-   Grain boundaries appear as thin lines where the orientation changes.

In liposome analysis, the contrast comes from **mass‑thickness**.

Loaded vesicles contain dense drug crystals that absorb more electrons.

This makes the core appear darker.

-   Empty vesicles have a core with the same density as the buffer.

These differences in physics influence the classification task.

-   In metallurgy, the classification is binary: boundary or not
    > boundary.

-   In liposome analysis, the classification is multi‑class: empty,
    > loaded, multilamellar, ruptured.

The physics also influences the noise in the images. Cryo‑TEM images are
noisy because low electron doses are used. Metallurgy images may have
different types of noise depending on the imaging conditions.

## **5.5 Differences in Quality Metrics**

The quality metrics reflect the goals of the analysis.

In metallurgy, the key metric is **grain size**.

Grain size influences the strength of the metal.

-   The grain boundaries are traced to compute the grain size.

In liposome analysis, the key metric is **encapsulation efficiency**.

Encapsulation efficiency reflects how well the vesicles trap the drug.

-   The number of loaded vesicles is divided by the total number of
    > vesicles.

The size distribution is also important in both pipelines, but the
meaning is different.

-   In metallurgy, the size distribution refers to the size of the
    > grains.

-   In liposome analysis, the size distribution refers to the diameter
    > of the vesicles.

These differences show how the physics of the sample determines the
quality metrics.

## **5.6 Why the Comparison Matters**

The comparison between the two pipelines shows that AI systems must be
designed with the physics of the sample in mind. The shape of the
objects, the source of contrast, the type of noise, and the goals of the
analysis all influence the choice of model architecture, the labeling
process, and the quality metrics.

This comparison also shows that AI is not a one‑size‑fits‑all solution.
The same model cannot be used for both pipelines. The model must be
chosen based on the specific characteristics of the sample.

The comparison highlights the importance of understanding the underlying
physics. Without this understanding, it is easy to choose the wrong
model or the wrong metric. The physics provides the foundation for the
entire pipeline.

# **6. Discussion**

The goal of this project is to create a practical and scalable method
for analyzing liposomal drug formulations using Cryo‑TEM images. The
pipeline combines human annotation, multimodal reasoning, and instance
segmentation. Each part of the pipeline plays a specific role, and the
parts work together to create a complete system for quantitative quality
control. The discussion below explains how the pieces fit together, why
the system works, and what the results mean for real‑world
manufacturing.

## **6.1 The Value of Combining Human Expertise and AI**

One of the strengths of this pipeline is that it combines human
expertise with AI. Human experts understand the biology of liposomes and
the physics of Cryo‑TEM imaging. They can identify subtle features that
may be difficult for a model to learn. But humans are slow and
inconsistent. They cannot analyze thousands of vesicles quickly.

AI models are fast and consistent. They can analyze large datasets in
seconds. But they need high‑quality training data. They also need
guidance when the images are noisy or ambiguous.

The pipeline uses a human annotation interface to create high‑quality
gold data. This data is used to train the student model. The teacher
model provides additional pseudo‑labels. The combination of human
annotations and teacher predictions creates a rich dataset that supports
semi‑supervised learning.

This approach takes advantage of the strengths of both humans and AI.
Humans provide the expertise. AI provides the speed and consistency.
Together, they create a system that is more powerful than either one
alone.

## **6.2 Why Multimodal Models Make Good Teachers**

Multimodal models such as Gemini 2.5 Pro or Flash can interpret images
and follow instructions. They can detect vesicles, classify them, and
return structured outputs. They can handle noisy images and ambiguous
cases. They can also explain their reasoning.

These models make good teachers because they can generate high‑quality
pseudo‑labels for unlabeled images. This is important because labeled
data is limited. The teacher model can label thousands of images
quickly. The student model can learn from these labels.

Knowledge distillation (Hinton et al., 2015; Sanh et al., 2019; Xie et
al., 2020) provides a framework for transferring knowledge from the
teacher to the student. The student model learns to mimic the teacher's
predictions. This improves performance, especially when labeled data is
scarce.

The teacher model is not perfect. It may make mistakes, especially when
the contrast is subtle. But the student model can learn from the
teacher's predictions and improve over time. The student model can also
learn from the human annotations, which serve as the ground truth.

## **6.3 Why Mask R‑CNN Is the Right Choice for Liposomes**

Mask R‑CNN is well suited for liposome analysis because it performs
instance segmentation. It identifies each vesicle as a separate object.
This is important for counting the vesicles and measuring their sizes.
The segmentation mask provides a precise outline of each vesicle. The
class label indicates whether the vesicle is empty or loaded.

The circular shape of the vesicles makes instance segmentation easier.
The membrane forms a clear boundary that can be detected by the model.
The contrast between empty and loaded vesicles is strong enough that the
model can classify them based on the mean pixel intensity of the core.

Mask R‑CNN also supports multi‑class classification. This makes it
possible to detect multilamellar vesicles and ruptured vesicles. These
defects are important for quality control because they indicate
instability in the formulation.

The model is trained using a combination of supervised and
semi‑supervised learning. The supervised part uses the human
annotations. The semi‑supervised part uses the teacher's predictions.
This combination improves performance when labeled data is limited.

## **6.4 Why Cryo‑TEM Is a Good Fit for AI Analysis**

Cryo‑TEM provides a direct view of the vesicles. The images show the
vesicles in their hydrated, near‑native state. The contrast between
empty and loaded vesicles is strong enough that automated methods can
classify them. The circular shape of the vesicles makes instance
segmentation easier.

Cryo‑TEM images are noisy because low electron doses are used. But
modern AI models are robust to noise. They can learn to detect the
vesicles even when the boundaries are faint. They can also learn to
classify the vesicles based on the mean pixel intensity of the core.

Cryo‑TEM is a good fit for AI analysis because the images contain
consistent features. The membrane forms a clear boundary. The core has a
consistent intensity. The defects have recognizable shapes. These
features make it possible to train a model that performs well across
different images.

## **6.5 How the Pipeline Supports Manufacturing Quality Control**

The pipeline provides quantitative measurements that support
manufacturing quality control. The detection accuracy shows whether the
model is reliable. The size distribution shows whether the vesicles are
the right size. The encapsulation efficiency shows whether the vesicles
contain the drug.

These metrics are important for regulatory compliance. Manufacturers
must show that the size distribution and the encapsulation efficiency
are consistent across batches. Automated measurement reduces human bias
and increases throughput. It also provides a way to detect changes in
the manufacturing process.

For example:

-   A shift in the size distribution may indicate a problem with the
    > mixing conditions.

-   A drop in encapsulation efficiency may indicate a problem with the
    > pH gradient.

-   An increase in ruptured vesicles may indicate mechanical stress.

The pipeline provides a way to detect these changes quickly. It also
provides a way to document the results.

## **6.6 Limitations and Future Work**

The pipeline has limitations. The teacher model may make mistakes. The
student model may struggle with images that have very low contrast. The
segmentation masks may not be perfect. The classification may be
ambiguous in some cases.

Future work could focus on improving the teacher model, collecting more
labeled data, or using more advanced architectures. It could also focus
on detecting additional defects, such as membrane thinning or
aggregation. Another direction is to integrate the pipeline with other
imaging methods, such as DLS or fluorescence microscopy.

# **Conclusion**

The goal of this work was to build a practical, scalable, and
scientifically grounded pipeline for analyzing liposomal drug
formulations using Cryo‑TEM images. Liposomes are simple in structure,
but their behavior in the body depends on many small physical details.
Their size, membrane thickness, lamellarity, and drug loading all
influence how they circulate, how they release the drug, and how
effective they are as therapeutic carriers. Because of this,
manufacturers need reliable ways to measure these properties during
production. Cryo‑TEM is one of the few imaging methods that can directly
visualize liposomes in their hydrated, near‑native state. But manual
analysis of Cryo‑TEM images is slow, subjective, and difficult to scale.
This creates a bottleneck in quality control.

The pipeline described in this paper addresses this problem by combining
human expertise, multimodal reasoning, and instance segmentation. The
human annotation interface provides high‑quality gold data. The JSON
format keeps the data organized and easy to parse. The multimodal
teacher model provides pseudo‑labels for unlabeled images. The Mask
R‑CNN student model performs instance segmentation and classification.
The pipeline measures detection accuracy, size distribution, and
encapsulation efficiency. These metrics provide a complete view of the
formulation.

The pipeline is grounded in the physics of Cryo‑TEM imaging. The
contrast between empty and loaded vesicles comes from mass‑thickness.
Loaded vesicles contain dense drug crystals that absorb more electrons.
This makes the core appear darker. Empty vesicles have a core with the
same density as the surrounding buffer. This difference in contrast is
consistent across images. It does not depend on staining or other
chemical treatments. It is a direct result of the physics of electron
scattering. This makes it a reliable feature for automated
classification.

The pipeline is also grounded in the biology of liposomal drug delivery.
The size of the vesicles influences how they circulate in the body. The
number of bilayers influences how the drug is released. Ruptured
vesicles indicate instability. Encapsulation efficiency reflects how
well the manufacturing process traps the drug. These biological
principles shape the design of the pipeline. They determine which
features are important and which metrics matter.

The comparison to the metallurgy pipeline shows how different physical
principles shape the design of AI systems. Metallurgy relies on
diffraction contrast and thin, winding grain boundaries. Liposome
analysis relies on mass‑thickness contrast and circular vesicles. These
differences influence the choice of model architecture, the labeling
process, and the quality metrics. The comparison highlights the
importance of understanding the underlying physics. Without this
understanding, it is easy to choose the wrong model or the wrong metric.

The pipeline supports manufacturing quality control by providing
quantitative measurements that are meaningful, repeatable, and easy to
interpret. Automated measurement reduces human bias and increases
throughput. It also provides a way to detect changes in the
manufacturing process. For example, a shift in the size distribution may
indicate a problem with the mixing conditions. A drop in encapsulation
efficiency may indicate a problem with the pH gradient. An increase in
ruptured vesicles may indicate mechanical stress. The pipeline provides
a way to detect these changes quickly.

The system is flexible and can be adapted to different types of vesicles
or imaging conditions. It provides a foundation for future work in
automated analysis of nanoscale structures. Future work could focus on
improving the teacher model, collecting more labeled data, or using more
advanced architectures. It could also focus on detecting additional
defects, such as membrane thinning or aggregation. Another direction is
to integrate the pipeline with other imaging methods, such as DLS or
fluorescence microscopy.

In summary, this work shows that AI can support high‑throughput quality
control of liposomal drug formulations. The combination of human
annotation, multimodal reasoning, and instance segmentation creates a
system that is accurate, scalable, and grounded in the physics of
Cryo‑TEM imaging. The pipeline provides quantitative measurements that
support regulatory requirements. It also shows how AI can bridge the gap
between noisy scientific images and practical manufacturing needs. The
system is a step toward reliable, automated analysis of liposomal drug
formulations and other nanoscale systems.

# References

Bojarski, M., et al. (2016). *End to end learning for self-driving
cars*. arXiv preprint arXiv:1604.07316.

Chapelle, O., Scholkopf, B., & Zien, A. (2006). *Semi-supervised
learning*. MIT Press.

He, K., Gkioxari, G., Dollár, P., & Girshick, R. (2017). Mask R-CNN. In
*Proceedings of the IEEE International Conference on Computer Vision*
(pp. 2961--2969).

Hinton, G., Vinyals, O., & Dean, J. (2015). *Distilling the knowledge in
a neural network*. arXiv preprint arXiv:1503.02531.

Lin, T. Y., et al. (2014). Microsoft COCO: Common objects in context. In
*European Conference on Computer Vision* (pp. 740--755). Springer.

Ronneberger, O., Fischer, P., & Brox, T. (2015). U-Net: Convolutional
networks for biomedical image segmentation. In *International Conference
on Medical Image Computing and Computer-Assisted Intervention* (pp.
234--241). Springer.

Sanh, V., Debut, L., Chaumond, J., & Wolf, T. (2019). *DistilBERT, a
distilled version of BERT: smaller, faster, cheaper and lighter*. arXiv
preprint arXiv:1910.01108.

Settles, B. (2009). *Active learning literature survey*. Computer
Sciences Technical Report 1648, University of Wisconsin-Madison.

Torchilin, V. P. (2005). Recent advances with liposomes as
pharmaceutical carriers. *Nature Reviews Drug Discovery*, 4(2),
145--160.

Xie, Q., et al. (2020). Self-training with noisy student improves
ImageNet classification. In *Proceedings of the IEEE/CVF Conference on
Computer Vision and Pattern Recognition* (pp. 10687--10698).
