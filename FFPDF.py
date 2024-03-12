import pdfrw

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A3
from Examples import PDF_dict2
from typing import List,Dict



def create_overlay_pdf(image_paths:List, overlay_pdf_path:str, top_left_x:float,
                       top_left_y:float, width:float, height:float, spacing:float)->None :
    """
    Create a PDF with multiple images with specified spacing between them. 
    PDF name is overlay.PDF.
    """
    # Calculate positions for all images based on the first image's position and spacing
    positions = [{
        'top_left_x': top_left_x + i * (width + spacing),
        'top_left_y': top_left_y,
        'width': width,
        'height': height
    } for i in range(len(image_paths))]
    
    # Create a new PDF with the images
    c = canvas.Canvas(overlay_pdf_path, pagesize=landscape(A3))
    for image_path, position in zip(image_paths, positions):
        c.drawImage(image_path, position['top_left_x'], position['top_left_y'], width=position['width'], height=position['height'])
    c.save()


def fill_fields(fields:Dict,filled_output_dir:str,template:str='moderate_template.pdf')-> any:
    """ fill all texbox in the template. It returns a pdfrw object """
    input_pdf = pdfrw.PdfReader(template)

    input_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    for x in range(0, len(input_pdf.Root.AcroForm.Fields)):
        key  = input_pdf.Root.AcroForm.Fields[x].T[1:-1]
        if  key in fields.keys():
            input_pdf.Root.AcroForm.Fields[x].update(pdfrw.PdfDict(V= fields[key]))

            # this section doesnt fit with arial 12 thus I reduce it to 11
            if key == 'DAMAGE2':
                font_size = pdfrw.objects.pdfstring.PdfString.encode('0 g /Arial 11 Tf')
                input_pdf.Root.AcroForm.Fields[x].update({'/DA': font_size})

            if key == 'Risk_Ranking':
                print('rating' , fields[key])
    writer = pdfrw.PdfWriter()
    writer.write(filled_output_dir, input_pdf)
    return input_pdf
                


def concat_pdfs(pdf1:str, pdf2:str, output:str)->None:
    """ 
    Reads the filled pdf (form) and reads the overlay images (Olay) and merges the files.
    "output" is the names of resulting PDF
    """
    form = pdfrw.PdfReader(pdf1)
    olay = pdfrw.PdfReader(pdf2)
    
    for form_page, overlay_page in zip(form.pages, olay.pages):
        merge_obj = pdfrw.PageMerge()
        overlay = merge_obj.add(overlay_page)[0]
        pdfrw.PageMerge(form_page).add(overlay).render()
        
    writer = pdfrw.PdfWriter()
    writer.write(output, form)


def main(fields:Dict,overlay_dir:str,template_dir:str,filled_output_dir:str,
         merge_dir:str,image_paths:List,top_left_x:float,top_left_y:float,
         width:float, height:float, spacing:float)->None:
    
    # create image overlay 
    create_overlay_pdf(image_paths, overlay_dir, top_left_x,
                       top_left_y, width, height, spacing)
    # fill pdf form 
    fill_fields(fields,filled_output_dir,template_dir)

    # merge pdf 
    concat_pdfs(filled_output_dir,overlay_dir,merge_dir)



if __name__ == '__main__':

    #  Export pydantic model in Dict
    fields = PDF_dict2
    # image list
    image_paths = [
    r'images\IMG_3369_20240222121404.JPG',
    r'images\IMG_3370_20240222121408.JPG',
    r'images\IMG_3371_20240222121413.JPG',
    ]
    # image settings
    top_left_x = 200  
    top_left_y = 50  
    width = 250      
    height = 300     
    spacing = 50   
    
    # filled pdf name
    filled_output_dir = 'filled_pdf.pdf'
    overlay_dir = 'overlay.pdf'
    merge_dir = 'report_example.pdf'
    template_dir =r"Templates\moderate_template.pdf"
    main(fields,overlay_dir,template_dir,filled_output_dir,
        merge_dir,image_paths,top_left_x,top_left_y,width,
        height,spacing)