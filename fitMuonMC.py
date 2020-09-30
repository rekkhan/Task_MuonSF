import FWCore.ParameterSet.Config as cms
import sys, os, shutil
import array as arr
from optparse import OptionParser
### USAGE: cmsRun fitMuonID.py TEST tight loose mc mc_all
###_id: tight, loose, medium, soft

# Options to run the program:      scenario    num      den
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# + cmsRun fitMuon_2016DTLeg1.py   Nominal      HZgtrg   HZZid   &> logDT2016_leg1_nominal.txt &     //nominal
# + cmsRun fitMuon_2016DTLeg1.py   MassUp       HZgtrg   HZZid   &> logDT2016_leg1_massup.txt &      //change mass range
# + cmsRun fitMuon_2016DTLeg1.py   NbinDown     HZgtrg   HZZid   &> logDT2016_leg1_bindown.txt &     //change bins down
# + cmsRun fitMuon_2016DTLeg1.py   NbinUp       HZgtrg   HZZid   &> logDT2016_leg1_binup.txt &       //change bins up
# + cmsRun fitMuon_2016DTLeg1.py   AltSig       HZgtrg   HZZid   &> logDT2016_leg1_altsig.txt &      //change signal Pdf
# + cmsRun fitMuon_2016DTLeg1.py   AltBkg       HZgtrg   HZZid   &> logDT2016_leg1_altbkg.txt &      //change Bkg shape

print "\n\n\nProgram start\n"

# + Read the arguments
#=====================
args = sys.argv[1:]

scenario = ''
if len(args) > 1:   scenario = args[1]
print "The scenario is", scenario

num = 'tight'
if len(args) > 2:   num = args[2]
print 'The num is', num

den = 'tight'
if len(args) > 3:   den = args[3]
print 'The den is', den

setYear = 2016
if len(args) > 4:   setYear = args[4]

setLeg = 1
if len(args) > 5:   setLeg = args[5]

setPt = 1
if len(args) > 6:   setPt = args[6]
binPt = int(setPt)

print "processing Year: %d, Leg:%d, pTbin: %d\n" % (int(setYear), int(setLeg), binPt)


# + Read Inputs
#==============
def FillNumDen(num, den):
	'''Declares the needed selections for a givent numerator, denominator'''
	#Define the mass distribution
	if 'MassUp' in scenario:
		process.TnP_MuonID.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}")
		print 'SYSTEMATIC STUDIES: mass_up upper edge = 140 GeV'
	elif 'MassDown' in scenario:
		process.TnP_MuonID.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "120", "GeV/c^{2}")
		print 'SYSTEMATIC STUDIES: mass_up upper edge = 120 GeV'
	else:
		process.TnP_MuonID.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}")
	
	# + Define the trigger (Numerator)
	#---------------------------------
	# * Trigger for 2016:
	process.TnP_MuonID . Categories . DoubleIsoMu17Mu8_IsoMu17leg   = cms.vstring("DoubleIsoMu17Mu8_IsoMu17leg",   "dummy[pass=1, fail=0]")
	process.TnP_MuonID . Categories . DoubleIsoMu17TkMu8_IsoMu17leg = cms.vstring("DoubleIsoMu17TkMu8_IsoMu17leg", "dummy[pass=1, fail=0]")
	process.TnP_MuonID . Categories . DoubleIsoMu17Mu8dZ_Mu17leg    = cms.vstring("DoubleIsoMu17Mu8dZ_Mu17leg",    "dummy[pass=1, fail=0]")
	process.TnP_MuonID . Categories . DoubleIsoMu17Mu8_IsoMu8leg    = cms.vstring("DoubleIsoMu17Mu8_IsoMu8leg",    "dummy[pass=1, fail=0]")
	process.TnP_MuonID . Categories . DoubleIsoMu17TkMu8_IsoMu8leg  = cms.vstring("DoubleIsoMu17TkMu8_IsoMu8leg",  "dummy[pass=1, fail=0]")
	# * Trigger for 2017:
	process.TnP_MuonID . Categories . DoubleIsoMu17Mu8dZ_Mu17leg = cms.vstring("DoubleIsoMu17Mu8dZ_Mu17leg", "dummy[pass=1, fail=0]")
	process.TnP_MuonID . Categories . DoubleIsoMu17Mu8_IsoMu8leg = cms.vstring("DoubleIsoMu17Mu8_IsoMu8leg", "dummy[pass=1, fail=0]")
	# * Trigger for 2018:
	process.TnP_MuonID . Categories . DoubleIsoMu17Mu8dZ_Mu17leg = cms.vstring("DoubleIsoMu17Mu8dZ_Mu17leg", "dummy[pass=1, fail=0]")
	process.TnP_MuonID . Categories . DoubleIsoMu17Mu8_IsoMu8leg = cms.vstring("DoubleIsoMu17Mu8_IsoMu8leg", "dummy[pass=1, fail=0]")
	
	if int(setYear)==2016:
		if int(setLeg) == 1:
			process . TnP_MuonID . Expressions . mu_trg1 = cms.vstring(
				"mu_trg1",
				"DoubleIsoMu17Mu8_IsoMu17leg==1||DoubleIsoMu17TkMu8_IsoMu17leg==1||DoubleIsoMu17Mu8dZ_Mu17leg==1",
				"DoubleIsoMu17Mu8_IsoMu17leg", "DoubleIsoMu17TkMu8_IsoMu17leg", "DoubleIsoMu17Mu8dZ_Mu17leg")
			process.TnP_MuonID.Cuts.trg_leg1  = cms.vstring("trg_leg1", "mu_trg1", "0.5")
		elif int(setLeg) == 2:
			process.TnP_MuonID.Expressions.mu_trg2 = cms.vstring(
				"mu_trg2",
				"DoubleIsoMu17Mu8_IsoMu8leg==1||DoubleIsoMu17TkMu8_IsoMu8leg==1",
				"DoubleIsoMu17Mu8_IsoMu8leg", "DoubleIsoMu17TkMu8_IsoMu8leg")
			process.TnP_MuonID.Cuts.trg_leg2  = cms.vstring("trg_leg2", "mu_trg2", "0.5")
	elif int(setYear)==2017:
		if int(setLeg) == 1:
			process.TnP_MuonID.Expressions.mu_trg1 = cms.vstring(
				"mu_trg1",
				"DoubleIsoMu17Mu8dZ_Mu17leg==1",
				"DoubleIsoMu17Mu8dZ_Mu17leg")
			process.TnP_MuonID.Cuts.trg_leg1  = cms.vstring("trg_leg1", "mu_trg1", "0.5")
		elif int(setLeg) == 2:
			process.TnP_MuonID.Expressions.mu_trg2 = cms.vstring(
				"mu_trg2",
				"DoubleIsoMu17Mu8_IsoMu8leg==1",
				"DoubleIsoMu17Mu8_IsoMu8leg")
			process.TnP_MuonID.Cuts.trg_leg2  = cms.vstring("trg_leg2", "mu_trg2", "0.5")
	elif int(setYear)==2018:
		if int(setLeg) == 1:
			process.TnP_MuonID.Expressions.mu_trg1 = cms.vstring(
				"mu_trg1",
				"DoubleIsoMu17Mu8dZ_Mu17leg==1",
				"DoubleIsoMu17Mu8dZ_Mu17leg")
			process.TnP_MuonID.Cuts.trg_leg1  = cms.vstring("trg_leg1", "mu_trg1", "0.5")
		elif int(setLeg) == 2:
			process.TnP_MuonID.Expressions.mu_trg2 = cms.vstring(
				"mu_trg2",
				"DoubleIsoMu17Mu8_IsoMu8leg==1",
				"DoubleIsoMu17Mu8_IsoMu8leg")
			process.TnP_MuonID.Cuts.trg_leg2  = cms.vstring("trg_leg2", "mu_trg2", "0.5")
	
	# + Define ID cut (Denominator)
	#------------------------------
	process.TnP_MuonID.Variables.HZZid  = cms.vstring("HZZid", "-2","2", "")
	process.TnP_MuonID.Expressions.HZZidCutvar  = cms.vstring("HZZidCutvar", "HZZid>0.5","HZZid")
	process.TnP_MuonID.Cuts.HZZidcut = cms.vstring("HZZidCutvar","HZZidCutvar","0.5")



