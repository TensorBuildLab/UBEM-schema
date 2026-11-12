# Competency questions answered from the catalog

Each question is executed by `meta_urban.analytics.competency()` over the YAML catalog.

**CQ1. Which open weather datasets give hourly or finer data for the United States at station or <= 1 km resolution?**  
wx-bsrn, wx-climate-onebuilding, wx-energyplus-weather, wx-noaa-isd

**CQ2. Which open geometry datasets give building-level polygons with height for the United States?**  
geo-3d-globfp, geo-ghs-obat, geo-globalbuildingatlas, geo-ms-global-footprints, geo-overture-buildings, geo-ut-globus

**CQ3. Which datasets are weighted samples, and which weights must be used?**  
chr-ahs (WEIGHT plus 160 replicate weights (REPWEIGHT1-REPWEIGHT160);...), chr-cbecs-2018 (FINALWT plus 151 replicate weights (FINALWT1-FINALWT151); va...), chr-recs-2020 (NWEIGHT plus 60 jackknife replicate weights (NWEIGHT1-NWEIGH...), ctx-acs (Published area estimates already apply the survey weights an...), occ-atus (TUFINLWGT (final weight, 2006-2019 and 2021 onward); TU06FWG...), occ-hetus (Not verified: microdata are access-restricted and the weight...), occ-uk-tus (Not verified: microdata are access-restricted and the weight...)

**CQ4. Which open datasets report measured energy at building or meter level?**  
nrg-ashrae-gepiii, nrg-bdg2, nrg-ideal, nrg-lead, nrg-london-lcl, nrg-plegma, nrg-redd, nrg-refit, nrg-smart-umass, nrg-uk-dale

**CQ5. Which building-characteristics datasets can be joined to a geometry dataset at building level?**  
chr-france-dpe, chr-nyc-ll84, chr-uk-epc, geo-cmab, geo-eubucco, geo-ghs-obat, geo-osm, geo-overture-buildings, geo-plateau  
_Building-level keys: address, building_id, geometry, lat_lon, parcel_id, ubid_

**CQ6. Which datasets lack an explicit license?**  
chr-bedes, chr-buildingsync, chr-doe-bpd, chr-doe-prototypes, chr-energy-codes-status, chr-eu-bso, chr-hotmaps, chr-nyc-ll84, chr-tabula-episcope, ctx-cambium, geo-china-rooftop-2023, geo-ghs-obat, nrg-ashrae-gepiii, nrg-ferc-714, nrg-lead, nrg-plegma, nrg-redd, occ-ashrae-ob-db, occ-ecobee-dyd, occ-hetus, sim-model-america, wx-argonne-future-weather, wx-bsrn, wx-energyplus-weather, wx-euro-cordex, wx-merra2, wx-na-cordex, wx-nasa-power, wx-noaa-isd, wx-noaa-normals, wx-nsrdb, wx-pvgis
