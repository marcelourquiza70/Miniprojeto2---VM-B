import csv
    
class backup:
    @staticmethod
    def importar(nome_arquivo):
        '''Lê um arquivo .csv e retorna seu conteúdo em uma lista de listas
        '''
        try:
            arquivo = open(nome_arquivo, "r", encoding="utf-8")
            lista_csv = csv.reader(arquivo, delimiter=";", lineterminator="\n")
            lista_contatos = []
        
            for contato in lista_csv:
                lista_contatos.append(contato)
            
            arquivo.close()
            
            return lista_contatos

        except:
            print('\nArquivo de backup (contatos.csv) não encontrado.\n')

    @staticmethod
    def exportar(nome_arquivo, lista_contatos):
        '''Exporta a lista de contatos para arquivo .csv'''
        
        arquivo = open(nome_arquivo, "w", encoding="utf-8")
        csv.writer(arquivo, delimiter=';', lineterminator='\n').writerows(lista_contatos)
        arquivo.close()
        
        print(f"A lista de contatos foi exportada para o arquivo: {arquivo} .")
        
        return

class dados:
    @staticmethod
    def valida_nome(nome):
        while True:
            #verifica se o nome é composto apenas por letras
            if "".join(nome.split(' ')).isalpha():
                return True
            else:
                print('O nome deve conter apenas letras.')
                return False

    @staticmethod
    def valida_telefone(telefone):
        #verifica se o telefone é composto apenas por números
        while True:
            if telefone.isnumeric():
                return True
            else:
                print('O telefone deve conter apenas números.')
                return False
    
    @staticmethod
    def valida_email(email):
        #verifica se o email contém um domínio
        while True:
            if '@' in email and '.' in email and email[-1] != '.':
                return True
            else:
                print('O email deve conter um domínio válido (@).')
                return False

    @staticmethod
    def requisita_dados():
        
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
                print(lista_telefones)

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
        self.nome_agenda = nome_agenda
        self.contatos_ativos = 0
        self.contatos_totais = 0
        self.contatos = []
        self.grupos = []

    def menu_agenda(self):
        while True:
            opt = input('1. Cadastrar contato: \n2. Alterar contato: \n3. Exclui contato\n4. Listar contatos\n5. Pesquisar contato\n6. Criar grupo\n7. Incluir/Exluir contato em grupo\n8. Listar Contatos de grupo\n9. Importar backup de contatos\n0. Sair\n')
            
            if opt == '1':
                nome, lista_telefones, lista_emails, sobrenome = dados.requisita_dados()
                self.cadastra_contato(nome, lista_telefones, lista_emails, sobrenome)
                
            elif opt == '2':
                self.altera_contato()
            elif opt == '3':
                self.exclui_contato()
            elif opt == '4':
                opt = '1' #input('1.Ativos\n2.Inativos\n3.Todos\n')
                self.lista_contatos(opt)
            elif opt == '5':
                self.busca_contato()
            elif opt == '6':
                self.cria_grupo()
            elif opt == '7':
                self.inclui_contato_no_grupo()
            elif opt == '8':
                self.listar_contatos_de_grupo()
            elif opt == '9':
                lista_contatos = backup.importar('contatos.csv')
                for contato in lista_contatos:
                    self.cadastra_contato(contato[0],contato[1],contato[2])
                print(f'{len(lista_contatos)} contatos importados com sucesso.')
            elif opt == '0':
                print('Voltando para menu de agendas!')
                break
            else:    
                print('Opção inválida')


    def cadastra_contato(self, nome, lista_telefones, lista_emails, sobrenome = ''):
        if self.contatos_ativos < 30:
            id = self.contatos_totais + 1
            self.contatos_totais += 1
            self.contatos_ativos += 1
            contato = Contato(id, nome, lista_telefones, lista_emails, sobrenome)
            self.contatos.append(contato)
            #self.conta_ativos()
        else:
            opt = input('Agenda cheia. Excluir uma entrada (s ou n)?')
            if opt.lower() == 's':
                self.exclui_contato()
                self.cadastra_contato()


    def altera_contato(self):
        opt = input('1.Ativos\n2.Inativos\n3.Todos\n')
        contato_selecionado = self.seleciona_contato(opt)
        nome = input(f'Entre com o nome do contato [{contato_selecionado.nome}]: ') or contato_selecionado.nome
        sobrenome = input(f'Entre com o sobrenome do contato [{contato_selecionado.sobrenome}]: ') or contato_selecionado.sobrenome
        self.altera_telefone(contato_selecionado)
        self.altera_email(contato_selecionado)
        if contato_selecionado.ativo:
            excluir = input('contato ativo. Excluir (s ou n)?')
            if excluir.lower() == 's':
                contato_selecionado.ativo = False
        else:
            ativar = input('contato inativo. Ativar (s ou n)?')
            if ativar.lower() == 's':
                contato_selecionado.ativo = True
        contato_selecionado.nome = nome.lower()
        contato_selecionado.sobrenome = sobrenome.lower()


    def cria_grupo(self):
        nome_grupo = input('Entre com o nome do grupo de pesquisa a ser criado: ')
        self.grupos.append(nome_grupo)
        print('Grupo {nome_grupo} criado com sucesso!')


    def inlui_exclui_contato_em_grupo(self):
        opt = input('Inluir ou exlcuir Contato de grupo (I ou E): ')
        if opt.lower() == 'i':
            lista_grupos(self)
            tag = input('Selecione grupo a incluir: ')
            inclui_contato_no_grupo(self, self.tags[tag]) 


    def inclui_contato_no_grupo(self, tag):
        self.tags.append(self.tags[tag])
        print('contato {self.nome} incluído no grupo {self.tags[tag]}!')


    def exclui_contato_do_grupo(self, tag):
        self.tags.remove(tag)
        print('contato {self.nome} excluído do grupo {tag}!')        


    def lista_grupos(self):
        print('Código do grupo\tNome do Grupo')
        for indice, grupo in enumerate(self.grupos):
            print(f'{indice + 1}.\t{grupo}')


    def listar_contato_de_grupo():
        lista_grupos(self)
        opt = input('Escolha o grupo a listar: ')
        print(f'--------------------AGENDA: {self.nome_agenda}--------------------')
        print('------------------------CONTATOS------------------------')
        print(f'------------------------{self.grupo[opt - 1]}--------------------------')
        print('ID'.ljust(3),' ','Nome')
        for contato in self.contatos:
            if contato.tags == self.grupo[opt - 1]:
                print(f'{contato.ID:3d}','-',contato.nome,contato.sobrenome)
        print('-------------------------------------------------------')


    def exclui_contato(self):
        opt = self.seleciona_contato('1')
        opt.ativo = False
        self.contatos_ativos -= 1


    def seleciona_contato(self, opt):
        self.lista_contatos(opt)
        opt = int(input('Selecione o contato: '))
        while True:
            if opt > len(self.contatos) or opt < 1:
                opt = int(input('Tente de novo. Selecione o contato: '))
            else:    
                return self.contatos[opt-1]
                break


