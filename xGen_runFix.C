#include <stdio.h>
#include <iostream>

// Options to run the program:      scenario     num      den
//---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// + cmsRun fitMuon_2016DTLeg1.py   Nominal      HZgtrg   HZZid   &> logDT2016_leg1_nominal.txt &     //nominal
// + cmsRun fitMuon_2016DTLeg1.py   MassUp       HZgtrg   HZZid   &> logDT2016_leg1_massup.txt &      //change mass range
// + cmsRun fitMuon_2016DTLeg1.py   NbinDown     HZgtrg   HZZid   &> logDT2016_leg1_bindown.txt &     //change bins down
// + cmsRun fitMuon_2016DTLeg1.py   NbinUp       HZgtrg   HZZid   &> logDT2016_leg1_binup.txt &       //change bins up
// + cmsRun fitMuon_2016DTLeg1.py   AltSig       HZgtrg   HZZid   &> logDT2016_leg1_altsig.txt &      //change signal Pdf
// + cmsRun fitMuon_2016DTLeg1.py   AltBkg       HZgtrg   HZZid   &> logDT2016_leg1_altbkg.txt &      //change Bkg shape

// List of scenario
//---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// + Nominal
// + MassUp
// + NbinDown
// + NbinUp
// + AltSig
// + AltBkg

void  xGen_runFix (bool isData,  int setScenario,  int setYear,  int setLeg,  int setPt)
{
	TString scenario[6] =
	{
		"Nominal",
		"MassUp",
		"NbinDown",
		"NbinUp",
		"AltSig",
		"AltBkg"
	};
	
	TString chooseData[2] =
	{
		"MC",
		"DT"
	};
	
	system (Form("mkdir -p  Log_Fix%s", scenario[setScenario-1].Data()));
	system (Form("mkdir -p  Run_Fix%s", scenario[setScenario-1].Data()));
	
	
	TString name_filesh;
	if (isData == true)
	{
		name_filesh = Form("Run_Fix%s/runFixFitMuon%s_%d_Leg%d_%s.sh", scenario[setScenario-1].Data(), chooseData[isData].Data(), setYear, setLeg, scenario[setScenario-1].Data());
	}
	else
	{
		name_filesh = Form("Run_Fix%s/runFixFitMuon%s_%d_Leg%d_%s.sh", scenario[setScenario-1].Data(), chooseData[isData].Data(), setYear, setLeg, scenario[setScenario-1].Data());
	}
	
	FILE *file_sh = fopen (name_filesh, "w");
	
	if (setLeg == 1)
	{
		
		fprintf (file_sh, "cmsRun fitMuon%s.py   %s   HZgtrg   HZZid   %d   %d   %d\n", chooseData[isData].Data(), scenario[setScenario-1].Data(), setYear, setLeg, setPt);
	}
	else
	{
		fprintf (file_sh, "cmsRun fitMuon%s.py   %s   HZgtrg   HZZid   %d   %d   %d\n", chooseData[isData].Data(), scenario[setScenario-1].Data(), setYear, setLeg, setPt);
	}
	
	fclose (file_sh);
	
	
	
	
	system (Form("chmod 777  Run_%s/runFitMuon*sh", scenario[setScenario-1].Data()));
}