def FillVariables():
	# + Declares only the parameters which are necessary, no more
	#------------------------------------------------------------
	process.TnP_MuonID.Variables.pt      = cms.vstring("muon p_{T}", "0", "1000", "GeV/c")
	process.TnP_MuonID.Variables.abseta  = cms.vstring("muon #|eta|", "0", "2.5", "")




def FillBin():
	# + define the binning
	#---------------------
	bin_abseta = arr.array ('f', [0.0, 0.9, 1.2, 2.1, 2.4])
	# * Leg1
	bin_pt1 = arr.array ('f', [10, 15, 17, 20, 25, 30, 40, 50, 60, 120, 200])
	# * Leg2
	bin_pt2 = arr.array ('f', [5, 8, 10, 15, 20, 25, 30, 40, 50, 60, 120, 200])
	
	# + Sets the values of the bin paramters and the bool selections on the denominators
	#-----------------------------------------------------------------------------------
	# * Parameter
	DEN.abseta = cms.vdouble (0.0, 0.9, 1.2, 2.1, 2.4)
	if int(setLeg) == 1:   DEN.pt = cms.vdouble (bin_pt1[binPt], bin_pt1[binPt+1])
	if int(setLeg) == 2:   DEN.pt = cms.vdouble (bin_pt2[binPt], bin_pt2[binPt+1])
	# * Selections
	DEN.HZZid = cms.vdouble (0.5, 1.1)


process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )



if not num  in ['looseid', 'mediumid', 'tightid', 'HZgtrg']:
	print '@ERROR: num should be in ',['looseid', 'mediumid', 'tightid', 'HZgtrg'], 'You used', num, '.Abort'
	sys.exit()
if not den in ['HZZid','looseid', 'mediumid', 'tightid']:
	print '@ERROR: den should be',['HZZid','looseid', 'mediumid', 'tightid'], 'You used', den, '.Abort'
	sys.exit()




#_*_*_*_*_*_*_*_*_*_*_*_*
#Prepare variables, den, num and fit funct
#_*_*_*_*_*_*_*_*_*_*_*_*
# Set-up the mass lower edge
# For systematic uncertainties
if 'MassUp' in scenario:
	_mrange = "75"
	print 'SYSTEMATIC STUDIES: mass_up lower edge = 75 GeV'
elif 'MassDown' in scenario:
	_mrange = "65"
	print 'SYSTEMATIC STUDIES: mass_down lower edge = 65 GeV'
# For the nominal case
else:
	#For ID
	_mrange = "70"

print '_mrange is', _mrange
mass_ =" mass"



# nbins variation for systematics
if 'NbinUp' in scenario:
	#nbins = 50
	nbins = 70
elif 'NbinDown' in scenario:
	#nbins = 30
	nbins = 50
else:
	# nominal case
	#nbins = 40
	if 'MassUp' in scenario:
		nbins = 55
	else:
		nbins = 60


mymatrix = [[1, 2, 3], [4, 5, 6]]
print mymatrix[1][2]


# + Parameter for nominal function
#=================================
# * - Signal & Background Leg1
#-----------------------------
mean1_L1 = [[91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, -1],  [89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, -1],  [91.5, 91.5, 91.5, 91.5, 91.5, 91.5, 91.5, 91.5, 91.5, 91.5, -1]]
mean2_L1 = [[85.0, 86.0, 86.0, 87.0, 87.0, 87.0, 91.0, 91.5, 91.5, 92.5, -1],  [85.0, 85.0, 85.0, 85.0, 85.0, 85.0, 89.0, 89.0, 89.0, 89.0, -1],  [92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 94.0, 93.5, -1]]

