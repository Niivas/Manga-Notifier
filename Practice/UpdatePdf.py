from borb.pdf import Document, Page, PageLayout, SingleColumnLayout, Paragraph, HexColor, Table, TableUtil, PDF
from decimal import Decimal


def updatePDF(data):
    # create an empty document
    doc: Document = Document()

    # create an empty page
    page: Page = Page()
    doc.add_page(page)

    # use a PageLayout to be able to add things easily
    layout: PageLayout = SingleColumnLayout(page)

    green = '#008000'
    black = '#000000'

    keyCount = 1
    # generate a Table for each issue
    for title, issue in data.items():
        # add a header (Paragraph)
        if issue["chaptersAddedSinceYouLastRead"] != "0.0":
            layout.add(Paragraph(f'{keyCount}. {title}', font_size=Decimal(20), font_color=HexColor(green)))
        else:
            layout.add(Paragraph(f'{keyCount}. {title}', font_size=Decimal(20), font_color=HexColor(black)))

        keyCount += 1

        # add a Table (using the convenient TableUtil class)
        table: Table = TableUtil.from_2d_array([["Site Accepted Name", issue.get("siteAcceptedName", "N.A.")],
                                                ["Latest Chapter", issue.get("latestChapter", "N.A.")],
                                                ["Latest Chapter Link",
                                                 issue.get("latestChapterLink", "N.A.")],
                                                ["Chapters Added since you last fetched",
                                                 issue.get("chaptersAddedSinceYouLastRead", "N.A.")],
                                                ], header_row=False, header_col=True, font_size=Decimal(10))
        layout.add(table)

    # store the PDF
    with open(r"C:\Users\Nivas Reddy\Desktop\Manga-Notifier\results\Latest Manga Updates.pdf", "wb") as pdf:
        PDF.dumps(pdf, doc)