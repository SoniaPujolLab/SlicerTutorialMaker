import ctk
import qt

import slicer

from slicer.ScriptedLoadableModule import *
from Lib.TutorialUtils import Util
from slicer.i18n import translate

# Slicer4Minute

class Slicer4MinuteTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def findModelId(self, preferredModelId, logic=None):
        """
        Find a model ID with fallback support.
        If the exact model ID is not found, searches for the latest version with the same base name.
        
        Args:
            preferredModelId (str): The preferred model ID (e.g., "prostate-v1.0.1")
            logic: MONAIAuto3DSegLogic instance (optional, will create if not provided)
        
        Returns:
            str: The model ID to use (exact match or latest version fallback)
        
        Examples:
            >>> self.findModelId("prostate-v1.0.1")
            "prostate-v1.0.1"  # if exists
            "prostate-v1.0.2"  # if v1.0.1 doesn't exist but v1.0.2 does
        """
        if logic is None:
            import MONAIAuto3DSeg
            logic = MONAIAuto3DSeg.MONAIAuto3DSegLogic()
        
        # First, try to find exact match
        for model in logic.models:
            if model["id"] == preferredModelId:
                print(f"Model found: {preferredModelId}")
                return preferredModelId
        
        # If exact match not found, extract base name and find latest version
        # Example: "prostate-v1.0.1" -> base: "prostate"
        import re
        match = re.match(r"^(.+)-v\d+\.\d+\.\d+$", preferredModelId)
        if match:
            baseName = match.group(1)
            print(f"Exact model '{preferredModelId}' not found. Searching for latest '{baseName}' version...")
            
            # Find all models matching the base name
            matchingModels = []
            for model in logic.models:
                if model["id"].startswith(baseName + "-v"):
                    matchingModels.append(model)
            
            if matchingModels:
                # Sort by version (models are already sorted by version, first is latest)
                latestModel = matchingModels[0]
                print(f"Using fallback model: {latestModel['id']} (title: {latestModel['title']})")
                return latestModel["id"]
        
        # If still not found, raise an error
        raise ValueError(f"Model '{preferredModelId}' not found and no fallback available. Available models: {[m['id'] for m in logic.models[:5]]}...")
    
    def getModelSearchKeywords(self, modelId, logic=None):
        """
        Get translated search keywords from model title.
        Extracts 1-2 key words from the model's translated title to display in search box.
        
        Args:
            modelId (str): The model ID to get keywords for
            logic: MONAIAuto3DSegLogic instance (optional, will create if not provided)
        
        Returns:
            str: 1-2 key words from the translated model title
        
        Examples:
            >>> self.getModelSearchKeywords("prostate-v1.0.1")
            "Prostate"  # or translated version like "Próstata" in Portuguese
            >>> self.getModelSearchKeywords("brats-gli-v1.0.0")
            "Brain Tumor" or "BRATS GLI"
        """
        if logic is None:
            import MONAIAuto3DSeg
            logic = MONAIAuto3DSeg.MONAIAuto3DSegLogic()
        
        from slicer.i18n import translate
        
        # Find the model
        for model in logic.models:
            if model["id"] == modelId:
                # Get translated title
                translatedTitle = translate("Models", model["title"])
                
                # Extract meaningful keywords (skip common words like "segmentation", "quick", etc.)
                skipWords = ["segmentation", "quick", "-", "ts1", "ts2", "v1", "v2"]
                words = translatedTitle.split()
                keywords = []
                
                for word in words:
                    if word.lower() not in skipWords and len(word) > 2:
                        keywords.append(word)
                        if len(keywords) >= 2:  # Get first 2 meaningful words
                            break
                
                # Return keywords
                if keywords:
                    return " ".join(keywords)
                else:
                    # Fallback to first word of title
                    return words[0] if words else ""
        
        return ""

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear(0)

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_Slicer4Minute1()

    def test_Slicer4Minute1(self):
        """ Tests parts of the Slicer4Minute tutorial.
        """
        
        layoutManager = slicer.app.layoutManager()
        mainWindow = slicer.util.mainWindow()  
        
        self.delayDisplay("Starting the test")
        import os

        if not os.path.isfile(slicer.dicomDatabase.databaseFilename):  
            dicomBrowser = ctk.ctkDICOMBrowser()
            dicomBrowser.databaseDirectory = slicer.dicomDatabase.databaseDirectory
            dicomBrowser.createNewDatabaseDirectory()
            slicer.dicomDatabase.openDatabase(slicer.dicomDatabase.databaseFilename)

        # TUTORIALMAKER BEGIN
                
        # Pre-install PyTorch without user confirmation
        try:
            import PyTorchUtils
            torchLogic = PyTorchUtils.PyTorchUtilsLogic()
            if not torchLogic.torchInstalled():
                self.delayDisplay("Installing PyTorch... (may take a few minutes)")
                torchLogic.installTorch(askConfirmation=False, torchVersionRequirement=">=1.12")
        except Exception as e:
            print(f"Error installing PyTorch: {e}")
        
        # Now install MONAI and check dependencies
        import MONAIAuto3DSeg
        logic = MONAIAuto3DSeg.MONAIAuto3DSegLogic()
        logic.setupPythonRequirements(upgrade=False)
        self.delayDisplay("Dependencies installed successfully!")

        # Clear the scene to start fresh
        slicer.mrmlScene.Clear(0)
        
        # Close Data Probe if it's open
        try:
            # Find and close the Data Probe widget
            dataProbe = slicer.util.findChild(slicer.util.mainWindow(), 'DataProbeCollapsibleWidget')
            if dataProbe and dataProbe.collapsed == False:
                dataProbe.collapsed = True
        except:
            pass
        
        # TUTORIALMAKER INFO TITLE AIBasedSegmentationIn3DSlicer
        # TUTORIALMAKER INFO AUTHOR Sonia Pujol, Ph.D.
        # TUTORIALMAKER INFO DATE 30/06/2025
        # TUTORIALMAKER INFO DESC AI - based Segmentation in 3D Slicer
        # TUTORIALMAKER INFO DEPENDENCIES MONAIAuto3DSeg
        
        # 1 shot: 
        mainWindow.moduleSelector().selectModule('Welcome')
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #1: In the Welcome screen.')
    
        # 2 shot: 
        #addDataDialog=slicer.qSlicerDataDialog()
        #qt.QTimer.singleShot(0, lambda: addDataDialog.exec())
        
        #self.delayDisplay('Screenshot #2: Click in Add Data button')
        #ww = slicer.app.activeWindow()
        #ww.close()

        # 3 shot: Load protate data
        import urllib.request
        import zipfile

        # Caminho para salvar o ZIP e extrair
        zip_url = "https://www.dropbox.com/scl/fi/6wblo2a3gmxngbd0h4ums/SlicerData.zip?rlkey=bkp7g1pofcyd2zo7v3erihsl0&st=kxwp96l9&dl=1"
        zip_path = os.path.join(slicer.app.temporaryPath, "SlicerData.zip")
        extract_path = os.path.join(slicer.app.temporaryPath, "SlicerData")

        # Baixar ZIP se não existir
        if not os.path.exists(zip_path):
            urllib.request.urlretrieve(zip_url, zip_path)

        # Carregar os volumes
        prostate_folder = os.path.join(extract_path, "dataset3_ProstateMRI")
        adc_path = os.path.join(prostate_folder, "msd-prostate-01-adc.nrrd")
        t2_path = os.path.join(prostate_folder, "msd-prostate-01-t2.nrrd")

        # Extrair ZIP se não estiver extraído
        if not (os.path.exists(adc_path) and os.path.exists(t2_path)):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(slicer.app.temporaryPath)

        

        slicer.util.loadVolume(adc_path)
        slicer.util.loadVolume(t2_path)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #3: Load protate data')

        # 4 shot: Open module selector and select Segmentation
        combo = mainWindow.moduleSelector().findChildren(qt.QComboBox)[0]
        modMenu = combo.parent().children()[4]
        combo.showPopup()
        for mActions in modMenu.actions():
            if mActions.text == translate("qSlicerAbstractCoreModule","Segmentation") or mActions.text == "Segmentation":
                segAction = mActions
                modMenu.setActiveAction(segAction)
                mainWindow.moduleSelector().selectModule('MONAIAuto3DSeg')
                break
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #4: Auto3DSeg module selected')
        
        # 5 shot: Select Prostate segmentation model
        modMenu.close()
        
        # Use model ID instead of translated title for language-independent selection
        import MONAIAuto3DSeg
        logic = MONAIAuto3DSeg.MONAIAuto3DSegLogic()
        
        # Set the model directly by ID with fallback support
        modelId = self.findModelId("prostate-v1.0.1", logic)
        parameterNode = logic.getParameterNode()
        parameterNode.SetParameter("Model", modelId)
        
        # Set search box with translated keywords for visual feedback
        searchBox = slicer.util.findChild(slicer.util.mainWindow(), "modelSearchBox")
        searchKeywords = self.getModelSearchKeywords(modelId, logic)
        searchBox.setText(searchKeywords)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #6: Prostate model selected')

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #6: Prostate model selected and ready to run')

        # 7 shot: Start model and take screenshot
        nodeSelectorT2= slicer.util.findChild(slicer.util.mainWindow(), "inputNodeSelector0")
        nodeT2 = slicer.util.getNode("msd-prostate-01-t2")
        nodeSelectorT2.setCurrentNode(nodeT2)

        nodeSelectorAdc = slicer.util.findChild(slicer.util.mainWindow(), "inputNodeSelector1")
        nodeAdc = slicer.util.getNode("msd-prostate-01-adc")
        nodeSelectorAdc.setCurrentNode(nodeAdc)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #7: T2 input node selected')

        # 8 shot: Run model
        runButton = slicer.util.findChild(slicer.util.mainWindow(), "applyButton")
        runButton.click()
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #8: Model running')
        self.delayDisplay('Waiting for the model to finish...')
        
        import time
        segment_found = False
        max_wait_time = 300  # Maximum wait time in seconds (5 minutes)
        start_time = time.time()
        
        while not segment_found:
            # Process GUI events to prevent freezing
            slicer.app.processEvents()
            
            # Check for timeout
            if time.time() - start_time > max_wait_time:
                break
            
            try:
                segmentation_nodes = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')
                for seg_node in segmentation_nodes:
                    if seg_node.GetSegmentation().GetNumberOfSegments() > 0:
                        segment_names = [seg_node.GetSegmentation().GetNthSegment(i).GetName().lower() for i in range(seg_node.GetSegmentation().GetNumberOfSegments())]
                        if "prostate pz" in segment_names and "prostate tz" in segment_names:
                            segment_found = True
                            break
            except Exception as e:
                print(f"Error checking segments: {e}")
                pass
            
            # Small delay to prevent excessive CPU usage
            time.sleep(1)

        # 9 shot: Result
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #9: Model finished')

        ### BRAIN GLIOMA ###
        segmentation_nodes = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')
        for seg_node in segmentation_nodes:
            slicer.mrmlScene.RemoveNode(seg_node)

        # 1 shot: 
        # mainWindow.moduleSelector().selectModule('Welcome')
        # layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)    
        # addDataDialog=slicer.qSlicerDataDialog()
        # qt.QTimer.singleShot(0, lambda: addDataDialog.exec())
        # self.delayDisplay('Screenshot #1: Click in Add Data button')
        # ww = slicer.app.activeWindow()
        # ww.close()

        # 2 shot: Load BrainMRI_Glioma data

        brain_glioma_folder = os.path.join(extract_path, "dataset4_BrainMRI_Glioma")
        braTS_t1c_path = os.path.join(brain_glioma_folder, "BraTS-GLI-00006-000-t1c.nii.gz")
        braTS_t1n_path = os.path.join(brain_glioma_folder, "BraTS-GLI-00006-000-t1n.nii.gz")
        braTS_t2f_path = os.path.join(brain_glioma_folder, "BraTS-GLI-00006-000-t2f.nii.gz")
        braTS_t2w_path = os.path.join(brain_glioma_folder, "BraTS-GLI-00006-000-t2w.nii.gz")

        slicer.util.loadVolume(braTS_t1c_path)
        slicer.util.loadVolume(braTS_t1n_path)
        slicer.util.loadVolume(braTS_t2f_path)
        slicer.util.loadVolume(braTS_t2w_path)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #2: Load protate data')

        # 3 shot: Open module selector and select Segmentation
        mainWindow.moduleSelector().selectModule('MONAIAuto3DSeg')

        # Use model ID instead of translated title for language-independent selection with fallback
        modelId = self.findModelId("brats-gli-v1.0.0", logic)
        parameterNode.SetParameter("Model", modelId)
        
        # Set search box with translated keywords for visual feedback
        searchBox = slicer.util.findChild(slicer.util.mainWindow(), "modelSearchBox")
        searchKeywords = self.getModelSearchKeywords(modelId, logic)
        searchBox.setText(searchKeywords)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #3: Brain Tumor Segmentation (BRATS) GLI model selected and ready to run')

        # 4 shot: Select volume inputs
        nodeSelectorT2F= slicer.util.findChild(slicer.util.mainWindow(), "inputNodeSelector0")
        nodeT2F = slicer.util.getNode("BraTS-GLI-00006-000-t2f")
        nodeSelectorT2F.setCurrentNode(nodeT2F)
        
        nodeSelectorT1C= slicer.util.findChild(slicer.util.mainWindow(), "inputNodeSelector1")
        nodeT1C = slicer.util.getNode("BraTS-GLI-00006-000-t1c")
        nodeSelectorT1C.setCurrentNode(nodeT1C)
        
        nodeSelectorT1N= slicer.util.findChild(slicer.util.mainWindow(), "inputNodeSelector2")
        nodeT1N = slicer.util.getNode("BraTS-GLI-00006-000-t1n")
        nodeSelectorT1N.setCurrentNode(nodeT1N)
        
        nodeSelectorT2W= slicer.util.findChild(slicer.util.mainWindow(), "inputNodeSelector3")
        nodeT2W = slicer.util.getNode("BraTS-GLI-00006-000-t2w")
        nodeSelectorT2W.setCurrentNode(nodeT2W)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #4: Brain Tumor Segmentation (BRATS) GLI input node selected')       

        # 5 shot: Run model
        runButton = slicer.util.findChild(slicer.util.mainWindow(), "applyButton")
        runButton.click()
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #5: Model running')
        self.delayDisplay('Waiting for the model to finish...')
        
        import time
        segment_found = False
        max_wait_time = 300  # Maximum wait time in seconds (5 minutes)
        start_time = time.time()
        
        while not segment_found:
            # Process GUI events to prevent freezing
            slicer.app.processEvents()
            
            # Check for timeout
            if time.time() - start_time > max_wait_time:
                break
            
            try:
                segmentation_nodes = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')
                for seg_node in segmentation_nodes:
                    if seg_node.GetSegmentation().GetNumberOfSegments() > 0:
                        segment_names = [seg_node.GetSegmentation().GetNthSegment(i).GetName().lower() for i in range(seg_node.GetSegmentation().GetNumberOfSegments())]
                        if "necrosis" in segment_names:
                            segment_found = True
                            break
            except Exception as e:
                print(f"Error checking segments: {e}")
                pass
            
            # Small delay to prevent excessive CPU usage
            time.sleep(1)

        # 9 shot: Result
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #9: Model finished')

        ### WHOLE BODY ###
        segmentation_nodes = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')
        for seg_node in segmentation_nodes:
            slicer.mrmlScene.RemoveNode(seg_node)

        # 1 shot: 
        mainWindow.moduleSelector().selectModule('DICOM')
        ct_thorax_folder = os.path.join(extract_path, "dataset1_ThoraxAbdomenCT")
        
        import DICOMLib
        from DICOMLib import DICOMUtils
        
        dicomDatabase = slicer.dicomDatabase
        if not dicomDatabase:
            dicomDatabasePath = os.path.join(slicer.app.temporaryPath, "DICOMDatabase")
            if not os.path.exists(dicomDatabasePath):
                os.makedirs(dicomDatabasePath)
            
            dicomWidget = slicer.modules.dicom.widgetRepresentation().self()
            dicomWidget.onDatabaseDirectoryChanged(dicomDatabasePath)
            dicomDatabase = slicer.dicomDatabase
        
        self.delayDisplay('Importing DICOM files...')
        DICOMUtils.importDicom(ct_thorax_folder)
        
        import time
        time.sleep(2)
        slicer.app.processEvents()
        
        self.delayDisplay('Loading DICOM data...')
        dicomFiles = slicer.util.getFilesInDirectory(ct_thorax_folder)
        loadablesByPlugin, loadEnabled = DICOMLib.getLoadablesFromFileLists([dicomFiles])
        loadedNodeIDs = DICOMLib.loadLoadables(loadablesByPlugin)
        
        max_wait_time = 30
        start_time = time.time()
        ct_node = None
        
        while ct_node is None and (time.time() - start_time) < max_wait_time:
            slicer.app.processEvents()
            time.sleep(0.5)
            
            try:
                ct_node = slicer.util.getNode("6: CT_Thorax_Abdomen")
                if ct_node:
                    break
            except:
                volumeNodes = slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')
                for node in volumeNodes:
                    nodeName = node.GetName()
                    if 'CT_Thorax_Abdomen' in nodeName:
                        ct_node = node
                        break
        
        if ct_node is None:
            raise Exception("Failed to load DICOM data. Node '6: CT_Thorax_Abdomen' not found.")
        
        self.delayDisplay(f'DICOM data loaded: {ct_node.GetName()}')
        
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #1: DICOM module selected')

        # 2 shot: Open module selector and select Segmentation
        mainWindow.moduleSelector().selectModule('MONAIAuto3DSeg')
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView)    

        # Use model ID instead of translated title for language-independent selection with fallback
        modelId = self.findModelId("whole-body-3mm-v1.0.0", logic)
        parameterNode.SetParameter("Model", modelId)
        
        # Set search box with translated keywords for visual feedback
        searchBox = slicer.util.findChild(slicer.util.mainWindow(), "modelSearchBox")
        searchKeywords = self.getModelSearchKeywords(modelId, logic)
        searchBox.setText(searchKeywords)
        
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #3: Whole Body Segmentation (TS1 - quick) model selected and ready to run')

        # 3 shot: Select volume input
        nodeSelectorTc = slicer.util.findChild(slicer.util.mainWindow(), "inputNodeSelector0")
        nodeSelectorTc.setCurrentNode(ct_node)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #3: Volume input selected for Whole Body Segmentation (TS1 - quick)')

        # 4 shot: Run model
        runButton.click()
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #4: Model running')
        self.delayDisplay('Waiting for the model to finish...')
        
        import time
        segment_found = False
        max_wait_time = 300  # Maximum wait time in seconds (5 minutes)
        start_time = time.time()
        
        while not segment_found:
            # Process GUI events to prevent freezing
            slicer.app.processEvents()
            
            # Check for timeout
            if time.time() - start_time > max_wait_time:
                break
            
            try:
                segmentation_nodes = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')
                for seg_node in segmentation_nodes:
                    if seg_node.GetSegmentation().GetNumberOfSegments() > 0:
                        segment_names = [seg_node.GetSegmentation().GetNthSegment(i).GetName().lower() for i in range(seg_node.GetSegmentation().GetNumberOfSegments())]
                        if "urinary bladder" in segment_names:
                            segment_found = True
                            break
            except Exception as e:
                print(f"Error checking segments: {e}")
                pass
            
            # Small delay to prevent excessive CPU usage
            time.sleep(1)

        show3DButton = slicer.util.findChild(slicer.util.mainWindow(), "segmentationShow3DButton")
        show3DButton.toggle()
        
        threeDWidget = layoutManager.threeDWidget(0)
        threeDView = threeDWidget.threeDView()
        threeDView.rotateToViewAxis(3)  # look from anterior direction
        threeDView.resetFocalPoint()  # reset the 3D view cube size and center it
        threeDView.resetCamera()  # reset camera zoom
        time.sleep(1)

        # 5 shot: Result
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #5: Model finished')

        # Done
        # TUTORIALMAKER END
        self.delayDisplay('Test passed!')
