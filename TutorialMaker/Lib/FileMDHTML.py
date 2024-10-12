import slicer
import os
import webbrowser
import qt
from slicer.i18n import tr as _

class markdownHTMLCreator:
    def __init__(self) -> None:
        self.ensure_pdfkit_installed()
        pass

    def ensure_pdfkit_installed(self):
        try:
            import pdfkit
        except ImportError:
            slicer.util.pip_install('pdfkit')
            
    def show_installing_message(self, message):
        msgBox = qt.QMessageBox()
        msgBox.setIcon(qt.QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setStandardButtons(qt.QMessageBox.NoButton)
        msgBox.show()
        
        # Allow the interface to process events to keep the message box responsive
        slicer.app.processEvents()
        return msgBox
    
    def tutorial_to_markdown(self,path,ListotalImages):
        tutorialName = "fourMin_tutorial"
        metadata = self.getMetadata(path)
        
        with open(path + ".md", 'w', encoding='utf-8') as md_file:
            #Create pages of the tutorial with annotations
            for num,item in enumerate(metadata):            
                numString = str(num)
                if (ListotalImages[num] == -1):
                    if (num == 0):
                        md_file.write('<meta charset="UTF-8">\n')
                        md_file.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
                        md_file.write(f'<div class="containerPage" style="max-width: 100%; margin: 0 auto;">\n')
                       # Header section
                        md_file.write(f'<div class="containerHeader" style="text-align: center; width: 100%;">\n')
                        md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_top.png" style="width: 100%;">\n')
                        md_file.write(f'<img class="logo" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/slicer.png" style="width: 100%; margin-top: 10px;">\n')
                        md_file.write('</div>\n')
                        md_file.write(f'<br>\n')

                        # Slide Title
                        md_file.write(f'<div class="mainPage" style="text-align: center; width: 100%;">\n')
                        md_file.write(f'  <div class="header" style="background-color: #a8d0e6; padding: 10px; color: white; font-size: 40px; font-weight: bold; text-align: center; max-width: 90%; margin: 0 auto;">{metadatos[item]["slide_title"]}</div>\n')
                        md_file.write(f'<br>\n')

                        # White container with text
                        authors = metadata[item]["slide_text"].replace('\n', '<br>')
                        if authors.endswith('<br>'):
                            authors = authors[:-4] 
                        md_file.write(f'  <div class="subheader" style="font-size: 30px; margin: 10px 0; color: gray; text-align: center; max-width: 90%; margin: 0 auto;">{authors}</div>\n')
                        md_file.write('</div>\n')
                        # Footer section

                        md_file.write(f'<div class="containerHeader" style="text-align: center; width: 100%;">\n')    
                        md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_down.png" style="width: 100%;">\n\n')
                        md_file.write('</div>\n')

                        # Closing the main page div
                        md_file.write(f'</div>')
                        md_file.write('<div style="page-break-after: always;"></div>\n')
                      
                        
                    else:
                        md_file.write(f'<div class="containerPage" style="max-width: 100%; margin: 0 auto; text-align: center;">\n')
                        
                        # Header section
                        md_file.write(f'<div class="containerHeader" style="text-align: center; width: 100%;">\n')            
                        md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_top.png" style="width: 100%;">\n\n')
                        md_file.write(f'<img class="logo" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/slicer.png" style="position: absolute; top: 10px; right: 10px; width: 100%; height: auto;">\n\n')

                        md_file.write(f'</div>\n')

                        # Slide Title
                        md_file.write(f'<div class="titulo" style="margin: 20px auto;"><h2>{metadata[item]["slide_title"]}</h2></div>\n\n')

                        # White container with text
                        md_file.write(f'<div class="containerWhite" style="background-color: #ffffff; padding: 20px; margin: 20px auto; max-width: 90%;">\n')
                        md_file.write(f'<div class="textWhite" style="font-size: 18px;">{metadata[item]["slide_text"]}</div>\n')
                        md_file.write(f'<img class="marginImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/NewSlide/white.png" style="width: 100%; max-width: 500px;">\n')
                        md_file.write(f'</div>\n')

                        # Footer section
                        md_file.write(f'<div class="containerHeader" style="text-align: center; width: 100%;">\n')    
                        md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_down.png" style="width: 100%;">\n\n')

                        # Page number
                        numString = str(num + 1)
                        totalSteps = str(len(metadata) + 1)
                        md_file.write(f'<div class="footerText"><small><small>Tutorial page {numString}/{totalSteps}</small></small></div>\n\n')

                        # Close containers
                        md_file.write(f'</div>\n')
                        md_file.write(f'</div>\n')

                else: 
                    # Main container
                    md_file.write(f'<div class="containerPage" style="max-width: 100%; margin: 0 auto; text-align: center;">\n')

                    # Header section
                    md_file.write(f'<div class="containerHeader" style="text-align: center; width: 100%;">\n')            
                    md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_top.png" style="width: 100%;">\n\n')
                    md_file.write(f'<img class="logo" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/slicer.png" style="width: 100%; margin-top: 10px;">\n\n')
                    md_file.write(f'</div>\n') 

                    # Slide Title
                    md_file.write(f'<div class="titulo" style="margin: 20px auto;"><h2>{metadata[item]["slide_title"]}</h2></div>\n\n')

                    # Slide Image
                    md_file.write(f'<img class="marginImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Outputs/Translation/output_image_{num}.png" style="width: 100%; max-width: 600px;"><br>\n\n')

                    # Slide Text
                    md_file.write(f'<div class="text" style="font-size: 18px; margin: 10px auto; max-width: 90%; text-align: center;">{metadata[item]["slide_text"]}</div><br>\n\n')

                    # Footer section
                    md_file.write(f'<div class="containerHeader" style="text-align: center; width: 100%;">\n')
                    md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_down.png" style="width: 100%;">\n\n')

                    # Page number
                    numString = str(num + 1)
                    totalSteps = str(len(metadata) + 1)
                    md_file.write(f'<div class="footerText"><small><small>Tutorial page {numString}/{totalSteps}</small></small></div>\n\n')

                    # Close containers
                    md_file.write(f'</div>\n')
                    md_file.write(f'</div>\n')

            message = _("Markdown file '{tutorialName}' has been generated. Would you like to open it?".format(tutorialName=tutorialName))
            confirm = qt.QMessageBox.question(slicer.util.mainWindow(), _("Markdown Generated"), message,
                                            qt.QMessageBox.Yes | qt.QMessageBox.No)
            if confirm == qt.QMessageBox.Yes:
                webbrowser.open("file://" + path + ".md")


    def markdown_to_html(self,path, ListTotalImages):
        tutorialName = "fourMin_tutorial"
        self.tutorial_to_markdown(os.path.dirname(slicer.util.modulePath("TutorialMaker")) + "/Outputs/Annotations/" + tutorialName, ListTotalImages)   
        # Define CSS styles
        styles = """
        <style> 
            .mainPage {
                height: 45%;
                margin-left: auto;
                margin-right: auto;
                font-size: 80px;
                font-weight: bold;
                text-align:center;
            }
            .titulo {
                font-size: 30px;
                font-weight: bold;
                text-align:center;
                align-items: center;
            }
            .text {
                font-size: 20px;
                text-align:center;
            }
            .containerPage{
                width : 1200px;
                heigth : 1200px; 
                align-items: center;
            }
            .containerHeader {
             width: 100%;
             heigth : 1in; 
            }
            .containerFooter {
             width: 100%;
             heigth : 0.2in; 
            }
            .containerWhite {
                position: relative;
                display: inline-block;
                width: 90%;
                display: block;
                margin-left: auto;
                margin-right: auto;
                margin-bottom:1in;
            }
            .textWhite {
                font-size: 28px;
                text-align:center;
                position: absolute;  
            }
            .logo{
                width:100%;
            }
            .header{
                display: flex; 
                align-items: center; 
            }
            .footerText{
                font-size: 15px;
                text-align:right;
                margin-bottom: 40px;
                margin-bottom: 1in;
            }
            .LineImage {
                width: 100vw;
                background-image: url('images/mail.png');
                background-size: auto 100%; 
                background-repeat: repeat-x; 
            }
            .marginImage {
                width: 90%;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
        </style>
        """

        # Read the Markdown file
        with open(path + ".md", 'r', encoding='utf-8') as file:
            md_file = file.read()
            # Combine styleswith the Markdown file
    
        html_content = f"{styles}\n{md_file}"

        # Define the path of the HTML file
        path = path.replace('_WithoutStyle', '')
        output_html_file = path + ".html"
        # Write the Markdown content with the styles in a HTML file
        with open(output_html_file, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

        message = _("HTML file '{tutorialName}' has been generated. Would you like to open it?".format(tutorialName=tutorialName))
        confirm = qt.QMessageBox.question(slicer.util.mainWindow(), _("HTML Generated"), message,
                                           qt.QMessageBox.Yes | qt.QMessageBox.No)
        if confirm == qt.QMessageBox.Yes:
            webbrowser.open("file://" + output_html_file)


    def getMetadata(self,path):
        import Lib.utils as utils
        path = path + ".json"
        OutputAnnotator = utils.JSONHandler.parseJSON(path)
        return OutputAnnotator
    
    def html_to_pdf(self,path, output_html_file, tutorialName):
        import pdfkit
        
        output_pdf_file = path + ".pdf"
        options = {
            'page-size': 'A4',
        }
        exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe')
        exe_path = os.path.normpath(exe_path)
        config = pdfkit.configuration(wkhtmltopdf=exe_path)
        
        try:
            pdfkit.from_file(output_html_file, output_pdf_file, options=options, configuration=config)
            message = _("PDF file '{tutorialName}' has been generated. Would you like to open it?".format(tutorialName=tutorialName))
            confirm = qt.QMessageBox.question(slicer.util.mainWindow(), _("PDF Generated"), message,
                                            qt.QMessageBox.Yes | qt.QMessageBox.No)
            if confirm == qt.QMessageBox.Yes:
                webbrowser.open("file://" + path + ".pdf")
        except IOError as e:
            print(f"Error al crear PDF: {e}")