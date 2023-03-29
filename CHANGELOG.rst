Changelog
=========

v0.1.10 (?-?-?)
+++++++++++++++++++++++++

New features
############
*

Bug fixes
#########
*

Other changes
#############
*


v0.1.9 (2023-03-18)
+++++++++++++++++++++++++

*   Calculation of BDEW profiles was improved



v0.1.8 (2021-01-27)
+++++++++++++++++++++++++

Bug fixes
#########
*   FutureWarning for "dyn_function_h0" was raised instead of printed



v0.1.7 (2021-01-27)
+++++++++++++++++++++++++

New features
############
*   Add dynamic h0 profile calculation
    (The implementation is not optimised for performance.
    Thus, it is not used by default.)

Bug fixes
#########
*   Fix improper use of pandas.dataframe.merge
    (demandlib will now work with pandas>=1.2)

Other changes
#############
*   Update deprecated pd.datetime to datetime.datetime
*   Add (integration) tests and coverage as CI
*   Split BDEW profile generation into submodules



v0.1.6 (2019-01-30)
+++++++++++++++++++++++++

General
#######

* Update requirements
* Fix typos



v0.1.5 (2018-09-05)
+++++++++++++++++++++++++

New features
############

* Add function `get_normalized_bdew_profile(self)` to get a normalised profile. You could also use an annual_demand of one to get the same results.

Bug fixes
#########

* Fix y-label of the heat example plot.

Other changes
#############

* Make matplotlib optional in examples.



v0.1.4 (2018-05-30)
+++++++++++++++++++++++++

Code
####

 * fix temperature bug
 * fix Code style

Documentation
#############

 * Documentation improvements.



v0.1.1 (2016-11-30)
+++++++++++++++++++++++++

New features
############
* Examples callable by command-line script

Bug fixes
#########
* Path specs when installed via pip

Other changes
#############
* Fix versioning



0.1.0 (2016-10-04)
+++++++++++++++++++++++++

New features
############
* Implementation of BDEW synthetic load profiles
* Synthetic load profiles for heating sector
* Self-made industry demand profile similar to BDEW profiles