sig1_L1 = [[1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, -1],  [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, -1],  [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, -1]]
sig2_L1 = [[2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 4.0, -1],  [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, -1],  [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, -1]]

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
aF_L1 = [[75.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, -1],  [65.0, 65.0, 70.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, -1],  [90.0, 95.0, 105.0, 85.0, 130.0, 130.0, 130.0, 130.0, 130.0, 130.0, -1]]
aP_L1 = [[75.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, -1],  [65.0, 65.0, 70.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, -1],  [90.0, 95.0, 105.0, 85.0, 130.0, 130.0, 130.0, 130.0, 130.0, 130.0, -1]]

bF_L1 = [[0.08, 0.15, 0.10, 0.10, 0.10, 0.15, 0.00, 0.00, 0.01, 0.01, -1],  [0.03, 0.03, 0.03, 0.01, 0.04, 0.04, 0.00, 0.00, 0.00, 0.00, -1],  [0.20, 0.20, 0.20, 0.20, 0.20, 0.15, 0.12, 0.12, 0.15, 0.15, -1]]
bP_L1 = [[0.08, 0.15, 0.10, 0.10, 0.10, 0.15, 0.00, 0.00, 0.01, 0.01, -1],  [0.03, 0.03, 0.03, 0.01, 0.04, 0.04, 0.00, 0.00, 0.00, 0.00, -1],  [0.20, 0.20, 0.20, 0.20, 0.20, 0.15, 0.12, 0.12, 0.15, 0.15, -1]]

gF_L1 = [[0.15, 0.15, 0.15, 0.10, 0.10, 0.10, 0.10, 0.00, 0.01, 0.01, -1],  [0.08, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -1],  [0.50, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, -1]]
gP_L1 = [[0.15, 0.15, 0.15, 0.10, 0.10, 0.10, 0.10, 0.00, 0.01, 0.01, -1],  [0.08, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, -1],  [0.50, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, -1]]

pF_L1 = [90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, -1]
pP_L1 = [90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, -1]

eff_L1 = [[0.01, 0.10, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90, -1],  [0.00, 0.00, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, -1],  [0.10, 0.70, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, -1]]

# * - Signal & Background Leg2
#-----------------------------
mean1_L2 = [[91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.5, 91.0],  [89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0],  [91.5, 91.5, 91.5, 91.5, 91.5, 91.5, 91.5, 91.5, 91.5, 92.0, 91.5]]
mean2_L2 = [[85.0, 86.0, 86.0, 87.0, 87.0, 86.0, 86.0, 91.5, 93.5, 92.5, 92.5],  [85.0, 85.0, 85.0, 85.0, 85.0, 85.0, 85.0, 89.0, 89.0, 89.0, 89.0],  [92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 94.5, 93.5, 94.0]]

sig1_L2 = [[1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 2.0],  [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],  [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]]
sig2_L2 = [[2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 5.5],  [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0],  [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0]]

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
aF_L2 = [[90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0],  [65.0, 65.0, 70.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 90.0],  [90.0, 95.0, 105.0, 85.0, 130.0, 130.0, 130.0, 130.0, 130.0, 130.0, 130.0]]
aP_L2 = [[90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0],  [65.0, 65.0, 70.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 65.0, 90.0],  [90.0, 95.0, 105.0, 85.0, 130.0, 130.0, 130.0, 130.0, 130.0, 130.0, 130.0]]

bF_L2 = [[0.08, 0.15, 0.10, 0.10, 0.10, 0.01, 0.01, 0.00, 0.01, 0.01, 0.01],  [0.03, 0.03, 0.03, 0.01, 0.04, 0.04, 0.00, 0.00, 0.00, 0.00, 0.00],  [0.20, 0.20, 0.20, 0.20, 0.20, 0.15, 0.15, 0.12, 0.12, 0.12, 0.12]]
bP_L2 = [[0.08, 0.15, 0.10, 0.10, 0.10, 0.01, 0.01, 0.00, 0.06, 0.01, 0.01],  [0.03, 0.03, 0.03, 0.01, 0.04, 0.04, 0.00, 0.00, 0.00, 0.00, 0.00],  [0.20, 0.20, 0.20, 0.20, 0.20, 0.15, 0.15, 0.12, 0.12, 0.12, 0.12]]

gF_L2 = [[0.15, 0.15, 0.15, 0.10, 0.10, 0.10, 0.10, 0.00, 0.01, 0.01, 0.01],  [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  [0.50, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60]]
gP_L2 = [[0.15, 0.15, 0.15, 0.10, 0.10, 0.10, 0.10, 0.00, 0.01, 0.01, 0.01],  [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  [0.50, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60]]

pF_L2 = [90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0]
pP_L2 = [90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0]

eff_L2 = [[0.01, 0.70, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90],  [0.00, 0.00, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65],  [0.20, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00]]



# + Parameter for alternative signal function (Exponential)
#==========================================================
# * - Only signal need to be defined
#-----------------------------------
mean_L1 = [[91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, -1],  [89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, -1],  [92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 91.5, -1]]
sig_L1 = [[1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, -1],  [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, -1],  [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, -1]]

mean_L2 = [[91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 91.0, 90.0],  [89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0, 89.0],  [92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 92.5, 91.5]]
sig_L2 = [[1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 2.5],  [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1.0],  [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0]]



# + Parameter for alternative background function (Exponential)
#==============================================================
# * - Only background need to be defined
#---------------------------------------
# * - - For Exponential background leg1
lF_L1 = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1],  [-0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -1],  [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, -1]]
lP_L1 = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1],  [-0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -1],  [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, -1]]

# * - - For Exponential background leg2
lF_L2 = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  [-0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1],  [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]]
lP_L2 = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  [-0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1],  [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]]


