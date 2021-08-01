import csv
import os
from os import listdir, stat
from os.path import isfile, join


    
class backup:
    @staticmethod
    def importar(nome_arquivo, agenda):
        '''
        Lê um arquivo .csv e retorna seu conteúdo em uma lista de listas
        '''
        try:
            arquivo = open('arquivos/' + nome_arquivo, "r", encoding="utf-8")
            lista_csv = csv.reader(arquivo, delimiter=";", lineterminator="\n")
            lista_contatos = []
        
            for contato in lista_csv:
                lista_contatos.append(contato)
            arquivo.close()

            print('leitura do arquivo Ok')
            print(lista_contatos)
        except:
            print(f'\nArquivo de backup {nome_arquivo} não encontrado.\n')
            return False

        try:
            print('desembaralhando...')
            lista_contatos = backup.desembaralha_contatos(lista_contatos)
            print(lista_contatos)
        except:
            print('Não foi possível desembaralhar o arquivo.')

        try:
            print('eliminando campos vazios...')
            lista_contatos = backup.elimina_campos_vazios(lista_contatos)
            print(lista_contatos)
        except:
            print('Não foi possível eliminar os campos vazios.')

        try:
            lista_contatos = backup.grava_grupos(agenda, lista_contatos)    
        except:
            print('Não foi possível gravar os grupos.\nUsando lista de grupos padrão')
        
        try:
            print('criando lista de telefones e e-mails...')
            lista_contatos = backup.create_tel_email_lists(lista_contatos)
        except:
            print('Não foi possível criar as listas de telefone e email.')
        
        print('lista de contatos criada com sucesso!')
        print(lista_contatos)
        return lista_contatos


    @staticmethod
    def grava_grupos(agenda, lista_contatos):
        if 'Todos' in lista_contatos[0][0]:
            print('gravando grupos...')
            grupos = lista_contatos.pop(0)
            grupos = grupos[0].split(',')
            for grupo in grupos:
                agenda.grupos.add(grupo)
            return lista_contatos
        else:
            print('lista de grupos não encontrada.\nUsando lista de grupos padrão')
        return False


    @staticmethod
    def create_tel_email_lists(lista_contatos):
        for contato in lista_contatos:
            tel_aux = contato[1].split(',')
            print('criando lista de telefones...')
            email_aux = contato[2].split(',')
            print('criando lista de emails...')
            grupos_aux = contato[4].split(',')
            print('criando lista de grupos...')
            contato.pop(1)
            contato.insert(1, tel_aux)
            print('inserindo lista de telefones...')
            contato.pop(2)
            contato.insert(2, email_aux)
            print('inserindo lista de telefones...')
            contato.pop(4)
            contato.insert(4, grupos_aux)
            print('inserindo lista de telefones...')
        return lista_contatos


    @staticmethod
    def elimina_campos_vazios(lista_contatos):
        
        for contato in lista_contatos:
                for campo in contato[-1::-1]:
                    if campo == '':
                        contato.pop(contato.index(campo))
                        print(contato)
                    else:
                        break
                    print(contato)
        return lista_contatos    


    @staticmethod    
    def ordena_linha(linha):
        linha_ordenada = ['', '', '']
        for dado in linha[0:3]:
            #se o dado tiver o caractere '@', coloque ele na posição 2 (email)
            if "@" in dado: linha_ordenada[2] = dado
            #se o dado for numérico, coloque ele na posição 1 (telefone)
            elif ',' in dado and '@' not in dado or dado.isnumeric(): linha_ordenada[1] = dado
            #se o dado for alfabético, coloque ele na posição 0 (nome)
            elif ''.join(dado.split(' ')).isalpha(): linha_ordenada[0] = dado

        for dado in linha[3:len(linha)]:
            linha_ordenada.append(dado)

        return linha_ordenada


    @staticmethod 
    def desembaralha_contatos(contatos):
    
        contatos_ordenados=[]

        #usa a função "ordena_linha" de forma recursiva, afim de organizar a lista inteira
        for linha in contatos:
            if 'Todos' not in linha[0]:
                contatos_ordenados.append(backup.ordena_linha(linha))
            else:
                contatos_ordenados.append(linha)
        return contatos_ordenados


    @staticmethod
    def exportar(nome_arquivo, lista_contatos):
        '''
        Exporta a lista de contatos para arquivo .csv
        '''

        arquivo = open('arquivos/' + nome_arquivo + '.csv', "r+", encoding="utf-8")
        csv.writer(arquivo, delimiter=';', lineterminator='\n').writerows(lista_contatos)
        arquivo.close()
        print(f"A lista de contatos foi exportada para o arquivo: {nome_arquivo} .")

        return     


    @staticmethod
    def formata_lista_contatos_exportacao(contatos, grupos):
        '''
        formata a lista de contatos para exportação para arquivo csv
        '''
        print('formatando lista de contatos')
        lista_contatos = [[','.join(grupos)]]
        for contato in contatos:
            lista_contatos.append([contato.nome, ','.join(contato.lista_telefones), ','.join(contato.lista_emails), contato.ID, ','.join(contato.tags), contato.sobrenome])
        print(lista_contatos)
        return lista_contatos


    @staticmethod
    def criar(nome_arquivo):
        '''
        Cria uma lista de contatos em um arquivo .csv
        '''
        arquivo = open('arquivos/' + nome_arquivo + '.csv', "w", encoding="utf-8")
        arquivo.close()
        
        print(f"Arquivo {nome_arquivo}.csv criado!")
        
        return    


    @staticmethod
    def le_diretorio():
        '''
        Le o diretorio de arquivos .csv
        '''
        mypath = 'arquivos/'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        return onlyfiles


    @staticmethod
    def salva_agenda(self):
        lista_contatos = backup.formata_lista_contatos_exportacao(self.contatos, self.grupos)
        backup.exportar(self.nome_agenda, lista_contatos)
        print(f'Agenda {self.nome_agenda} salva com sucesso!')