#    def seleciona_telefone(self, contato_selecionado):
#        for tel in contato_selecionado.lista_telefones:
#                    print(f'\tTelefone {contato_selecionado.lista_telefones.index(tel)+1}: {tel}')
#        opt = int(input('Selecione o telefone: '))
#        while True:
#            if opt > len(contato_selecionado.lista_telefones) or opt < 1:
#                opt = int(input('Tente de novo. Selecione o telefone: '))
#            else:    
#                return opt
#                break


    def altera_telefone(self, contato_selecionado):
        for tel in contato_selecionado.lista_telefones:
            telefone = input(f'Entre com o novo telefone (q para sair) [({tel[-11:-9]}) {tel[-9:-8]} {tel[-8:-4]}-{tel[-4:]}]: ') or tel
            if telefone.lower() == 'q':
                break
            contato_selecionado.lista_telefones[contato_selecionado.lista_telefones.index(tel)] = telefone


#    def seleciona_email(self, contato_selecionado):
#        for email in contato_selecionado.lista_emails:
#                    print(f'\tE-mail {contato_selecionado.lista_emails.index(email)+1}: {email}')
#        opt = int(input('Selecione o E-mail: '))
#        if opt.lower() == 'q':
#                break
#        while True:
#            if opt > len(contato_selecionado.lista_emails) or opt < 1:
#                opt = int(input('Tente de novo. Selecione o E-mail: '))
#            else:    
#                return opt
#                break


    def altera_email(self, contato_selecionado):
        for email in contato_selecionado.lista_emails:
            novo_email = input(f'Entre com o novo E-mail [{email}]: ') or email
            if email.lower() == 'q':
                break
            contato_selecionado.lista_emails[contato_selecionado.lista_emails.index(email)] = novo_email


    def busca_contato(self):
        opt = input('Qual contato vc está buscando: ')
        counter = 0
        for contato in self.contatos:
            busca_exata = contato.nome + ' ' + contato.sobrenome
            if opt in contato.nome or opt in busca_exata or opt in contato.sobrenome or opt in contato.telefone or opt in contato.email:
                print(f'{contato.ID}.\tNome: {contato.nome.title()}')
                print(f'\tSobrenome: {contato.sobrenome.title()}')
                for tel in contato.lista_telefones:
                    print(f'\tTelefone {contato.lista_telefones.index(tel)+1}: ({tel[-11:-9]}) {tel[-9:-8]} {tel[-8:-4]}-{tel[-4:]}')
                for email in contato.lista_emails:
                    print(f'\tE-mail {contato.lista_emails.index(email)+1}: {email}')
            else:
                counter += 1
        if counter == len(self.contatos):
                print('não encontrado')
    
        
    def lista_contatos(self, opt):
        #opt = input('1.Ativos\n2.Inativos\n3.Todos\n')
        print(f'--------------------AGENDA: {self.nome_agenda}--------------------')
        print('------------------------CONTATOS------------------------')
        
        print('ID'.ljust(3),' ','Nome')
        for contato in self.contatos:
            if opt == '1' and contato.ativo:
                print(f'{contato.ID:3d}','-',contato.nome,contato.sobrenome)
                #print(f'{contato.ID:<}\t{contato.nome.title():<}\t{contato.sobrenome.title():<}\t({contato.telefone[0][-11:-9]:<}) {contato.telefone[0][-9:-8]:<} {contato.telefone[0][-8:-4]:<}-{contato.telefone[0][-4:]:<}\t{contato.email[0]:<}')
            elif opt == '2' and contato.ativo == False:
                print(f'{contato.ID:3d}','-',contato.nome,contato.sobrenome)
                #print(f'{contato.ID}\t{contato.nome.title()}\t{contato.sobrenome.title()}\t({contato.telefone[-11:-9]}) {contato.telefone[-9:-8]} {contato.telefone[-8:-4]}-{contato.telefone[-4:]}\t{contato.email[0]}')
            elif opt == '3':
                print(f'{contato.ID:3d}','-',contato.nome,contato.sobrenome)
                #print(f'{contato.ID}\t{contato.nome.title()}\t{contato.sobrenome.title()}\t({contato.telefone[-11:-9]}) {contato.telefone[-9:-8]} {contato.telefone[-8:-4]}-{contato.telefone[-4:]}\t{contato.email[0]}')
        print('-------------------------------------------------------')


 #   def conta_ativos(self):
 #       self.contatos_ativos = 0
 #       for contato in self.contatos:
 #           if contato.ativo:
 #               self.contatos_ativos += 1


