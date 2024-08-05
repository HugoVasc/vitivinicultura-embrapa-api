import os
import scrapy
import json


class VitiviniculturaSpider(scrapy.Spider):
    name = "vitivinicultura"
    allowed_domains = ["vitibrasil.cnpuv.embrapa.br"]
    start_urls = ["http://vitibrasil.cnpuv.embrapa.br/"]
    navigation_url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao={}"
    navigation_inside_url_if_sub_buttons = (
        "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao={}&opcao={}"
    )

    def __init__(self):
        """
        Inicializa o spider
        Verifica se a pasta data/raw_data existe, se não cria
        """
        super(VitiviniculturaSpider, self).__init__()
        self.log("Iniciando o spider...")
        # verifica se pasta data/raw_data existe se não cria
        if not os.path.exists(os.path.join("..", "data", "raw_data")):
            os.makedirs(os.path.join("..", "data", "raw_data"))

    def start_requests(self):
        """
        Inicia o processo de scrap realizando a navegação na página inicial
        """
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response: scrapy.http.Response):
        """
        Realiza a navegação nas abas da página inicial
        """
        buttons = response.xpath('//button[@class="btn_opt"]')
        for button in buttons:
            value = button.xpath("@value").get()
            text = button.xpath("text()").get()
            self.log(f"Realizando scrap da aba: {text}...")
            yield scrapy.Request(
                url=self.navigation_url.format(value),
                callback=self.get_sub_buttons_options,
                meta={"opcao": value, "main_button": {"value": value, "text": text}},
            )

    def get_sub_buttons_options(self, response):
        """
        Obtem as opções de botões de subnavegação e salva em arquivo
        """
        sub_buttons = []
        buttons = response.xpath('//button[@class="btn_sopt"]')
        if buttons:
            for button in buttons:
                value = button.xpath("@value").get()
                text = button.xpath("text()").get()
                sub_buttons.append({"value": value, "text": text})
                opcao = response.meta["opcao"]
                self.log(f"Realizando scrap da sub-aba: {text}...")
                yield scrapy.Request(
                    url=self.navigation_inside_url_if_sub_buttons.format(value, opcao),
                    callback=self.parse_table,
                )
            self.save_sub_buttons(response.meta["main_button"], sub_buttons)
        else:
            # Se não houver subopções, prossegue para o parsing da tabela
            yield from self.parse_table(response)

    def parse_table(self, response: scrapy.http.Response):
        """
        Obtem o link para download do arquivo
        """
        download_path = response.xpath("//a[@class='footer_content']/@href").get()
        if download_path:
            url = self.start_urls[0] + download_path
            self.log(f"Realizando download de {url}")
            yield scrapy.Request(url=url, callback=self.save_file)
        else:
            # Realiza o scraping dos dados diretamente da tabela
            rows = response.xpath("//table//tr")
            for row in rows:
                cells = row.xpath("td")
                data = {
                    "cultivar": cells[0].xpath("text()").get(),
                    "quantidade": cells[1].xpath("text()").get(),
                }
                self.log(f"Dados da tabela: {data}")

    def save_file(self, response: scrapy.http.Response):
        """
        Baixa e salva o arquivo na pasta data/raw_data do projeto
        """
        filename = response.url.split("/")[-1]
        file_path = os.path.join(os.path.join("..", "data", "raw_data"), filename)
        with open(file_path, "wb") as f:
            f.write(response.body)
        self.log(f"Salvo arquivo {file_path}")

    def save_sub_buttons(self, main_button, sub_buttons):
        """
        Salva as opções de sub botões em um arquivo JSON
        """
        data = {"main_button": main_button, "sub_buttons": sub_buttons}
        filename = f"{main_button['value']}_sub_buttons.json"
        file_path = os.path.join(os.path.join("..", "data", "raw_data"), filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.log(f"Salvo arquivo de sub botões {file_path}")