class dados:
    @staticmethod
    def valida_nome(nome):
        while True:
            '''
            verifica se o nome é composto apenas por letras
            '''
            if "".join(nome.split(' ')).isalpha():
                return True
            else:
                print('O nome deve conter apenas letras.')
                return False

    @staticmethod
    def valida_telefone(telefone):
        '''
        verifica se o telefone é composto apenas por números
        '''
        while True:
            if telefone.isnumeric():
                return True
            else:
                print('O telefone deve conter apenas números.')
                return False
    
    @staticmethod
    def valida_email(email):
        '''
        verifica se o email contém um domínio
        '''
        while True:
            if '@' in email and '.' in email and email[-1] != '.':
                return True
            else:
                print('O email deve conter um domínio válido (@).')
                return False

    @staticmethod
    def requisita_dados():
        '''
        Menu de contatos da agenda
        '''
        
        lista_emails = []
        
        lista_telefones = []

        while True:
            nome = input('Entre com o nome do contato: ')
            if dados.valida_nome(nome):
                break

        while True:
            sobrenome = input('Entre com o sobrenome do contato: ')
            if sobrenome=='':
                break
            elif dados.valida_nome(sobrenome):
                break

        while True:
            telefone = input('Entre com o telefone do contato (q para sair): ')
            if telefone.lower() == 'q':
                break 
            if dados.valida_telefone(telefone):
                lista_telefones.append(telefone)
            

        while True:
            email = input('Entre com o e-mail do contato (q para sair): ')
            if email.lower() == 'q':
                break
            if dados.valida_email(email):
                lista_emails.append(email.lower())
        
        return nome, lista_telefones, lista_emails, sobrenome


