
=========================================
 Model Description
=========================================

BDEW
~~~~

Using the demandlib you can create heat and electrical profiles by scaling the BDEW profiles to your desired annual demand.
The BDEW profiles are the standard load profiles from BDEW ... (heat?)

Heat Profiles
+++++++++++++

Heat profiles are created according to the approach described in the `BDEW guideline <https://www.enwg-veroeffentlichungen.de/badtoelz/Netze/Gasnetz/Netzbeschreibung/LF-Abwicklung-von-Standardlastprofilen-Gas-20110630-final.pdf>`_.

The method was originally established this `PhD Thesis at TU Munich <https://mediatum.ub.tum.de/doc/601557/601557.pdf>`_.

The approach for generating heat demand profiles is described in section 4.1 (Synthetic load profile approach).

.. math::

    Q_{day}(\theta) = KW \cdot h(\theta) \cdot F \cdot SF$

| **KW**: Kundenwert (customer value). Daily consumption of customer at :math:`\approx 8 \circ C`, depending on SLP type and Temperature timeseries.  
| **h**: h-Wert (h-value) , depending on SLP type and daily mean temperature.  
| **F**: Wochentagsfaktor (week day factor), depending on SLP type and day of the week.  
| **T**: Daily mean temperature 2 meters above the ground (simple mean or "geometric series", which means a weighted sum over the previous days). 
| **SF**: Stundenfaktor (hour factor)  

The geometric series approach is motivated for the situation of forecasting. I am not sure if this is still usefull when the
actual temperature at that day is known.

:math:`T = \frac{T_t + 0.5 \cdot T_{t-1} + 0.25 \cdot T_{t-2} + 0.125 \cdot T_{t-3}}{1 + 0.5 + 0.25 + 0.125})` 

Depending on the profile type, different coefficients A, B, C, D for the sigmoid function are used.

.. math::

   h(\theta) = \frac{A}{1+(\frac{B}{\theta-\theta_0})^C} + D

   \theta_0 = 40^\circ C

Types of houses:

| EFH: Einfamilienhaus (single family house)
| MFH: Mehrfamilienhaus (multi family house)
| GMK: Metall und Kfz (Metal)
| GHA: Einzel- und Großhandel
| GKO: Gebietskörperschaften, Kreditinstitute und Versicherungen
| GBD: sonstige betriebliche Dienstleistung
| GGA: Gaststätten
| GBH: Beherbergung
| GWA: Wäschereien, chemische Reinigungen
| GGB: Gartenbau
| GBA: Backstube
| GPD: Papier und Druck
| GMF: haushaltsähnliche Gewerbebetriebe
| GHD: Summenlastprofil G/H/D

Electrical Profiles
++++++++++++++++++++

The electrical profiles are the standard load profiles from BDEW. You can choose from H0, G0...G6 and L0...L3 (?) by defining an annual demand for any of these options.


Furter Profiles
~~~~~~~~~~~~~~~

We implemented further profiles (one until now) to represent further demand sectors which are not covered by the BDEW load profiles.

Industrial Electrical Profile
++++++++++++++++++++++++++++++

The industrial electrical profile uses a step function.
