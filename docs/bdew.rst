==================
BDEW Load Profiles
==================

Using the demandlib you can create heat and electrical profiles by scaling the BDEW profiles to your desired annual demand.
The BDEW profiles are the standard load profiles from BDEW.

Heat Profiles
~~~~~~~~~~~~~

Description
+++++++++++

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

Building class:

The parameter ``building_class`` (German: Baualtersklasse) can assume values in range 1-11.
See page 42 of `this document <https://www.eko-netz.de/files/eko-netz/download/3.5_standardlastprofile_bgw_information_lastprofile.pdf>`_ for guidance on how to determine ``building_class``.

You can either use the building class of 11 for Germany according to table 3 in the linked document, the ``building_class`` assigned to German federal states in table 3:

    ========================= =====================================
    Federal state                    Building class
    ========================= =====================================
    Baden-Württemberg           4
    Bayern                      5
    Berlin                      3
    Brandenburg                 5
    Bremen                      1
    Hamburg                     2
    Hessen                      3
    Mecklenburg-Vorpommern      6
    Niedersachsen               3
    Nordrhein-Westfalen         3
    Rheinland-Pfalz             4
    Saarland                    2
    Sachsen                     4
    Sachsen-Anhalt              5
    Schleswig-Holstein          4
    Thüringen                   5
    ========================= =====================================

or determine ``building_class`` on your own by identifying the proportion of buildings with a building age prior to 1978 and a building age of 1979 or later in the total building stock
and matching the proportion prior to 1978 with the span given in the column "Altbauanteil" in table 2 of the linked document.

Usage
+++++

Electrical Profiles
~~~~~~~~~~~~~~~~~~~

Description
+++++++++++

The electrical profiles are the standard load profiles from BDEW. All profiles
have a resolution of 15 minutes. They are based on measurements in the German
electricity sector. There is a dynamic function (h0_dyn) for the houshold (h0)
profile that better takes the seasonal variance into account.

.. math::

    F_t = -3,92\cdot10^{-10} \cdot t^4 + 3,2\cdot10^{-7} \cdot t^3– 7,02\cdot10^{-5}\cdot t^2 + 2,1\cdot10^{-3}\cdot t + 1,24

With `t` the day of the year as a decimal number.

The following profile types are available.
Be aware that the types in Python code are strings in **lowercase**.

.. csv-table:: German (original)
   :header: Typ,Beschreibung,Erläuterung
   :widths: 10, 40, 50

    G0, "Gewerbe allgemein", "Gewogener Mittelwert der Profile G1-G6"
    G1, "Gewerbe werktags 8–18 Uhr", "z.B. Büros, Arztpraxen, Werkstätten, Verwaltungseinrichtungen"
    G2, "Gewerbe mit starkem bis überwiegendem Verbrauch in den Abendstunden","z.B. Sportvereine, Fitnessstudios, Abendgaststätten"
    G3, "Gewerbe durchlaufend", "z.B. Kühlhäuser, Pumpen, Kläranlagen"
    G4, "Laden/Friseur",
    G5, "Bäckerei mit Backstube",
    G6, "Wochenendbetrieb", "z.B. Kinos"
    G7, "Mobilfunksendestation", "durchgängiges Bandlastprofil"
    L0, "Landwirtschaftsbetriebe allgemein", "Gewogener Mittelwert der Profile L1 und L2"
    L1, "Landwirtschaftsbetriebe mit Milchwirtschaft/Nebenerwerbs-Tierzucht",
    L2, "Übrige Landwirtschaftsbetriebe",
    H0/H0_dyn, "Haushalt/Haushalt dynamisiert",


.. csv-table:: British English (translation)
   :header: type, description, explanation
   :widths: 10, 40, 50

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
    H0/H0_dyn, "Household/dynamic houshold",


Further information in German language is available at the
`BDEW <https://www.bdew.de/energie/standardlastprofile-strom/>`_.

Usage
+++++

.. code-block:: python

    from demandlib import bdew
