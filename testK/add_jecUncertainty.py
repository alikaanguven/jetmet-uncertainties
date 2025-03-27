#!/usr/bin/env python
# from exampleModule import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


jecUncertAll_cpp = lambda: jecUncertProducerCpp("106X_upgrade2018_realistic_v16_L1v1",
                                                allUncerts)

fnames = ["/eos/vbc/experiments/cms/store/user/lian/CustomNanoAOD_v3/stop_M600_585_ct20_2018/output/out_NANOAODSIMoutput_0.root"]
p = PostProcessor(".", fnames, "", "", [jecUncertAll_cpp()], provenance=True)
p.run()