class Agenda:
    
    agendas = []

    def __init__(self, nome_agenda):
        '''
        cria objeto Agenda
        '''
        self.nome_agenda = nome_agenda
        self.IDs = set()
        self.contatos_ativos = 0
        self.contatos_totais = 0
        self.contatos = [] 
        self.grupos = {'Ativos', 'Inativos', 'Todos'}

    def menu_agenda(self):
        '''
        Menu da agenda
        '''
        while True:
            opt = input('1. Cadastrar contato: \n2. Alterar contato: \n3. Excluir contato\n4. Listar contatos\n5. Pesquisar contato\n6. Criar grupo\n7. Incluir/Exluir contato em grupo\n8. Listar Contatos de grupo\n9. Importar backup de contatos\n10. Salvar alterações\n0. Sair\n')
            
            if opt == '1':
                nome, lista_telefones, lista_emails, sobrenome = dados.requisita_dados()
                self.cadastra_contato(nome=nome, lista_telefones=lista_telefones, lista_emails=lista_emails, sobrenome=sobrenome)
                
            elif opt == '2':
                self.altera_contato()
            elif opt == '3':
                #contato_selecionado = self.seleciona_contato('Ativos')
                self.exclui_contato()
            elif opt == '4':
                opt = 'Ativos' #input('1.Ativos\n2.Inativos\n3.Todos\n')
                self.lista_contatos('Ativos')
            elif opt == '5':
                self.pesquisa_contato()
            elif opt == '6':
                self.cria_grupo()
            elif opt == '7':
                self.inlui_exclui_contato_em_grupo()
            elif opt == '8':
                self.lista_contatos()
            elif opt == '9':
                opt = self.seleciona_csv()
                lista_contatos = backup.importar(opt)
                self.cadastra_contatos(lista_contatos)                   
            elif opt == '10':
                backup.salva_agenda(self)
            elif opt == '0':
                opt = input('1. Salvar e sair\n2. Sair sem salvar\n')
                if opt == '1':
                    backup.salva_agenda(self)
                else:
                    print('Voltando para menu de agendas!')
                break
            else:    
                print('Opção inválida')


    def cadastra_contatos(self, file, lista_contatos):
        '''
        cadastra todos os contatos de uma lista de contatos importados        
        '''    
        for i, contato in enumerate(lista_contatos):
            if len(contato) == 3:
                self.cadastra_contato(nome = contato[0].lower(), lista_telefones = contato[1], lista_emails = contato[2])
                print(i+1, 'contatos importados')
            elif len(contato) == 4:
                self.cadastra_contato(nome = contato[0].lower(), lista_telefones = contato[1], lista_emails = contato[2], ID = contato[3])
                print(i+1, 'contatos importados')           
            elif len(contato) == 5:
                self.cadastra_contato(nome = contato[0].lower(), lista_telefones = contato[1], lista_emails = contato[2], ID = contato[3], tags = contato[4])
                print(i+1, 'contatos importados')
            elif len(contato) == 6:
                self.cadastra_contato(nome = contato[0].lower(), lista_telefones = contato[1], lista_emails = contato[2], ID = contato[3], tags = contato[4], sobrenome = contato[5])
                print(i+1, 'contatos importados')
            else:
                print(f'\nNão foi possível carregar os contatos de {file}\n')


    def cadastra_contato(self, nome, lista_telefones, lista_emails, ID='', tags='', sobrenome = ''):
        '''
        testa se a agenda tem espaço e se, tiver, cadastra um novo contato.
        Se a agenda estiver cheia, te pergunta se quer excluir algum contato existente
        '''
        if self.contatos_ativos < 75:
            self.contatos_totais += 1
            self.contatos_ativos += 1
            if ID == '':
                ID = self.cria_ID()
            else:
                ID = int(ID)
                self.IDs.add(ID)
            contato = Contato(ID, nome, lista_telefones, lista_emails, sobrenome)
            print(ID, type(ID))
            for tag in tags:
                contato.tags.add(tag)
            self.contatos.append(contato)
            contato.tags.add('Ativos')
            contato.tags.add('Todos')
            print(contato.nome, contato.lista_telefones, contato.lista_emails, contato.ID, contato.tags, contato.sobrenome)
            
        else:
            opt = input('Agenda cheia. Excluir uma entrada (s ou n)?')
            if opt.lower() == 's':
                self.exclui_contato()
                self.cadastra_contato()


    def cria_ID(self):
        '''
        cria ID
        '''
        print('criando ID')
        while True:
            for i in range(1, max(self.IDs)):
                print(i, i in self.IDs)
                if i not in self.IDs:
                    ID = i
                    self.IDs.add(ID)
                    print('ID not in IDs',ID, type(ID))
                    print('IDs: ', self.IDs)
                    break
                print(len(self.IDs))
                ID = max(self.IDs) + 1
                print('New ID', ID, type(ID))
                print('IDs: ', self.IDs)
                self.IDs.add(ID)
            break

        return ID
        

    def altera_contato(self):
        '''
        seleciona um contato e pede um novo valor ao usuário
        '''
        
        opt = self.seleciona_grupo()
        contato_selecionado = self.seleciona_contato(opt)
        nome = input(f'Entre com o nome do contato [{contato_selecionado.nome}]: ') or contato_selecionado.nome
        sobrenome = input(f'Entre com o sobrenome do contato [{contato_selecionado.sobrenome}]: ') or contato_selecionado.sobrenome
        
        self.altera_telefone(contato_selecionado)
        
        while True:
            telefone = input('Entre com o telefone do contato (q para sair): ')
            if telefone.lower() == 'q':
                break 
            if dados.valida_telefone(telefone):
                contato_selecionado.lista_telefones.append(telefone)
        
        self.altera_email(contato_selecionado)
        
        while True:
            email = input('Entre com o e-mail do contato (q para sair): ')
            if email.lower() == 'q':
                break
            if dados.valida_email(email):
                contato_selecionado.lista_emails.append(email.lower())

        if 'Ativos' in contato_selecionado.tags:
            excluir = input('contato ativo. Excluir (s ou n)?')
            if excluir.lower() == 's':
                self.inativar_contato(contato_selecionado)
        else:
            ativar = input('contato inativo. Ativar (s ou n)?')
            if ativar.lower() == 's':
                self.ativar_contato(contato_selecionado)
        contato_selecionado.nome = nome.lower()
        contato_selecionado.sobrenome = sobrenome.lower()


    def altera_telefone(self, contato_selecionado):
        '''
        Pede ao usuário novo valor para todos os telefones do contato selecionado.
        Se o usuário não entrar com nenhum valor, permanece o valor existente
        '''
        for tel in contato_selecionado.lista_telefones:
            telefone = input(f'Entre com o novo telefone (q para sair) [({tel[-11:-9]}) {tel[-9:-8]} {tel[-8:-4]}-{tel[-4:]}]: ') or tel
            if telefone.lower() == 'q':
                break
            contato_selecionado.lista_telefones[contato_selecionado.lista_telefones.index(tel)] = telefone


    def altera_email(self, contato_selecionado):
        '''
        Pede ao usuário novo valor para todos os emails do contato selecionado.
        Se o usuário não entrar com nenhum valor, permanece o valor existente
        '''
        for email in contato_selecionado.lista_emails:
            novo_email = input(f'Entre com o novo E-mail [{email}]: ') or email
            if email.lower() == 'q':
                break
            contato_selecionado.lista_emails[contato_selecionado.lista_emails.index(email)] = novo_email


    def exclui_contato(self):
        '''
        Muda o contato do grupo Ativos para Inativos
        '''
        opt = input('\n1. Excluir contato definitivamente\n2. Mover contato para Inativos\n3. Sair')
        contato_selecionado = self.seleciona_contato('Ativos')
        if opt == '1':
            self.purge_contato(contato_selecionado)
            self.contatos_ativos -= 1
            self.contatos_totais -= 1
        if opt == '2':
            self.inativar_contato(contato_selecionado)
            self.contatos_ativos -= 1
        if opt == '3':
            pass


    def purge_contato(self, contato_selecionado):
        '''
        exclui definitavivamente o contato
        '''
        self.contatos.remove(contato_selecionado)


    def inativar_contato(self, contato_selecionado):
            contato_selecionado.tags.discard('Ativos')
            contato_selecionado.tags.add('Inativos')
            self.contatos_ativos -= 1
            print(contato_selecionado.tags)


    def ativar_contato(self, contato_selecionado):
            contato_selecionado.tags.discard('Inativos')
            contato_selecionado.tags.add('Ativos')
            self.contatos_ativos += 1
            print(contato_selecionado.tags)    


    def pesquisa_contato(self):
        '''
        Pesquisa a lista de contatos e busca pelo string digitado pelo usuário
        '''
        opt = input('Qual contato vc está buscando: ')
        counter = 0
        for contato in self.contatos:
            busca_exata = contato.nome + ' ' + contato.sobrenome
            if opt in contato.nome or opt in busca_exata or opt in contato.sobrenome or opt in contato.lista_telefones or opt in contato.lista_emails:
                print(f'{contato.ID}.\tNome: {contato.nome.title()}')
                print(f'\tSobrenome: {contato.sobrenome.title()}')
                for index, tel in enumerate(contato.lista_telefones):
                    print(f'\tTelefone {index + 1}: ({tel[-11:-9]}) {tel[-9:-8]} {tel[-8:-4]}-{tel[-4:]}')
                for index, email in enumerate(contato.lista_emails):
                    print(f'\tE-mail {index + 1}: {email}')
            else:
                counter += 1
        if counter == len(self.contatos):
                print('não encontrado')


    def cria_grupo(self):
        '''
        Cria um novo grupo para classificar contatos
        '''
        nome_grupo = input('Entre com o nome do grupo de pesquisa a ser criado: ')
        self.grupos.add(nome_grupo)
        print(f'Grupo {nome_grupo} criado com sucesso!')


    def inlui_exclui_contato_em_grupo(self):
        '''
        Seleciona um contato, se a opção é incluir ou excluir e um grupo de classificação.
        Chama função para incluir ou excluir o contato selecionado no grupo escolhido
        '''

        contato_selecionado = self.seleciona_contato('Todos')
        opt = input('Inluir ou exlcuir Contato de grupo (I ou E): ')
        if opt.lower() == 'i':
            tag = self.seleciona_grupo()
            self.inclui_contato_no_grupo(contato_selecionado, tag)
        if opt.lower() == 'e':
            tag = self.seleciona_grupo_de_contato(contato_selecionado)
            self.exclui_contato_do_grupo(contato_selecionado, tag) 


    def inclui_contato_no_grupo(self, contato_selecionado, tag):
        '''
        inclui um contato em um dos grupos de classificação
        '''
        contato_selecionado.tags.add(tag)
        print(contato_selecionado.tags)
        print('contato {contato_selecionado} incluído no grupo {tag}!')


    def exclui_contato_do_grupo(self, contato_selecionado, tag):
        '''
        exclui um contato do grupo de classificação
        '''
        if tag == 'Ativos' or tag == 'Inativo' or tag == 'Todos':
            print('Impossível excluir de grupo primário.\nPara exlcuir definitivamente ou mover para Inativo, escolha a opção 3. excluir\nPara reativar contato, escolha a opção 2. Alterar contato')
        else:
            contato_selecionado.tags.discard(tag)
            print('contato {contato_selecionado} excluído do grupo {tag}!')        


    def lista_contatos(self, *grupo):
        '''
        lista os contatos do grupo de classificação selecionado
        '''
        try:
            opt = grupo[0]
        except:
            opt = False

        if opt:
            self.imprime_contatos(opt)
        else:
            opt = self.seleciona_grupo()
            self.imprime_contatos(opt)


    def seleciona_grupo(self):
        '''
        seleciona um grupo de contatos
        '''
        lista_aux = list(sorted(self.grupos))

        for index, grupo in enumerate(lista_aux):
            print(f'{index + 1}. {grupo.title()}')
        
        while True:
            try:
                opt = int(input('Escolha o grupo (ou 0 para sair): '))
                print(opt)
                if opt <= 0 or opt > len(grupo):
                    print('Escolha Inválida!')
                    break
                else:
                    print(lista_aux[opt - 1])
                    return lista_aux[opt - 1]
            
            except:
                print('Entrada Inválida.')



    def seleciona_grupo_de_contato(self, contato_selecionado):
        '''
        seleciona um grupo em que o contato está incluído
        '''
        lista_aux = sorted(list(contato_selecionado.tags))

        for index, tag in enumerate(lista_aux):
            print(f'{index + 1}. {tag.title()}')
        
        while True:
            try:
                opt = int(input('Escolha o grupo (ou 0 para sair): '))
                print(opt)
                if opt <= 0 or opt > len(tag):
                    print('saindo')
                    break
                else:
                    print(lista_aux[opt - 1])
                    return lista_aux[opt - 1]
            
            except:
                print('Entrada Inválida.')


    def imprime_contatos(self, opt):
        print(opt)
        print(f'--------------------AGENDA: {self.nome_agenda}--------------------')
        print('------------------------CONTATOS------------------------')
        print(f'------------------------{opt}--------------------------')
        print('ID'.ljust(3),' ','Nome')
        for contato in self.contatos:
            for tag in contato.tags:
                if tag == opt:
                    print(f'{contato.ID}','-',contato.nome.title(),contato.sobrenome.title())
        print('-------------------------------------------------------')


    def seleciona_contato(self, grupo):
        '''
        seleciona um contato
        '''
        self.lista_contatos(grupo)
       
        while True:
            try:
                opt = int(input('Selecione o contato: '))
                counter = 0
                for contato in self.contatos:
                    if opt == int(contato.ID) and grupo in contato.tags:
                        counter += 1
                        return contato
                if counter == 0:
                    print('Contato não encontrado!')
                    
            except:
                print('Entrada Inválida. Selecione um contato!')     


    def seleciona_csv(self):
        '''
        seleciona um arquivo .csv do diretório
        '''
        onlyfiles = backup.le_diretorio()
        print(f'--------------Arquivos .csv---------------')
        for file in onlyfiles:
            print(f'{onlyfiles.index(file) + 1}. {file}')
        opt = int(input('Selecione o arquivo: '))
        return (onlyfiles[opt - 1])

    
