import scrapy
from items import FileItem

class NhsSpider(scrapy.Spider):
    name = "nhs"
    start_urls = [
        "https://www.nhsbsa.nhs.uk/pharmacies-gp-practices-and-appliance-contractors/drug-tariff/drug-tariff-part-viii"
    ]

    # From start_url find all the Anchors for calss excel  href relative urls
    # add the base url to all relative urls
    # yield a custom FileItem initialized with the urls found
    # The defautl scrapy.pipelines.files.FilesPipeline saves the files to the FS

    def parse(self, response):
        relative_urls = response.css('p a.excel::attr(href)').extract()
        urls = [response.urljoin(relative_url) for relative_url in relative_urls]
        yield FileItem(
            file_urls=urls
        )

    # Alternantive ti save a file:
    def parse_listing(self, response):
        # ... extract pdf urls
        xls_urls = []
        for url in xls_urls:
            yield scrapy.Request(url, callback=self.save_xls)

    def save_xls(self, response):
        path = self.get_path(response.url)
        with open(path, "wb") as f:
            f.write(response.body)