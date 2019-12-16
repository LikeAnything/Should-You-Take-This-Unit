'''
A PDF scraper, scrapes text from a given pdf file.

Date: 4/12/2019
Directly copied from: http://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
Requires pdfminer: pip3 install pdfminer

'''

import io
 
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
 
def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
 
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
 
        text = fake_file_handle.getvalue()
 
    # close open handles
    converter.close()
    fake_file_handle.close()
 
    if text:
        return text
 
if __name__ == '__main__':
    print(extract_text_from_pdf('sampleSetuPDFs/UE00389-Unit_Evaluation_Report-FIT1003_SAFRICA_ON-CAMPUS_ON_S1-01-1915544_c2708757-78de-4d7f-a5da-732bc7bf37f9en-US.pdf'))
