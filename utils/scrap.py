import os
import scrapy

class VitiviniculturaSpider(scrapy.Spider):
    name = 'vitivinicultura'
    allowed_domains = ['vitibrasil.cnpuv.embrapa.br']
    start_urls = ['http://vitibrasil.cnpuv.embrapa.br/']
    navigation_url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao={}"
    
    def __init__(self):
        """
        Inicializa o spider
        Verifica se a pasta data existe, se não cria        
        """
        super(VitiviniculturaSpider, self).__init__()
        self.log("Iniciando o spider...")
        # verifica se pasta data existe se não cria
        if not os.path.exists("data"):
            os.makedirs("data")


    def start_requests(self):
           """
              Inicia o processo de scrap realizando a navegação na página inicial
           """
           yield scrapy.Request(url=self.navigation_url.format("opt_01"), callback=self.parse)

    def parse(self, response: scrapy.http.Response):
        """
        Realiza a navegação nas abas da página inicial
        """
        buttons = response.xpath('//button[@class="btn_opt"]')
        for button in buttons:
            value = button.xpath('@value').get()
            text = button.xpath('text()').get()
            self.log(f"Realizando scrap da aba: {text}...")
            yield scrapy.Request(
                url=self.navigation_url.format(value),
                callback=self.parse_table
            )

    def parse_table(self, response: scrapy.http.Response):
        """
        Obtem o link para download do arquivo
        """
        download_path = response.xpath("//a[@class='footer_content']/@href").get()
        url = self.start_urls[0] + download_path
        # log
        self.log(f"Realizando download de {url}")
        yield scrapy.Request(url=url, callback=self.save_file)

    def save_file(self, response: scrapy.http.Response):
        """
        Baixa e salva o arquivo na pasta data/ do projeto
        """
        filename = response.url.split("/")[-1]
        with open(f"data/{filename}", 'wb') as f:
            f.write(response.body)
        self.log(f'Salvo arquivo {filename}')