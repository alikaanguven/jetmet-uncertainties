#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
# soon to be deprecated
# new way of using jme uncertainty


# Function parameters
# (isMC=True, dataYear=2016, runPeriod="B", jesUncert="Total", redojec=False, jetType = "AK4PFchs", noGroom=False)
# All other parameters will be set in the helper module

jmeCorrections = createJMECorrector(
    True, "2016", "B", "Total", "AK4PFchs", False)

fnames = ["/eos/vbc/experiments/cms/store/user/lian/CustomNanoAOD_v3/stop_M600_585_ct20_2018/output/out_NANOAODSIMoutput_0.root"]

# p=PostProcessor(".",fnames,"Jet_pt>150","",[jetmetUncertainties2016(),exampleModuleConstr()],provenance=True)
p = PostProcessor(".", fnames, "Jet_pt>150", "", [
                  jmeCorrections(), exampleModuleConstr()], provenance=True)
p.run()