class Contato():
    def __init__(self, ID, nome, lista_telefones, lista_emails, sobrenome=''):
        '''
        Inicializa um objeto da classe Contato
        '''
        self.ID = ID
        self.nome = nome
        self.sobrenome = sobrenome
        self.lista_telefones = lista_telefones
        self.lista_emails = lista_emails
        self.tags = set()


def main():
    '''
    Função principal, que inicializa o sistema.
    Pede ao usuário uma opção do Menu e chama as funções conforme a opção escolhida
    '''
    verifica_diretorios()
    carrega_agendas()

    while True:
        opt = input('\n1. Cadastrar agenda: \n2. Acessar agenda: \n3. Listar agendas\n4. Pesquisar agendas\n5. Exclui agenda\n0. Sair\n')
        if opt == '1':
            cria_agenda()
        elif opt == '2':
            acessa_agenda()
        elif opt == '3':
            lista_agendas()
        elif opt == '4':
            busca_agendas()
        elif opt == '5':
            exclui_agenda()
        elif opt == '0':
            print('Saindo do sistema. Até logo!')
            break
        else:    
            print('Opção inválida')


def verifica_diretorios():
    '''
    verifica se o diretorio arquivos existe
    Se não existir, cria um
    '''
    caminho = 'arquivos/'
    if os.path.isdir(caminho):
        print('Diretório arquivos já existe')
    else:
        os.makedirs(caminho)
        print('diretório arquivos criado')


