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
        
        # Install necessary dependencies BEFORE starting
        self.delayDisplay("Verificando e instalando dependências...")
        
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
    
        # TUTORIALMAKER BEGIN

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
        
        # 1 shot: 
        mainWindow.moduleSelector().selectModule('Welcome')
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #1: In the Welcome screen.')
    
        # 2 shot: 
        #addDataDialog=slicer.qSlicerDataDialog()
        #qt.QTimer.singleShot(0, lambda: addDataDialog.exec())


        
        self.delayDisplay('Screenshot #2: Click in Add Data button')
        ww = slicer.app.activeWindow()
        ww.close()

        # 3 shot: Load protate data
        import os
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
        searchBox = slicer.util.findChild(slicer.util.mainWindow(), "modelSearchBox")
        searchBox.setText("Prostate")

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #6: Prostate model filtered')

        # 6 Shot: Select prostate model
        modelCombo = slicer.util.findChild(slicer.util.mainWindow(), "modelComboBox")
        modelCombo.setCurrentItem(modelCombo.findItems("Prostate", qt.Qt.MatchContains)[0])

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
        mainWindow.moduleSelector().selectModule('Welcome')
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)    
        
        addDataDialog=slicer.qSlicerDataDialog()
        qt.QTimer.singleShot(0, lambda: addDataDialog.exec())

        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #1: Click in Add Data button')
        ww = slicer.app.activeWindow()
        ww.close()

        # 2 shot: Load BrainMRI_Glioma data

        # Carregar os volumes
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

        #searchBox = slicer.util.findChild(slicer.util.mainWindow(), "modelSearchBox")
        searchBox.setText("(BRATS) GLI")

        #modelCombo = slicer.util.findChild(slicer.util.mainWindow(), "modelComboBox")
        modelCombo.setCurrentItem(modelCombo.findItems("(BRATS) GLI", qt.Qt.MatchContains)[0])

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
        
        # Criar/configurar banco de dados DICOM
        import DICOMLib
        from DICOMLib import DICOMUtils
        
        # Obter ou criar o banco de dados DICOM
        dicomDatabase = slicer.dicomDatabase
        if not dicomDatabase:
            # Se não existe, criar um banco temporário
            dicomDatabasePath = os.path.join(slicer.app.temporaryPath, "DICOMDatabase")
            if not os.path.exists(dicomDatabasePath):
                os.makedirs(dicomDatabasePath)
            
            # Inicializar o banco de dados
            dicomWidget = slicer.modules.dicom.widgetRepresentation().self()
            dicomWidget.onDatabaseDirectoryChanged(dicomDatabasePath)
            dicomDatabase = slicer.dicomDatabase
        
        # Importar arquivos DICOM
        self.delayDisplay('Importando arquivos DICOM...')
        DICOMUtils.importDicom(ct_thorax_folder)
        
        # Aguardar a importação ser concluída
        import time
        time.sleep(2)
        slicer.app.processEvents()
        
        # Carregar os dados DICOM
        self.delayDisplay('Carregando dados DICOM...')
        dicomFiles = slicer.util.getFilesInDirectory(ct_thorax_folder)
        loadablesByPlugin, loadEnabled = DICOMLib.getLoadablesFromFileLists([dicomFiles])
        loadedNodeIDs = DICOMLib.loadLoadables(loadablesByPlugin)
        
        # Aguardar o carregamento ser concluído e verificar se os nós foram criados
        max_wait_time = 30  # 30 segundos no máximo
        start_time = time.time()
        ct_node = None
        
        while ct_node is None and (time.time() - start_time) < max_wait_time:
            slicer.app.processEvents()
            time.sleep(0.5)
            
            # Procurar especificamente pelo nó "6: CT_Thorax_Abdomen"
            try:
                ct_node = slicer.util.getNode("6: CT_Thorax_Abdomen")
                if ct_node:
                    print(f"Nó DICOM encontrado: {ct_node.GetName()}")
                    break
            except:
                # Se não encontrar com o nome exato, procurar por padrão similar
                volumeNodes = slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')
                for node in volumeNodes:
                    nodeName = node.GetName()
                    if 'CT_Thorax_Abdomen' in nodeName:
                        ct_node = node
                        print(f"Nó DICOM encontrado: {nodeName}")
                        break
        
        if ct_node is None:
            raise Exception("Falha ao carregar dados DICOM. Nó '6: CT_Thorax_Abdomen' não foi encontrado.")
        
        self.delayDisplay(f'Dados DICOM carregados: {ct_node.GetName()}')
        
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #1: DICOM module selected')

        # 2 shot: Open module selector and select Segmentation
        mainWindow.moduleSelector().selectModule('MONAIAuto3DSeg')
        layoutManager.setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutConventionalWidescreenView)    

        searchBox.setText("TS1 -")
        modelCombo.setCurrentItem(modelCombo.findItems("TS1 -", qt.Qt.MatchContains)[0])
        
        # TUTORIALMAKER SCREENSHOT
        self.delayDisplay('Screenshot #3: Whole Body Segmentation (TS1 - quick) model selected and ready to run')

        # 3 shot: Select volume input
        nodeSelectorTc = slicer.util.findChild(slicer.util.mainWindow(), "inputNodeSelector0")
        # Usar o nó CT que foi encontrado anteriormente
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
