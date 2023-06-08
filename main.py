from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re


class Extracao:

    def __init__(self, nome_arquivo, year, month, day):
        from datetime import datetime

        self._nome_arquivo = nome_arquivo
        self._datafinal = datetime(year=year, month=month, day=day)

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

    def salvar_arquivo(self, registro):

        with open(self._nome_arquivo, 'a') as arquivo:
            arquivo.write(';'.join(registro) + '\n')

    def executar_extracao(self):

        hoje = datetime.now()

        while hoje > self._datafinal:
            dia_sl = datetime.strftime(hoje, "%d")
            mes_sl = datetime.strftime(hoje, "%m")
            ano_sl = datetime.strftime(hoje, "%y")

            html = self.conect_requisicao(
                "https://www.cgesp.org/v3/alagamentos.jsp?dataBusca={0}%2F{1}%2F20{2}&enviaBusca=Buscar".format(dia_sl,
                                                                                                                mes_sl,
                                                                                                                ano_sl))
            if html == 'Stop-Work':
                continue

            soup = BeautifulSoup(html, 'html.parser')
            classe_html = soup.find('div', class_="content")
            texto_div = classe_html.text.strip()
            data = '20{0}.{1}.{2}'.format(ano_sl, mes_sl, dia_sl)
            hoje -= timedelta(days=1)

            if texto_div == 'Não há registros de alagemtnos para essa data.':
                continue

            texto_geral = soup.find_all('table', {'class': re.compile('tb-pontos-de-alagamentos')})
            bairro_texto = classe_html.find_all('td',
                                                {'class': re.compile('bairro arial-bairros-alag linha-pontilhada')})

            for x in range(0, len(bairro_texto)):
                bairro = bairro_texto[x].text.strip()
                lista_html = texto_geral[x].find_all('ul')

                for j in range(0, len(lista_html)):
                    icone = lista_html[j].find('li').get('title')
                    referencia = lista_html[j].find('li', {'arial-descr-alag col-local'})
                    hr_inicio = referencia.text[3:8]
                    avenida = referencia.text[16:]

                    registro = [bairro, data, icone, hr_inicio, avenida]

                    self.salvar_arquivo(registro)


class LeituraArquivo:

    def __init__(self, nameFile):
        self._nameFile = nameFile
        self._count = 0
        with open(nameFile) as data:
            self._data = data.readlines()

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            element = self._data[self._count]
        except IndexError as ie:
            self._count = 0
            raise StopIteration
        self._count += 1
        return element


if __name__ == '__main__':
    name = 'Data_CGESP1.txt'
    ano = 2022
    mes = 1
    dia = 1
    #etx = Extracao(name, ano, mes, dia)
    #etx.executar_extracao()
    tt = LeituraArquivo(name)
    c= 0
    for file in tt:
        print(file)

    pass