def cria_agenda():
    '''
    Pede ao usuário um valor para o atributo nome e cria um objeto Agenda com este atributo
    '''
    while True:
        nome_agenda = input('Entre com o nome da agenda (0 para sair): ')
        if nome_agenda != '0':
            cria_csv(nome_agenda)
            cria_objeto_agenda(nome_agenda)
        else:
            break

def cria_csv(nome_agenda):
    '''
    cria arquvo csv para armazenar uma agenda
    '''
    onlyfiles = backup.le_diretorio()
    if nome_agenda not in onlyfiles: 
        backup.criar(nome_agenda)
    else:
        print(f'Agenda {nome_agenda} já existe')
    

def cria_objeto_agenda(nome_agenda):
    '''
    cria o objeto agenda que vai acessar um arquivo csv com uma agenda armazenada
    '''
    print('criando agenda', nome_agenda)
    nome_agenda = nome_agenda.split('.')[0]
    if nome_agenda not in Agenda.agendas:
        agenda = Agenda(nome_agenda)
        Agenda.agendas.append(agenda) 
        print(f'Objeto Agenda.{nome_agenda[0:nome_agenda.find(".")]} criado!')
        return agenda
    else:
        print('Agenda já existe')


def carrega_agendas():
    '''
    Carrega as agendas existentes no sistema
    '''
    onlyfiles = backup.le_diretorio()
    for file in onlyfiles:
        agenda = cria_objeto_agenda(file)
        lista_contatos = backup.importar(file, agenda)
        if lista_contatos:
            agenda.cadastra_contatos(file, lista_contatos)