# * - - For Chebychev background leg1
a0F_L1 = [[0.50, 0.50, 0.90, 0.90, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, -1],  [0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, -1],  [0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, -1]]
a0P_L1 = [[0.50, 0.50, 0.90, 0.90, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, -1],  [0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, -1],  [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, -1]]

a1F_L1 = [[-0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -1],  [-0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -1],  [-0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -1]]
a1P_L1 = [[-0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -1],  [-0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -1],  [-0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -1]]

a2F_L1 = [[0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, -1],  [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, -1],  [0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, -1]]
a2P_L1 = [[0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, -1],  [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, -1],  [0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, -1]]

# * - - For Chebychev background leg2
a0F_L2 = [[0.50, 0.50, 0.90, 0.90, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50],  [0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30, 0.30],  [0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80]]
a0P_L2 = [[0.50, 0.50, 0.90, 0.90, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50],  [0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.80, 0.30],  [1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.80]]

a1F_L2 = [[-0.3, -0.3, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30],  [-0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40],  [-0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10]]
a1P_L2 = [[-0.3, -0.3, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30, -0.30],  [-0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40, -0.40],  [-0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10, -0.10]]

a2F_L2 = [[0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],  [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08],  [0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13]]
a2P_L2 = [[0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],  [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08],  [0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13]]



