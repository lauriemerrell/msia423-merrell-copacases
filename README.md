# MSiA423 Template Repository

<!-- toc -->

- [Project charter](#project-charter)
    * [Vision](#vision)
    * [Mission](#mission)
    * [Success criteria](#success-criteria)
- [Directory structure](#directory-structure)
- [Mid-Project PR Instructions](#mid-project-pr)
  * [Data acquisition and database creation - overall structure](#overall-structure)
  * [Running data acquisition and database creation locally](#running-data-acquisition-and-database-creation-locally)
  * [Running data acquisition and database creation in Docker](#running-data-acquisition-and-database-creation-in-docker)

<!-- tocstop -->

# Chicago Civilian Office of Police Accountability Case Outcome Prediction Project


**Developer**: Laurie Merrell

**QA**: Joe Baka

## Project charter

### Vision

Accountability is an important component of the relationship between police departments and the communities in which they operate. One important aspect of this accountability is provided by oversight boards which hear complaints of alleged misconduct by police officers and provide rulings on the merits of these complaints (whether or not they are justified). In Chicago, the Civilian Office of Police Accountability ([COPA](https://www.chicagocopa.org/)) serves this function by hearing cases and deciding whether misconduct occurred (for more information, see COPA's [reference page on the investigative process](https://www.chicagocopa.org/investigations/investigative-process/)). For the public in Chicago to have additional oversight of this process, particularly in the current climate of fraught relationships between police departments and many communities (especially Black communities), it would be useful to have insight on whether complainants of certain races or certain ages are more or less likely to receive favorable outcomes in their complaints than others. This information could help COPA examine its own outcomes for potential bias, and it could assist journalists, activists, and members of the public who are seeking insight into how the police accountability infrastructure in Chicago operates. 

### Mission

To achieve the outcomes outlined above, we will create a tool which provides a predicted probability of judgment outcomes based on basic attributes of the case, including demographic attributes of the complainant, the type of the complaint, and demographic attributes of the officers included on the complaint. The model driving this tool will be built using the [COPA Cases dataset](https://data.cityofchicago.org/Public-Safety/COPA-Cases-Summary/mft5-nfa8) from the [Chicago Data Portal](https://data.cityofchicago.org/). The final model must be highly explainable (since the primary audiences for its output are nontechnical and the goal is transparency), so logistic regression and tree-based models will be favored (tree-based methods are also most analytically appropriate since all the predictors are categorical.)

### Success Criteria

We will have three primary success criteria:

- **Model performance**: At this point, we do not have an a priori reason to weight false negatives or false positives differently, so we will plan to use overall accuracy as our model evaluation criterion. However, if we investigate the data and see significant class imbalances which would make accuracy an unreliable indicator, we may have to re-evaluate this. Our baseline goal is to surpass the accuracy of a fully-random model (i.e., do better than just predicting the majority class for all cases.) Once we investigate the data further we may be able to refine this target; however, since the goal is mostly about transparency, we think that if models are not achieving very impressive accuracy we can report this in detail in our public-facing tool, and that will still provide value. 

- **Business value**: The "business" value of this project would be provided if it is deemed a useful tool for COPA, journalists, activists, or the public. Therefore, a long-term goal would be seeing this tool cited in a news article or cited in a context like a city council hearing related to the performance of COPA.

- **User-friendliness**: To achieve the "business" goals of this project, this tool must be very easy to use and interpret for nontechnical audiences (and since we are unlikely to achieve the business goals, this can perhaps serve as a proxy for likeliness to be adopted). Therefore, this tool must adhere very strongly to the (i.e., pass all criteria of) [Nielsen usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) and be simple and intuitive to use. The user should be able to select different combinations of characteristics for a case and see the probability of each possible case outcome for that combination of characteristics, and they should be able to do so without any explanation or training which is not immediately available within the tool's user interface. 

