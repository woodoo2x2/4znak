from PIL import Image, EpsImagePlugin, ImageWin, ImageDraw, ImageFont
import win32print
import win32ui
def convert_eps_to_jpeg(image_name,name,color,size):
    EpsImagePlugin.gs_windows_binary =  r'C:\Program Files\gs\gs10.01.2\bin\gswin64c'

    pic = Image.open(image_name)
    pic.load(scale = 10)
    if pic.mode in ('P', '1'):
        pic = pic.convert("RGB")

    # pic.save("image_esp_test.jpeg")
    # image = Image.new('RGB', (420, 284), 'white')
    image = Image.new('RGB', (406, 284), 'white')

    pic = pic.resize((200,200))
    image.paste(pic,(30,30))
    font = ImageFont.truetype('microsoftsansserif.ttf', size=20)
    draw_text = ImageDraw.Draw(image)
    if len(name.split())>1:
        name = '\n'.join(name.split())
    draw_text.text((250,40),f'Наименование:\n{name.capitalize()}\nЦвет:\n{color.capitalize()}\nРазмер:\n{size}',font=font, fill=('#1C0606'))

    image.save('example.jpeg')

def print_label():
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111

    printer_name = win32print.GetDefaultPrinter()
    file_name = "example.jpeg"

    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)

    bmp = Image.open(file_name)

    bmp = bmp.rotate(180)

    hDC.StartDoc(file_name)
    hDC.StartPage()

    dib = ImageWin.Dib(bmp)
    dib.draw(hDC.GetHandleOutput(), (0, 0, printer_size[0], printer_size[1]))

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()

