from borb.pdf import Document, Page, PageLayout, SingleColumnLayout, Paragraph, HexColor, Table, TableUtil, PDF
from decimal import Decimal


def updatePdf(data):
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
        if issue["chaptersAddedSinceYouLastRead"] != "0.0":
            layout1.add(Paragraph(f'{keyCount}. {title}', font_size=Decimal(20), font_color=HexColor(green)))
        else:
            layout1.add(Paragraph(f'{keyCount}. {title}', font_size=Decimal(20), font_color=HexColor(black)))

        keyCount += 1

        # add a Table (using the convenient TableUtil class)
        table1: Table = TableUtil.from_2d_array([["Site Accepted Name", issue.get("siteAcceptedName", "N.A.")],
                                                 ["Latest Chapter", issue.get("latestChapter", "N.A.")],
                                                 ["Latest Chapter Link",
                                                  issue.get("latestChapterLink", "N.A.")],
                                                 ["Chapters Added since you last fetched",
                                                  issue.get("chaptersAddedSinceYouLastRead", "N.A.")],
                                                 ['Is Favorite', issue.get('isFavorite', "N.A.")]
                                                 ], header_row=False, header_col=True, font_size=Decimal(9))
        layout1.add(table1)
        if issue['isFavorite'] == 'yes':
            if issue["chaptersAddedSinceYouLastRead"] != "0.0":
                layout2.add(Paragraph(f'{count}. {title}', font_size=Decimal(20), font_color=HexColor(green)))
            else:
                layout2.add(Paragraph(f'{count}. {title}', font_size=Decimal(20), font_color=HexColor(black)))
            table2: Table = TableUtil.from_2d_array([["Site Accepted Name", issue.get("siteAcceptedName", "N.A.")],
                                                     ["Latest Chapter", issue.get("latestChapter", "N.A.")],
                                                     ["Latest Chapter Link",
                                                      issue.get("latestChapterLink", "N.A.")],
                                                     ["Chapters Added since you last fetched",
                                                      issue.get("chaptersAddedSinceYouLastRead", "N.A.")],
                                                     ['Is Favorite', issue.get('isFavorite', "N.A.")]
                                                     ], header_row=False, header_col=True, font_size=Decimal(9))
            count += 1
            layout2.add(table2)

    with open(r'C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Favorite Mangas.pdf', 'wb') as pdf:
        PDF.dumps(pdf, doc2)
    # store the PDF
    with open(r"C:\Users\Nivas Reddy\Desktop\Github files\Manga-Notifier\results\Latest Manga Updates.pdf", "wb") as pdf:
        PDF.dumps(pdf, doc1)
