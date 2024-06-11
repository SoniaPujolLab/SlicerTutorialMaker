import slicer
import os
import webbrowser
import qt

class markdownHTMLCreator:
    def __init__(self) -> None:
        pass

    def tutorial_to_markdown(self,path,ListotalImages):
        tutorialName = "fourMin_tutorial"
        metadatos = self.getMetadatos(path)
        #path = path + '_WithoutStyle'
        #print(path)
       # print(ListotalImages)
        with open(path + ".md", 'w', encoding='utf-8') as md_file:
            #Create main page
            md_file.write('<meta charset="UTF-8">\n')
            md_file.write(f'<img class="logo" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/slicer.png">\n\n')
            md_file.write(f'<br>')  
            md_file.write(f'    <div class="mainPage">\n')
            md_file.write(f'        <div>TUTORIAL</div>\n')
            md_file.write(f'        <br>\n')
            md_file.write(f'        <div class="text">AUTORES</div>\n')
            md_file.write(f'    </div>\n')
            md_file.write(f'</div>\n')
            md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_down.png">\n\n')

            #cont = 0
            #Create pages of the tutorial with annotations
            for num,item in enumerate(metadatos):
                #HEADER
               # print('num',num)
                #print('item',item)
               # num = int(item)-1 #Number of image-slide
               
                numString = str(num)
                numImage = str(ListotalImages[num])
                #print('NumImage',numImage)
                if (ListotalImages[num] == -1):
                   # imgSS = cont
                    md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_top.png">\n\n')
                    md_file.write(f'<img class="logo" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/slicer.png">\n\n')
                
                    md_file.write(f'<div class="titulo"><center><h2>{metadatos[item]["slide_title"]}</h2></center></div>\n\n')     

                     # Insert the image in Markdown with CSS styling
                   # md_file.write(f'<div class = "containerWhite"><img class="marginImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/NewSlide/white.png"><br>\n\n')
                    #Insert text
                    #md_file.write(f'<br>')
                    #md_file.write(f'<div class="textWhite"><center>{metadatos[item]["slide_text"]}</center></div><br></div>\n\n')
                    md_file.write(f'<div class="containerWhite">\n')
                    md_file.write(f'    <div class="textWhite">{metadatos[item]["slide_text"]}</div>\n')
                    md_file.write(f'    <img class="marginImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/NewSlide/white.png">\n')
                    md_file.write(f'</div>\n\n')
                    md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_down.png">\n\n')
                    
                    #Slide number
                    numString = str(num + 1)
                    totalSteps = str(len(metadatos) + 1)

                    md_file.write(f'<div class="footerText"><center><small><small>Tutorial page {numString}/{totalSteps}</small></small></center>\n\n')
                    # Close the slide div
                    md_file.write('</div>\n')

                   # if(cont < len(ListWhite)-1):
                    #    cont = cont + 1 
                else:                  
                    md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_top.png">\n\n')
                    md_file.write(f'<img class="logo" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/slicer.png">\n\n')
                    
                    md_file.write(f'<div class="titulo"><center><h2>{metadatos[item]["slide_title"]}</h2></center></div>\n\n')               

                    # Insert the image in Markdown with CSS styling
                    md_file.write(f'<img class="marginImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Outputs/Translation/output_image_{num}.png"><br>\n\n')
                    print(num)
                    #Insert text
                    md_file.write(f'<br>')
                    md_file.write(f'<div class="text"><center>{metadatos[item]["slide_text"]}</center></div><br>\n\n')
                    md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_down.png">\n\n')
                    
                    #Slide number
                    numString = str(num + 1)
                    totalSteps = str(len(metadatos) + 1)

                    md_file.write(f'<div class="footerText"><center><small><small>Tutorial page {numString}/{totalSteps}</small></small></center>\n\n')
                    # Close the slide div
                    md_file.write('</div>\n')
            
            #Create acknowledgments
            md_file.write('<meta charset="UTF-8">\n')
            md_file.write(f'<img class="logo" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/slicer.png">\n\n')
            md_file.write(f'<br>')  
            md_file.write(f'    <div class="mainPage">\n')
            md_file.write(f'        <div>ACKNOWLEDGMENTS</div>\n')
            md_file.write(f'        <br>\n')
            md_file.write(f'        <div class="text">...</div>\n')
            md_file.write(f'    </div>\n')
            md_file.write(f'</div>\n')
            md_file.write(f'<img class="LineImage" src="{os.path.dirname(slicer.util.modulePath("TutorialMaker"))}/Resources/Icons/Painter/line_down.png">\n\n')
            md_file.write(f'<div class="footerText">Tutorial page {totalSteps}/{totalSteps}\n\n')
            print(f"Markdown file has been generated at '{path}'")


            message = "Markdown file '{}' has been generated. Would you like to open it?".format(tutorialName)
            confirm = qt.QMessageBox.question(slicer.util.mainWindow(), "Markdown Generated", message,
                                            qt.QMessageBox.Yes | qt.QMessageBox.No)
            if confirm == qt.QMessageBox.Yes:
                webbrowser.open("file://" + path + ".md")


    def markdown_to_html(self,path, ListTotalImages):
        #ListWhite.sort()
        tutorialName = "fourMin_tutorial"
        #print(os.path.dirname(slicer.util.modulePath("TutorialMaker")) + "/Outputs/Annotations/" + tutorialName)
        self.tutorial_to_markdown(os.path.dirname(slicer.util.modulePath("TutorialMaker")) + "/Outputs/Annotations/" + tutorialName, ListTotalImages)   
        #Define CSS styles
        styles = """
        <style> 
            @page {
                size: A4 landscape;
                margin: 1cm;
            }
            .mainPage {
                height: 90%; 
                display: block;
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
            .containerWhite {
                position: relative;
                display: inline-block;
                width: 90%;
                display: block;
                margin-left: auto;
                margin-right: auto;
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
                margin-right: 10px;


            
            }
            .LineImage {
                width: 100% 
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
            contenido_md = file.read()
            # COmbine styleswith the Markdown file
    
        contenido_html_con_estilos = f"{styles}\n{contenido_md}"

        # Define the path of the HTML file
        path = path.replace('_WithoutStyle', '')
        output_html_file = path + ".html"
        # write the Markdown content with the styles in a HTML file
        with open(output_html_file, 'w', encoding='utf-8') as html_file:
            html_file.write(contenido_html_con_estilos)

       
        print(f"HTML file has been generated at '{path}'")
        message = "HTML file '{}' has been generated. Would you like to open it?".format(tutorialName)
        confirm = qt.QMessageBox.question(slicer.util.mainWindow(), "HTML Generated", message,
                                           qt.QMessageBox.Yes | qt.QMessageBox.No)
        if confirm == qt.QMessageBox.Yes:
            webbrowser.open("file://" + output_html_file)


    def getMetadatos(self,path):
        import Lib.utils as utils
        path = path + ".json"
        OutputAnnotator = utils.JSONHandler.parseJSON(path)
        return OutputAnnotator
    

        