class Contato():
    def __init__(self, id, nome, lista_telefones, lista_emails, sobrenome=''):
        self.ID = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.lista_telefones = lista_telefones
        self.lista_emails = lista_emails
        self.ativo = True
        self.tags = []


def main():
    while True:
        opt = input('1. Cadastrar agenda: \n2. Acessar agenda: \n3. Listar agendas\n4. Pesquisar agendas\n5. Sair\n')
        if opt == '1':
            cria_agenda()
        elif opt == '2':
            seleciona_agenda()
        elif opt == '3':
            lista_agendas()
        elif opt == '4':
            busca_agendas()
        elif opt == '5':
            print('Saindo do sistema. Até logo!')
            break
        else:    
            print('Opção inválida')

def cria_agenda():
    nome_agenda = input('Entre com o nome da agenda: ')
    agenda = Agenda(nome_agenda)
    Agenda.agendas.append(agenda)
    print(f'Agenda {nome_agenda} criada')


def seleciona_agenda():

    if len(Agenda.agendas) == 0:
        print('Não existem agendas cadastradas.')
    else:
        print('---------AGENDAS---------')
        for agenda in Agenda.agendas:
            print(f'{Agenda.agendas.index(agenda)+1}: {agenda.nome_agenda}')
        print('-------------------------\n')
        opt = int(input('Selecione a agenda: '))
        
        while True:
            if opt > len(Agenda.agendas) or opt < 1:
                opt = int(input('Tente de novo. Selecione a agenda: '))
            else:    
                Agenda.agendas[opt-1].menu_agenda()
                break

def lista_agendas():
    if len(Agenda.agendas) == 0:
        print('Não existem agendas cadastradas.')
    else:
        print('----------AGENDAS----------')
        for agenda in Agenda.agendas:
            print(f'{Agenda.agendas.index(agenda)+1}: {agenda.nome_agenda.title()} - contatos ativos: {agenda.contatos_ativos}, contatos totais: {agenda.contatos_totais}')
            print('---------------------------\n')


def busca_agendas():
        opt = input('Qual agenda vc está buscando: ')
        counter = 0
        for agenda in Agenda.agendas:
            if opt in agenda.nome_agenda:
                print(f'{Agenda.agendas.index(agenda)+1}.\tNome: {agenda.nome_agenda.title()} - contatos ativos: {agenda.contatos_ativos}, contatos totais: {agenda.contatos_totais} ')
            else:
                counter += 1
        if counter == len(Agenda.agendas):
                print('não encontrada')
main()