Template = cms.EDAnalyzer (
	"TagProbeFitTreeAnalyzer",
	SplitMode = cms.uint32(0),
	NumCPU = cms.uint32(8),
	SaveWorkspace = cms.bool(False),
	
	Variables = cms.PSet(
		weight = cms.vstring("weight","0","10","")
		),
	
	Categories = cms.PSet(),
	Expressions = cms.PSet(),
	Cuts = cms.PSet(),
	
	
	
	
	PDFs = cms.PSet(
		voigtPlusCMS = cms.vstring(
			"Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])".replace("mass",mass_),
			"RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
			"RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
			"efficiency[0.9,0.7,1]",
			"signalFractionInPassing[0.9]"
			),
		voigtPlusCMSbeta0p2 = cms.vstring(
			"Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])".replace("mass",mass_),
			"RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.001, 0.,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
			"RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.03, 0.02,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
			"efficiency[0.9,0.7,1]",
			"signalFractionInPassing[0.9]"
			),
		vpvPlusExpo = cms.vstring(
			"Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
			"Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])".replace("mass",mass_),
			"SUM::signal(vFrac[0.8,0,1]*signal2, signal1)",
			"Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])".replace("mass",mass_),
			"Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])".replace("mass",mass_),
			"efficiency[0.9,0,1]",
			"signalFractionInPassing[0.9]"
			),
		vpvPlusCheb = cms.vstring(
			"Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
			"Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
			"SUM::signal(vFrac[0.8,0.5,1]*signal2, signal1)",
			#par3
			"RooChebychev::backgroundPass(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})".replace("mass",mass_),
			"RooChebychev::backgroundFail(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})".replace("mass",mass_),
			"efficiency[0.9,0.7,1]",
			"signalFractionInPassing[0.9]"
			),
		
		
		# + Iteration: Nominal ====================
		vpv_CMS_L1 = cms.vstring(
			"Voigtian :: signal1 (mass, mean1[%f, %f, %f], width[2.495], sigma1[%f, %f, %f])" % (
				mean1_L1[0][binPt], mean1_L1[1][binPt], mean1_L1[2][binPt],
				sig1_L1[0][binPt],  sig1_L1[1][binPt],  sig1_L1[2][binPt]
				),
			"Voigtian :: signal2 (mass, mean2[%f, %f, %f], width[2.495], sigma2[%f, %f, %f])" % (
				mean2_L1[0][binPt], mean2_L1[1][binPt], mean2_L1[2][binPt],
				sig2_L1[0][binPt],  sig2_L1[1][binPt],  sig2_L1[2][binPt]
				),
			"RooCMSShape :: backgroundFail (mass, alphaFail[%f], betaFail[%f, %f, %f], gammaFail[%f, %f, %f], peakFail[%f])" % (
				aF_L1[0][binPt],
				bF_L1[0][binPt], bF_L1[1][binPt], bF_L1[2][binPt],
				gF_L1[0][binPt], gF_L1[1][binPt], gF_L1[2][binPt],
				pF_L1[binPt]
				),
			"RooCMSShape :: backgroundPass (mass, alphaPass[%f], betaPass[%f, %f, %f], gammaPass[%f, %f, %f], peakPass[%f])" % (
				aP_L1[0][binPt],
				bP_L1[0][binPt], bP_L1[1][binPt], bP_L1[2][binPt],
				gP_L1[0][binPt], gP_L1[1][binPt], gP_L1[2][binPt],
				pP_L1[binPt]
				),
			"SUM::signal(vFrac[0.4, 0.1, 1.0]*signal2, signal1)",
			"efficiency[%f, %f, %f]" % (eff_L1[0][binPt], eff_L1[1][binPt], eff_L1[2][binPt]),
			"signalFractionInPassing[0.9]"
			),
		
		vpv_CMS_L2 = cms.vstring(
			"Voigtian :: signal1 (mass, mean1[%f, %f, %f], width[2.495], sigma1[%f, %f, %f])" % (
				mean1_L2[0][binPt], mean1_L2[1][binPt], mean1_L2[2][binPt],
				sig1_L2[0][binPt],  sig1_L2[1][binPt],  sig1_L2[2][binPt]
				),
			"Voigtian :: signal2 (mass, mean2[%f, %f, %f], width[2.495], sigma2[%f, %f, %f])" % (
				mean2_L2[0][binPt], mean2_L2[1][binPt], mean2_L2[2][binPt],
				sig2_L2[0][binPt],  sig2_L2[1][binPt],  sig2_L2[2][binPt]
				),
			"RooCMSShape :: backgroundFail (mass, alphaFail[%f], betaFail[%f, %f, %f], gammaFail[%f, %f, %f], peakFail[%f])" % (
				aF_L2[0][binPt],
				bF_L2[0][binPt], bF_L2[1][binPt], bF_L2[2][binPt],
				gF_L2[0][binPt], gF_L2[1][binPt], gF_L2[2][binPt],
				pF_L2[binPt]
				),
			"RooCMSShape :: backgroundPass (mass, alphaPass[%f], betaPass[%f, %f, %f], gammaPass[%f, %f, %f], peakPass[%f])" % (
				aP_L2[0][binPt],
				bP_L2[0][binPt], bP_L2[1][binPt], bP_L2[2][binPt],
				gP_L2[0][binPt], gP_L2[1][binPt], gP_L2[2][binPt],
				pP_L2[binPt]
				),
			"SUM::signal(vFrac[0.4, 0.1, 1.0]*signal2, signal1)",
			"efficiency[%f, %f, %f]" % (eff_L2[0][binPt], eff_L2[1][binPt], eff_L2[2][binPt]),
			"signalFractionInPassing[0.9]"
			),
		
		vpv_CMS_L1_2016eta3pt9 = cms.vstring(
			"Voigtian::signal1(mass, mean1[91.5, 91.0, 92.5], width[2.495], sigma1[3.5, 2.0, 6.0])",
			"Voigtian::signal2(mass, mean2[91.5, 91.0, 92.5], width,        sigma2[3.5, 2.0, 6.0])",
			"RooCMSShape::backgroundPass(mass, alphaPass[90.0], betaPass[0.001, 0.0, 0.09], gammaPass[0.01, 0.0, 0.6], peakPass[90.0])",
			"RooCMSShape::backgroundFail(mass, alphaFail[90.0], betaFail[0.001, 0.0, 0.09], gammaFail[0.01, 0.0, 0.6], peakFail[90.0])",
			"SUM::signal(vFrac[0.4, 0.1, 1.0]*signal2, signal1)",
			"efficiency[0.9, 0.6, 1.0]",
			"signalFractionInPassing[0.9]"
			),
		
		vpv_CMS_L2_2016eta3pt10 = cms.vstring(
			"Voigtian::signal1(mass, mean1[91.5, 91.0, 92.5], width[2.495], sigma1[3.5, 2.0, 6.0])",
			"Voigtian::signal2(mass, mean2[91.5, 91.0, 92.5], width,        sigma2[3.5, 2.0, 6.0])",
			"RooCMSShape::backgroundPass(mass, alphaPass[90.0], betaPass[0.001, 0.0, 0.09], gammaPass[0.01, 0.0, 0.6], peakPass[90.0])",
			"RooCMSShape::backgroundFail(mass, alphaFail[90.0], betaFail[0.001, 0.0, 0.09], gammaFail[0.01, 0.0, 0.6], peakFail[90.0])",
			"SUM::signal(vFrac[0.4, 0.1, 1.0]*signal2, signal1)",
			"efficiency[0.9, 0.6, 1.0]",
			"signalFractionInPassing[0.9]"
			),
		
		
		
		# + Iteration: MassUp ====================
		
		
		
		# + Iteration: NbinDown ====================
		
		
		
		# + Iteration: NbinUp ====================
		
		
		
		# + Iteration: AltSig ====================
		voig_CMS_L1 = cms.vstring(
			"Voigtian :: signal (mass, mean1[%f, %f, %f], width[2.495], sigma1[%f, %f, %f])" % (
				mean_L1[0][binPt], mean_L1[1][binPt], mean_L1[2][binPt],
				sig_L1[0][binPt],  sig_L1[1][binPt],  sig_L1[2][binPt]
				),
			"RooCMSShape :: backgroundFail (mass, alphaFail[%f], betaFail[%f, %f, %f], gammaFail[%f, %f, %f], peakFail[%f])" % (
				aF_L1[0][binPt],
				bF_L1[0][binPt], bF_L1[1][binPt], bF_L1[2][binPt],
				gF_L1[0][binPt], gF_L1[1][binPt], gF_L1[2][binPt],
				pF_L1[binPt]
				),
			"RooCMSShape :: backgroundPass (mass, alphaPass[%f], betaPass[%f, %f, %f], gammaPass[%f, %f, %f], peakPass[%f])" % (
				aP_L1[0][binPt],
				bP_L1[0][binPt], bP_L1[1][binPt], bP_L1[2][binPt],
				gP_L1[0][binPt], gP_L1[1][binPt], gP_L1[2][binPt],
				pP_L1[binPt]
				),
			"efficiency[%f, %f, %f]" % (eff_L1[0][binPt], eff_L1[1][binPt], eff_L1[2][binPt]),
			"signalFractionInPassing[0.9]"
			),
		
		voig_CMS_L2 = cms.vstring(
			"Voigtian :: signal (mass, mean1[%f, %f, %f], width[2.495], sigma1[%f, %f, %f])" % (
				mean_L2[0][binPt], mean_L2[1][binPt], mean_L2[2][binPt],
				sig_L2[0][binPt],  sig_L2[1][binPt],  sig_L2[2][binPt]
				),
			"RooCMSShape :: backgroundFail (mass, alphaFail[%f], betaFail[%f, %f, %f], gammaFail[%f, %f, %f], peakFail[%f])" % (
				aF_L2[0][binPt],
				bF_L2[0][binPt], bF_L2[1][binPt], bF_L2[2][binPt],
				gF_L2[0][binPt], gF_L2[1][binPt], gF_L2[2][binPt],
				pF_L2[binPt]
				),
			"RooCMSShape :: backgroundPass (mass, alphaPass[%f], betaPass[%f, %f, %f], gammaPass[%f, %f, %f], peakPass[%f])" % (
				aP_L2[0][binPt],
				bP_L2[0][binPt], bP_L2[1][binPt], bP_L2[2][binPt],
				gP_L2[0][binPt], gP_L2[1][binPt], gP_L2[2][binPt],
				pP_L2[binPt]
				),
			"efficiency[%f, %f, %f]" % (eff_L2[0][binPt], eff_L2[1][binPt], eff_L2[2][binPt]),
			"signalFractionInPassing[0.9]"
			),
		
		
		
		# + Iteration: AltBkg ====================
		# * Chebyshev background
		vpv_Cheb_L1 = cms.vstring(
			"Voigtian :: signal1 (mass, mean1[%f, %f, %f], width[2.495], sigma1[%f, %f, %f])" % (
				mean1_L1[0][binPt], mean1_L1[1][binPt], mean1_L1[2][binPt],
				sig1_L1[0][binPt],  sig1_L1[1][binPt],  sig1_L1[2][binPt]
				),
			"Voigtian :: signal2 (mass, mean2[%f, %f, %f], width[2.495], sigma2[%f, %f, %f])" % (
				mean2_L1[0][binPt], mean2_L1[1][binPt], mean2_L1[2][binPt],
				sig2_L1[0][binPt],  sig2_L1[1][binPt],  sig2_L1[2][binPt]
				),
			"SUM::signal(vFrac[0.4, 0.1, 1.0]*signal2, signal1)",
			"RooChebychev :: backgroundPass (mass, {a0P[%f, %f, %f], a1P[%f, %f, %f], a2P[%f, %f, %f]})" % (
				a0P_L1[0][binPt], a0P_L1[1][binPt], a0P_L1[2][binPt],
				a1P_L1[0][binPt], a1P_L1[1][binPt], a1P_L1[2][binPt],
				a2P_L1[0][binPt], a2P_L1[1][binPt], a2P_L1[2][binPt]
				),
			"RooChebychev :: backgroundFail (mass, {a0F[%f, %f, %f], a1F[%f, %f, %f], a2F[%f, %f, %f]})" % (
				a0F_L1[0][binPt], a0F_L1[1][binPt], a0F_L1[2][binPt],
				a1F_L1[0][binPt], a1F_L1[1][binPt], a1F_L1[2][binPt],
				a2F_L1[0][binPt], a2F_L1[1][binPt], a2F_L1[2][binPt]
				),
			"efficiency[%f, %f, %f]" % (eff_L1[0][binPt], eff_L1[1][binPt], eff_L1[2][binPt]),
			"signalFractionInPassing[0.9]"
			),
		
		vpv_Cheb_L2 = cms.vstring(
			"Voigtian :: signal1 (mass, mean1[%f, %f, %f], width[2.495], sigma1[%f, %f, %f])" % (
				mean1_L2[0][binPt], mean1_L2[1][binPt], mean1_L2[2][binPt],
				sig1_L2[0][binPt],  sig1_L2[1][binPt],  sig1_L2[2][binPt]
				),
			"Voigtian :: signal2 (mass, mean2[%f, %f, %f], width[2.495], sigma2[%f, %f, %f])" % (
				mean2_L2[0][binPt], mean2_L2[1][binPt], mean2_L2[2][binPt],
				sig2_L2[0][binPt],  sig2_L2[1][binPt],  sig2_L2[2][binPt]
				),
			"SUM::signal(vFrac[0.4, 0.1, 1.0]*signal2, signal1)",
			"RooChebychev :: backgroundPass (mass, {a0P[%f, %f, %f], a1P[%f, %f, %f], a2P[%f, %f, %f]})" % (
				a0P_L2[0][binPt], a0P_L2[1][binPt], a0P_L2[2][binPt],
				a1P_L2[0][binPt], a1P_L2[1][binPt], a1P_L2[2][binPt],
				a2P_L2[0][binPt], a2P_L2[1][binPt], a2P_L2[2][binPt]
				),
			"RooChebychev :: backgroundFail (mass, {a0F[%f, %f, %f], a1F[%f, %f, %f], a2F[%f, %f, %f]})" % (
				a0F_L2[0][binPt], a0F_L2[1][binPt], a0F_L2[2][binPt],
				a1F_L2[0][binPt], a1F_L2[1][binPt], a1F_L2[2][binPt],
				a2F_L2[0][binPt], a2F_L2[1][binPt], a2F_L2[2][binPt]
				),
			"efficiency[%f, %f, %f]" % (eff_L2[0][binPt], eff_L2[1][binPt], eff_L2[2][binPt]),
			"signalFractionInPassing[0.9]"
			),
		
		vpv_Cheb_L1_2016eta3pt9 = cms.vstring(
			"Voigtian :: signal1 (mass, mean1[%f, %f, %f], width[2.495], sigma1[6.5, 2.5, 8.0])" % (
				mean1_L1[0][binPt], mean1_L1[1][binPt], mean1_L1[2][binPt]
				),
			"Voigtian :: signal2 (mass, mean2[%f, %f, %f], width[2.495], sigma2[6.5, 2.5, 8.0])" % (
				mean2_L1[0][binPt], mean2_L1[1][binPt], mean2_L1[2][binPt]
				),
			"SUM::signal(vFrac[0.4, 0.1, 1.0]*signal2, signal1)",
			"RooChebychev :: backgroundPass (mass, {a0P[%f, %f, %f], a1P[%f, %f, %f], a2P[%f, %f, %f]})" % (
				a0P_L1[0][binPt], a0P_L1[1][binPt], a0P_L1[2][binPt],
				a1P_L1[0][binPt], a1P_L1[1][binPt], a1P_L1[2][binPt],
				a2P_L1[0][binPt], a2P_L1[1][binPt], a2P_L1[2][binPt]
				),
			"RooChebychev :: backgroundFail (mass, {a0F[%f, %f, %f], a1F[%f, %f, %f], a2F[%f, %f, %f]})" % (
				a0F_L1[0][binPt], a0F_L1[1][binPt], a0F_L1[2][binPt],
				a1F_L1[0][binPt], a1F_L1[1][binPt], a1F_L1[2][binPt],
				a2F_L1[0][binPt], a2F_L1[1][binPt], a2F_L1[2][binPt]
				),
			"efficiency[%f, %f, %f]" % (eff_L1[0][binPt], eff_L1[1][binPt], eff_L1[2][binPt]),
			"signalFractionInPassing[0.9]"
			),
		
		vpv_Cheb_L2_2016eta3pt10 = cms.vstring(
			"Voigtian :: signal1 (mass, mean1[%f, %f, %f], width[2.495], sigma1[6.5, 2.5, 8.0])" % (
				mean1_L2[0][binPt], mean1_L2[1][binPt], mean1_L2[2][binPt]
				),
			"Voigtian :: signal2 (mass, mean2[%f, %f, %f], width[2.495], sigma2[6.5, 2.5, 8.0])" % (
				mean2_L2[0][binPt], mean2_L2[1][binPt], mean2_L2[2][binPt]
				),
			"SUM::signal(vFrac[0.4, 0.1, 1.0]*signal2, signal1)",
			"RooChebychev :: backgroundPass (mass, {a0P[%f, %f, %f], a1P[%f, %f, %f], a2P[%f, %f, %f]})" % (
				a0P_L2[0][binPt], a0P_L2[1][binPt], a0P_L2[2][binPt],
				a1P_L2[0][binPt], a1P_L2[1][binPt], a1P_L2[2][binPt],
				a2P_L2[0][binPt], a2P_L2[1][binPt], a2P_L2[2][binPt]
				),
			"RooChebychev :: backgroundFail (mass, {a0F[%f, %f, %f], a1F[%f, %f, %f], a2F[%f, %f, %f]})" % (
				a0F_L2[0][binPt], a0F_L2[1][binPt], a0F_L2[2][binPt],
				a1F_L2[0][binPt], a1F_L2[1][binPt], a1F_L2[2][binPt],
				a2F_L2[0][binPt], a2F_L2[1][binPt], a2F_L2[2][binPt]
				),
			"efficiency[%f, %f, %f]" % (eff_L2[0][binPt], eff_L2[1][binPt], eff_L2[2][binPt]),
			"signalFractionInPassing[0.9]"
			),
		
		# * Exponential background
		vpv_Exp_L1 = cms.vstring(
			"Voigtian :: signal1 (mass, mean1[%f, %f, %f], width[2.495], sigma1[%f, %f, %f])" % (
				mean1_L1[0][binPt], mean1_L1[1][binPt], mean1_L1[2][binPt],
				sig1_L1[0][binPt], sig1_L1[1][binPt],  sig1_L1[2][binPt]
				),
			"Voigtian :: signal2 (mass, mean2[%f, %f, %f], width[2.495], sigma2[%f, %f, %f])" % (
				mean2_L1[0][binPt], mean2_L1[1][binPt], mean2_L1[2][binPt],
				sig2_L1[0][binPt],  sig2_L1[1][binPt],  sig2_L1[2][binPt]
				),
			"SUM::signal(vFrac[0.4, 0.1, 0.6]*signal2, signal1)",
			"Exponential::backgroundPass(mass, lp[%f, %f, %f])" % (
				lP_L1[0][binPt], lP_L1[1][binPt], lP_L1[2][binPt]
				),
			"Exponential::backgroundFail(mass, lf[%f, %f, %f])" % (
				lF_L1[0][binPt], lF_L1[1][binPt], lF_L1[2][binPt]
				),
			"efficiency[%f, %f, %f]" % (eff_L1[0][binPt], eff_L1[1][binPt], eff_L1[2][binPt]),
			"signalFractionInPassing[0.9]"
			),
		
		vpv_Exp_L2 = cms.vstring(
			"Voigtian :: signal1 (mass, mean1[%f, %f, %f], width[2.495], sigma1[%f, %f, %f])" % (
				mean1_L2[0][binPt], mean1_L2[1][binPt], mean1_L2[2][binPt],
				sig1_L2[0][binPt],  sig1_L2[1][binPt],  sig1_L2[2][binPt]
				),
			"Voigtian :: signal2 (mass, mean2[%f, %f, %f], width[2.495], sigma2[%f, %f, %f])" % (
				mean2_L2[0][binPt], mean2_L2[1][binPt], mean2_L2[2][binPt],
				sig2_L2[0][binPt],  sig2_L2[1][binPt],  sig2_L2[2][binPt]
				),
			"SUM::signal(vFrac[0.4, 0.1, 0.6]*signal2, signal1)",
			"Exponential::backgroundPass(mass, lp[%f, %f, %f])" % (
				lP_L2[0][binPt], lP_L2[1][binPt], lP_L2[2][binPt]
				),
			"Exponential::backgroundFail(mass, lf[%f, %f, %f])" % (
				lF_L2[0][binPt], lF_L2[1][binPt], lF_L2[2][binPt]
				),
			"efficiency[%f, %f, %f]" % (eff_L2[0][binPt], eff_L2[1][binPt], eff_L2[2][binPt]),
			"signalFractionInPassing[0.9]"
			),
		),
	
	binnedFit = cms.bool(True),
	binsForFit = cms.uint32(nbins),
	saveDistributionsPlot = cms.bool(False),
	Efficiencies = cms.PSet(), # will be filled later
)