def acessa_agenda():
    '''
    Acessa a agenda selecionada pelo usuário
    '''
    opt = seleciona_agenda()
    while True:
        if opt == -100:
            break
        elif opt > len(Agenda.agendas) or opt < 1:
            opt = int(input('Tente de novo. Selecione a agenda: '))
        else:    
            Agenda.agendas[opt-1].menu_agenda()
            break


def seleciona_agenda():
    '''
    Exibe a lista das agendas cadastradas e pede ao usuário que selecione uma
    '''
    if len(Agenda.agendas) == 0:
        print('Não existem agendas cadastradas.')
        return -100
    else:
        print('---------AGENDAS---------')
        for agenda in Agenda.agendas:
            print(f'{Agenda.agendas.index(agenda)+1}: {agenda.nome_agenda.title()}')
        print('-------------------------\n')
        while True:
            try:
                opt = int(input('Selecione a agenda: '))
                break
            except:
                print('Opção inválida.')   
        return opt 
        
    
def lista_agendas():
    '''
    lista as agendas cadastradas
    '''
    if len(Agenda.agendas) == 0:
        print('Não existem agendas cadastradas.')
    else:
        print('--------------------AGENDAS--------------------')
        for agenda in Agenda.agendas:
            print(f'{Agenda.agendas.index(agenda)+1}: {agenda.nome_agenda.title()} - contatos ativos: {agenda.contatos_ativos}, contatos totais: {agenda.contatos_totais}')
        print('-----------------------------------------------\n')


def busca_agendas():
    '''
    Pesquisa as agendas cadastradas através de um string digitado pelo usuário
    '''
    opt = input('Qual agenda vc está buscando: ')
    counter = 0
    for agenda in Agenda.agendas:
        if opt in agenda.nome_agenda:
            print(f'{Agenda.agendas.index(agenda)+1}.\tNome: {agenda.nome_agenda.title()} - contatos ativos: {agenda.contatos_ativos}, contatos totais: {agenda.contatos_totais} ')
        else:
            counter += 1
        if counter == len(Agenda.agendas):
            print('não encontrada')


def exclui_agenda():
    '''
    Exclui agenda
    '''
    opt = seleciona_agenda()
    while True:
        if opt == -100:
            break
        excluir = input(f'Tem certeza que deseja excluir a agenda {Agenda.agendas[opt - 1].nome_agenda} (s ou n)?')
        if excluir.lower() == "s":
            os.remove('arquivos/' + Agenda.agendas[opt - 1].nome_agenda + '.csv')
            Agenda.agendas.remove(Agenda.agendas[opt - 1])
            break
        else:
            print('A agenda não será excluída!')
            break
        

#chama a função main e inicializa o sistema 
main()