
=========================================
 Model Description
=========================================

BDEW
~~~~

Using the demandlib you can create heat and electrical profiles by scaling the BDEW profiles to your desired annual demand.
The BDEW profiles are the standard load profiles from BDEW.

Heat Profiles
+++++++++++++

Heat profiles are created according to the approach described in the `BDEW guideline <https://www.enwg-veroeffentlichungen.de/badtoelz/Netze/Gasnetz/Netzbeschreibung/LF-Abwicklung-von-Standardlastprofilen-Gas-20110630-final.pdf>`_.

The method was originally established in this `PhD Thesis at TU Munich <https://mediatum.ub.tum.de/doc/601557/601557.pdf>`_.

The approach for generating heat demand profiles is described in section 4.1 (Synthetic load profile approach).

.. math::
    Q_{day}(\theta) = KW \cdot h(\theta) \cdot F \cdot SF

| **KW**: Kundenwert (customer value). Daily consumption of customer at :math:`\approx 8 ^\circ C`, depending on SLP type and Temperature timeseries.
| **h**: h-Wert (h-value) , depending on SLP type and daily mean temperature.
| **F**: Wochentagsfaktor (week day factor), depending on SLP type and day of the week.
| **T**: Daily mean temperature 2 meters above the ground (simple mean or "geometric series", which means a weighted sum over the previous days).
| **SF**: Stundenfaktor (hour factor)

The geometric series approach is meant to account for thermal inertia.

.. math::
   \theta = \frac{T_t + 0.5 \cdot T_{t-1} + 0.25 \cdot T_{t-2} + 0.125 \cdot T_{t-3}}{1 + 0.5 + 0.25 + 0.125}

Depending on the profile type, different coefficients A, B, C, D for the sigmoid function are used.

.. math::
   h(\theta) &= \frac{A}{1+(\frac{B}{\theta-\theta_0})^C} + D \\
   \theta_0 &= 40^\circ C

Types of houses:

| **EFH**: Einfamilienhaus (single family house)
| **MFH**: Mehrfamilienhaus (multi family house)
| **GMK**: Metall und Kfz (metal and automotive)
| **GHA**: Einzel- und Großhandel (retail and wholesale)
| **GKO**: Gebietskörperschaften, Kreditinstitute und Versicherungen (Local authorities, credit institutions and insurance companies)
| **GBD**: sonstige betriebliche Dienstleistung (other operational services)
| **GGA**: Gaststätten (restaurants)
| **GBH**: Beherbergung (accommodation)
| **GWA**: Wäschereien, chemische Reinigungen (laundries, dry cleaning)
| **GGB**: Gartenbau (horticulture)
| **GBA**: Backstube (bakery)
| **GPD**: Papier und Druck (paper and printing)
| **GMF**: haushaltsähnliche Gewerbebetriebe (household-like business enterprises)
| **GHD**: Summenlastprofil Gewerbe/Handel/Dienstleistungen (Total load profile Business/Commerce/Services)

Electrical Profiles
++++++++++++++++++++

The electrical profiles are the standard load profiles from BDEW. You can choose from the following types:

.. csv-table:: German (original)
   :header: Typ,Beschreibung,Erläuterung
   :widths: 5, 10, 20

    G0, "Gewerbe allgemein", "Gewogener Mittelwert der Profile G1-G6"
    G1, "Gewerbe werktags 8–18 Uhr", "z.B. Büros, Arztpraxen, Werkstätten, Verwaltungseinrichtungen"
    G2, "Gewerbe mit starkem bis überwiegendem Verbrauch in den Abendstunden", "z.B. Sportvereine, Fitnessstudios, Abendgaststätten"
    G3, "Gewerbe durchlaufend", "z.B. Kühlhäuser, Pumpen, Kläranlagen"
    G4, "Laden/Friseur",
    G5, "Bäckerei mit Backstube",
    G6, "Wochenendbetrieb", "z.B. Kinos"
    G7, "Mobilfunksendestation", "durchgängiges Bandlastprofil"
    L0, "Landwirtschaftsbetriebe allgemein", "Gewogener Mittelwert der Profile L1 und L2"
    L1, "Landwirtschaftsbetriebe mit Milchwirtschaft/Nebenerwerbs-Tierzucht",
    L2, "Übrige Landwirtschaftsbetriebe",
    H0, "Haushalt",

I am not sure how to translate `"Gewerbe"` -> business, commerce, trade ?

.. csv-table:: British English (translation)
   :header: type, description, explanation
   :widths: 5, 10, 20

    G0, "General trade/business/commerce", "Weighted average of profiles G1-G6"
    G1, "Business on weekdays 8 a.m. - 6 p.m.", "e.g. offices, doctors' surgeries, workshops, administrative facilities"
    G2, "Businesses with heavy to predominant consumption in the evening hours", "e.g. sports clubs, fitness studios, evening restaurants"
    G3, "Continuous business", "e.g. cold stores, pumps, sewage treatment plants"
    G4, "Shop/barber shop"
    G5, "Bakery with bakery"
    G6, "Weekend operation", "e.g. cinemas"
    G7, "Mobile phone transmitter station", "continuous band load profile"
    L0, "General farms", "Weighted average of profiles L1 and L2"
    L1, "Farms with dairy farming/part-time livestock farming",
    L2, "Other farms",
    H0, "Household",


Further Profiles
~~~~~~~~~~~~~~~~

We implemented further profiles (one until now) to represent further demand sectors which are not covered by the BDEW load profiles.

Industrial Electrical Profile
++++++++++++++++++++++++++++++

The industrial electrical profile uses a step function.