# + Define the input directories
#===============================
name_fileinput = ""
if int(setYear) == 2016:
	name_fileinput = "/home/hoa/Task_ScaleFactor/Input/tnpZ_withNVtxWeights16.root"
elif int(setYear) == 2017:
	name_fileinput = "/home/hoa/Task_ScaleFactor/Input/tnpZ_withNVtxWeights17.root"
elif int(setYear) == 2018:
	name_fileinput = "/home/hoa/Task_ScaleFactor/Input/tnpZ_withNVtxWeights18.root"

process.TnP_MuonID = Template.clone(
	InputFileNames     = cms.vstring (name_fileinput),
	InputTreeName      = cms.string ("fitter_tree"),
	InputDirectoryName = cms.string ("tpTree"),
	Efficiencies       = cms.PSet(),
	)


BIN = cms.PSet(
	)

print 'debug1'
Num_dic = {'HZgtrg':'HZgtrg', 'looseid':'LooseID', 'mediumid':'MediumID', 'tightid':'TightID'}
Den_dic = {'HZZid':'HZZid', 'looseid':'LooseID', 'mediumid':'MediumID', 'tightid':'TightIDandIPCut'}
Sel_dic = {'looseid':'LooseCutid', 'mediumid':'MediumCutid', 'tightid':'TightCutid'}
if int(setLeg) == 1:
	Sel_dic = {'HZgtrg':'trg_leg1', 'looseid':'LooseCutid', 'mediumid':'MediumCutid', 'tightid':'TightCutid'}
