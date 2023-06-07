from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

class Extracao:
    @staticmethod
    def tempo_pause(tempo):
        import time
        return time.sleep(tempo)

    def conect_requisicao(self, url):
        from urllib.request import urlopen, Request
        from urllib.error import HTTPError

        headers = \
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/94.0.4606.61 Safari/537.36"}
        requisicao = Request(url, headers=headers)
        try:
            response = urlopen(requisicao)
        except HTTPError:
            print('Time_Sleep')
            self.tempo_pause(60)
            return "Stop-Work"
        html = response.read()
        return html


    pass

    def salvar_arquivo(self, registro, cont):

        nome_arquivo = f"Data_CGESP1.txt"

        with open(nome_arquivo, 'a') as arquivo:
            arquivo.write(';'.join(registro) + '\n')
        print(cont)


if __name__ == '__main__':
    datafinal = datetime(year = 2022, month = 1, day =1)
    hoje = datetime.now()
    cont = 0
    while (hoje > datafinal):
        dia = datetime.strftime(hoje, "%d")
        mes = datetime.strftime(hoje, "%m")
        ano = datetime.strftime(hoje, "%y")

        ext = Extracao()
        html = ext.conect_requisicao("https://www.cgesp.org/v3/alagamentos.jsp?dataBusca={0}%2F{1}%2F20{2}&enviaBusca=Buscar".format(dia,mes,ano))

        if html == 'Stop-Work':
            continue

        soup = BeautifulSoup(html, 'html.parser')
        classe_html = soup.find('div', class_="content")
        texto_div = classe_html.text.strip()

        data = '20{0}.{1}.{2}'.format(ano, mes, dia)
        hoje -= timedelta(days=1)

        if texto_div == 'Não há registros de alagemtnos para essa data.':
            continue
        cont +=1
        texto_geral = soup.find_all('table', {'class': re.compile('tb-pontos-de-alagamentos')})
        bairro_texto = classe_html.find_all('td', {'class': re.compile('bairro arial-bairros-alag linha-pontilhada')})

        for x in range(0, len(bairro_texto)):
            bairro = bairro_texto[x].text.strip()
            lista_html = texto_geral[x].find_all('ul')

            for j in range(0, len(lista_html)):
                icone = lista_html[j].find('li').get('title')
                referencia = lista_html[j].find('li', {'arial-descr-alag col-local'})
                hr_inicio = referencia.text[3:8]
                avenida = referencia.text[16:]

                registro = [bairro, data, icone, hr_inicio, avenida]

                ext.salvar_arquivo(registro, cont)
    pass