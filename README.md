# MeteoAdriatic ARW Error Correction

### What is all about?
NWP models have forecast errors and that fact is unavoidable. There are multiple reasons for errors, such as unknown exact atmosphere state at model initialization, imperfect model dynamics and phyisics, non-linear behaviour of system and so on.

There are multiple ways we can address this problem and try to improve model forecast ability. As major forecast errors usually come from imperfect NWP model that does not resemble atmosphere in most precise way, forecast output usually has detectable bias that depends on system (atmosphere+surface) features at particular geographic area. For example, if model underpredicts maximum daily temperature at particular location during sunny day, it is often the case it will do similar underprediction in most if not all sunny days.

We believe that bias like this one is very easy to correct using machine learning system where we big dataset of meteorological data is given as input training data and observed errors as input solution data to the learning model. After such training, we hope that system will be able to predict NWP magnitudes of error in advance.