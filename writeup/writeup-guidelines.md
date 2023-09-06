# Writeup Guidelines

*These guidelines were largely adopted from the SAR-RARP50 challenge [HERE](https://www.synapse.org/#!Synapse:syn27618412/wiki/) and from the MICCAI 2021 Reproducibility Checklist.*

Each participating team should prepare their writeup following these guidelines. It is encouraged to include citations and links to source code repositories if applicable. If you have source code publicly available (e.g., GitHub, BitBucket), please provide the link to your source code accordingly.

Please make sure to include the following information.

* Title
* Authors
* Affiliations
* Type the following in the writeup as a separate paragraph before start of the main content. 

```
Registered Team Name: <type your team name here>
Do the members of the team listed above agree to make their submission public as part of the challenge archive?
<Type "Yes" or "No">
```
> [!NOTE]
> Only those registered teams that agree to make their submission public will have the opportunity to nominate co-authors on the challenge publication.

### Writeup sections and headings

Make sure to include the following sections in your writeup. 

#### Introduction
Please try to cover the following bullet points in your introduction:
* Briefly present the clinical motivation behind your work.
* Describe the used methods for the selected challenges (segmentation). Provide the reader with your intuition of how you approached the problems a/o any literature that supports your methods.
* Describe the differences between the submitted solution compared to others in the literature.
* What is the novelty of the method (if any)?

#### Methods and Results
This section should cover a full description of your methods to the point where a reader can reproduce them. Proposals must be well documented and include any references, data, visualizations, or other information that supports the validity of the algorithm. Make sure to provide a clear description of the mathematical setting, algorithm, and/or model

Please include the following for each step:
* Preprocessing steps:
    * Cropping strategy
    * Resampling method for anisotropic data
    * Intensity normalization method
    * Registration method for multi-sequence/modality data
* Network architecture details:
    * Pretraining (if allowed)
    * Layer details in each block/module
    * Number of parameters
    * Range of hyper-parameters
* Training:
    * Usage of outside/additional data (if allowed)
    * If not provided by challenge organizers: data split
    * Computing infrastructure (e.g., GPU name, number, memory)
    * Patch size and patch sampling strategy
    * Batch size
    * Optimizer, learning rate and its decay schedule
    * Loss function
    * Data augmentation methods including all hyperparameters
    * Stopping criteria, and optimal model selection criteria
    * Training/evaluation runs
    * Training time
* Testing steps:
    * If using patch-based strategy, describe the patch aggregation method
    * Inference time
* Postprocessing steps

Please cover the following points when describing your methods and results:
* Describe the employed methodology in detail. A figure including the flow diagram of the overall framework is highly encouraged.
* Provide extended forms of shortened acronyms at least once.
* Describe the choice behind variables a/o hyperparameters as well as any pre-trained model used.
* Describe any publicly available data used apart from the challenge dataset.
* Describe the type of data manipulations, augmentation or pre-processing performed.
* (Optional) Include any preliminary results that motivate your methodology design choices.

#### Discussion and Conclusions
* Provide a summary of the challenge submission with a discussion around the design choices. 
* Include any preliminary results that can support the submission. 
* Provide a discussion of the strengths and weaknesses of the challenge submission (cases where the method is likely to work best/worst). 
* Finally, provide a brief insight into the future directions that could be followed to improve the author's model performances.