else:
	Sel_dic = {'HZgtrg':'trg_leg2', 'looseid':'LooseCutid', 'mediumid':'MediumCutid', 'tightid':'TightCutid'}
print 'debugSel'



FillVariables()
FillNumDen(num,den)
print num
print den
ID_BINS = [(Sel_dic[num],("NUM_%s_DEN_%s"%(Num_dic[num],Den_dic[den]),BIN))]
print 'debug5'
print Sel_dic[num]
print ("NUM_%s_DEN_%s"%(Num_dic[num],Den_dic[den]),BIN)


#_*_*_*_*_*_*_*_*_*_*_*
#Launch fit production
#_*_*_*_*_*_*_*_*_*_*_*
print ID_BINS
for ID, ALLBINS in ID_BINS:
	print 'debug1'
	X = ALLBINS[0]
	print X
	B = ALLBINS[1]
	_output = '/home/hoa/Task_ScaleFactor/Output/Efficiency/'
	if not os.path.exists(_output):
		print 'Creating', '/Efficiency/',', the directory where the fits are stored.'
		os.makedirs(_output)
	_output += 'MC_' + scenario
	if not os.path.exists(_output):
		os.makedirs(_output)
	module = process.TnP_MuonID.clone(OutputFileName = cms.string(_output + "/TnP%dleg%d_pt%d.root" % (int(setYear), int(setLeg), binPt)))
	
	
	DEN = B.clone(); num_ = ID;
	FillBin()
	
	
	# + How to fit each given bins by different function
	#---------------------------------------------------
	#                          General function              first bin     function for 1st bin            second bin     function for 2nd bin
	# * shape = cms.vstring(     "voigtPlusCMS",           "*pt_bin0*",          "voigtPlusCMS",          "*pt_bin1*",          "voigtPlusCMS")
	if scenario == 'Nominal':
		print 'SYSTEMATIC STUDIES: the signal function will be TWO voigtian + CMSshape'
		print 'den is', den
		print 'num_ is ', num
		if int(setLeg)==1:
			shape = cms.vstring("vpv_CMS_L1")
		elif int(setLeg)==2:
			shape = cms.vstring("vpv_CMS_L2")
	elif scenario == 'MassUp':
		print 'SYSTEMATIC STUDIES: the signal function will be TWO voigtian + CMSshape'
		print 'den is', den
		print 'num_ is ', num
		if int(setLeg)==1:
			shape = cms.vstring("vpv_CMS_L1")
		elif int(setLeg)==2:
			shape = cms.vstring("vpv_CMS_L2")
	elif scenario == 'NbinDown':
		print 'SYSTEMATIC STUDIES: the signal function will be TWO voigtian + CMSshape'
		print 'den is', den
		print 'num_ is ', num
		if int(setLeg)==1:
			shape = cms.vstring("vpv_CMS_L1")
		elif int(setLeg)==2:
			shape = cms.vstring("vpv_CMS_L2")
	elif scenario == 'NbinUp':
		print 'SYSTEMATIC STUDIES: the signal function will be TWO voigtian + CMSshape'
		print 'den is', den
		print 'num_ is ', num
		if int(setLeg)==1:
			shape = cms.vstring("vpv_CMS_L1")
		elif int(setLeg)==2:
			shape = cms.vstring("vpv_CMS_L2")
	elif scenario == 'AltSig':
		print 'SYSTEMATIC STUDIES: the signal function will be ONE voigtian + CMSshape'
		print 'den is', den
		print 'num_ is ', num
		if int(setLeg)==1:
			shape = cms.vstring("voig_CMS_L1")
		elif int(setLeg)==2:
			shape = cms.vstring("voig_CMS_L2")
	elif scenario == 'AltBkg':
		print 'SYSTEMATIC STUDIES: use CMS shape for background'
		if int(setLeg)==1:
			if binPt < 7:
				shape = cms.vstring("vpv_Exp_L1")
			else:
				shape = cms.vstring("vpv_Cheb_L1")
		elif int(setLeg)==2:
			if binPt < 8:
				shape = cms.vstring("vpv_Exp_L2")
			else:
				shape = cms.vstring("vpv_Cheb_L2")
	
	
	print 'd3'
	mass_variable ="mass"
	print 'den is', den
	
	# Compute isolation efficiency
	print 'd4'
	setattr(
		module.Efficiencies,
		ID+"_"+X,
		cms.PSet(
			EfficiencyCategoryAndState = cms.vstring(num_,"above"),
			UnbinnedVariables = cms.vstring(mass_variable),
			BinnedVariables = DEN,
			BinToPDFmap = shape
			)
		)
	print 'd5'
	setattr(process, "TnP_MuonID_"+ID+"_"+X, module)
	print 'd6'
	setattr(process, "run_"+ID+"_"+X, cms.Path(module))
	print 'd7'
	
	
	# PU reweighting applied for MC when par != vtx
	print 'the PU reweighting will be applied'
	
	setattr(
		module.Efficiencies,
		ID+"_"+X,
		cms.PSet(
			EfficiencyCategoryAndState = cms.vstring(num_,"above"),
			UnbinnedVariables = cms.vstring(mass_variable, "weight"),
			BinnedVariables = DEN,
			BinToPDFmap = shape
			)
		)
	print 'd5'
	setattr(process, "TnP_MuonID_"+ID+"_"+X, module)
	setattr(process, "run_"+ID+"_"+X, cms.Path(module))
