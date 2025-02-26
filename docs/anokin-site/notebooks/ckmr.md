# Close-kin Mark-Recapture?

## The Challenge: Understanding Mosquito Movement

One of the most significant gaps in our understanding of malaria vectors is surprisingly basic: we don't understand well how
 far the malaria mosquito can fly. This seemingly simple question has major implications for malaria control. Current estimates vary:

- Traditional studies suggest mosquitoes fly no more than 5km per generation
- Recent research in the [Sahel](https://doi.org/10.1038/s41586-019-1622-4) and western Kenya indicates mosquitoes may travel much further, carried by wind currents over extremely large distances

### Why This Matters
Understanding mosquito dispersal is crucial for several reasons:

1. **Vector Control Trials**: To effectively evaluate new control tools like spatial repellents and ATSBs, we need to design robust randomized controlled trials (RCTs). The distance mosquitoes can travel affects how we structure these trials.

2. **Gene Drive Implementation**: Gene drive technology shows promise for malaria control through either:
   - [Population suppression](https://doi.org/10.1038/nbt.4245)
   - Making vectors refractory to malaria transmission
   
   Large consortiums like Target Malaria and Zero Transmission are planning field trials in the near future. To model gene drive spread accurately, we must understand mosquito movement patterns.

3. **Insecticide Resistance**: The spread of insecticide resistance threatens current control methods, which are heavily reliant on insecticide use. Understanding how mosquitoes move helps us track and predict resistance spread.

## Close-Kin Mark-Recapture (CKMR)

### What is CKMR?
Close-kin mark-recapture is an advanced genomic technique that allows us estimate demographic parameters, such as dispersal rates and population size. It was originally developed for fisheries [(Bravington et al.  2016)](https://doi.org/10.1214/16-STS552). Instead of marking and releasing individual organisms, we:

1. Sample mosquitoes across a defined area
2. Sequence their genomes
3. Identify related individuals through their DNA
4. Use the geographic distance between related mosquitoes to estimate dispersal patterns

### Why CKMR?
CKMR offers several advantages over traditional methods:

- **Non-invasive**: No need to mark mosquitoes, which can affect their behavior
- **Comprehensive**: Can detect both short and long-distance movement
- **Additional insights**: Beyond dispersal, CKMR can reveal:
  - Census population size
  - Daily survivorship
  - Population dynamics


Whilst genomics is revolutionising vector surveillance, most advances have focused on monitoring insecticide resistance. AnoKin utilises genomics in a novel, innovative way to estimate dispersal rates.

## Project Implementation

### Study Site
We are conducting this work at Lake Kanyaboli, western Kenya, chosen for:
- High malaria transmission
- Stable *An. funestus* habitat
- Existing research infrastructure
- Well-characterized wind patterns

### Expected Outcomes
In conducting this project, we hope to provide:
1. Quantitative estimates of *An. funestus* dispersal distances and rates
2. Open-source software for analyzing close-kin genomic data
3. Improved design parameters for future intervention trials

## Looking Forward

The results from AnoKin will directly inform:
- Design of vector control trials
- Implementation of gene drive strategies
- Management of insecticide resistance

By filling this critical knowledge gap, we can better target our interventions and work more effectively toward malaria elimination.

