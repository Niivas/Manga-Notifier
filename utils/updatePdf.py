from borb.pdf import Document, Page, PageLayout, SingleColumnLayout, Paragraph, HexColor, Table, TableUtil, PDF
from decimal import Decimal


def updatePdf(data):
    """
    :param data: a dictionary containing manga titles as keys and their corresponding information as values
    :return: None

    This method updates a PDF document with the latest manga updates based on the given data.
    It creates two separate documents: one for all mangas and another for favorite mangas.
    The documents are saved to the respective file paths.
    """
    # create an empty document for all mangas
    doc1: Document = Document()

    # create an empty page
    page1: Page = Page()
    doc1.add_page(page1)

    # use a PageLayout to be able to add things easily
    layout1: PageLayout = SingleColumnLayout(page1)

    # create an empty document for favorite mangas
    doc2: Document = Document()
    page2: Page = Page()
    doc2.add_page(page2)
    layout2: PageLayout = SingleColumnLayout(page2)
    green = '#008000'
    black = '#000000'

    keyCount = 1
    count = 1
    # generate a Table for each issue
    for title, issue in data.items():
        # add a header (Paragraph)
        if "days" in issue["latestRelease"] or "day" in issue["latestRelease"] or "1 week" in issue["latestRelease"] or "min" in issue["latestRelease"] or "hour" in issue["latestRelease"]:
            layout1.add(Paragraph(f'{keyCount}. {title}', font_size=Decimal(20), font_color=HexColor(green)))
        else:
            layout1.add(Paragraph(f'{keyCount}. {title}', font_size=Decimal(20), font_color=HexColor(black)))
        keyCount += 1

        # add a Table (using the convenient TableUtil class)
        table1: Table = TableUtil.from_2d_array([["Latest Chapter", issue.get("latestChapter", "N.A.")],
                                                 ["Latest Chapter Link",
                                                  issue.get("latestChapterLink", "N.A.")],
                                                 ["Latest Release", issue.get("latestRelease", "N.A.")],
                                                 ['Is Favorite', issue.get('isFavorite', "N.A.")]
                                                 ], header_row=False, header_col=True, font_size=Decimal(9))
        layout1.add(table1)
        if issue['isFavorite'] == 'yes':
            if "days" in issue["latestRelease"] or "day" in issue["latestRelease"] or "1 week" in issue["latestRelease"]:
                layout2.add(Paragraph(f'{count}. {title}', font_size=Decimal(20), font_color=HexColor(green)))
            else:
                layout2.add(Paragraph(f'{count}. {title}', font_size=Decimal(20), font_color=HexColor(black)))
            table2: Table = TableUtil.from_2d_array([
                                                     ["Latest Chapter", issue.get("latestChapter", "N.A.")],
                                                     ["Latest Chapter Link",
                                                      issue.get("latestChapterLink", "N.A.")],
                                                        ["Latest Release", issue.get("latestRelease", "N.A.")],
                                                     ['Is Favorite', issue.get('isFavorite', "N.A.")]
                                                     ], header_row=False, header_col=True, font_size=Decimal(9))
            count += 1
            layout2.add(table2)

    with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Favorite Mangas.pdf', 'wb') as pdf:
        PDF.dumps(pdf, doc2)
    # store the PDF
    with open(r"C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.pdf",
              "wb") as pdf:
        PDF.dumps(pdf, doc1)
