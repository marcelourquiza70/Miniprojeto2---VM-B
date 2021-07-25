import csv
    
class backup:
    @staticmethod
    def importar(nome_arquivo):
        '''
        Lê um arquivo .csv e retorna seu conteúdo em uma lista de listas
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
        '''
        Exporta a lista de contatos para arquivo .csv
        '''
        
        arquivo = open(nome_arquivo, "w", encoding="utf-8")
        csv.writer(arquivo, delimiter=';', lineterminator='\n').writerows(lista_contatos)
        arquivo.close()
        
        print(f"A lista de contatos foi exportada para o arquivo: {arquivo} .")
        
        return

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
        '''
        cria objeto Agenda
        '''
        self.nome_agenda = nome_agenda
        self.contatos_ativos = 0
        self.contatos_totais = 0
        self.contatos = []
        self.grupos = ['Ativos', 'Inativos', 'Todos']

    def menu_agenda(self):
        '''
        Menu da agenda
        '''
        while True:
            opt = input('1. Cadastrar contato: \n2. Alterar contato: \n3. Exclui contato\n4. Listar contatos\n5. Pesquisar contato\n6. Criar grupo\n7. Incluir/Exluir contato em grupo\n8. Listar Contatos de grupo\n9. Importar backup de contatos\n0. Sair\n')
            
            if opt == '1':
                nome, lista_telefones, lista_emails, sobrenome = dados.requisita_dados()
                self.cadastra_contato(nome, lista_telefones, lista_emails, sobrenome)
                
            elif opt == '2':
                self.altera_contato()
            elif opt == '3':
                contato_selecionado = self.seleciona_contato('1')
                self.inativar_contato(contato_selecionado)
            elif opt == '4':
                opt = '1' #input('1.Ativos\n2.Inativos\n3.Todos\n')
                self.lista_contatos(opt)
            elif opt == '5':
                self.pesquisa_contato()
            elif opt == '6':
                self.cria_grupo()
            elif opt == '7':
                self.inlui_exclui_contato_em_grupo()
            elif opt == '8':
                self.lista_contatos()
            elif opt == '9':
                lista_contatos = backup.importar('contatos.csv')
                for contato in lista_contatos:
                    self.cadastra_contato(nome = contato[0].lower(), lista_telefones = list([contato[1]]), lista_emails = list([contato[2]]))
                print(f'{len(lista_contatos)} contatos importados com sucesso.')
            elif opt == '0':
                print('Voltando para menu de agendas!')
                break
            else:    
                print('Opção inválida')


    def cadastra_contato(self, nome, lista_telefones, lista_emails, sobrenome = ''):
        '''
        testa se a agenda tem espaço e se, tiver, cadastra um novo contato.
        Se a agenda estiver cheia, te pergunta se quer excluir algum contato existente
        '''
        if self.contatos_ativos < 30:
            id = self.contatos_totais + 1
            self.contatos_totais += 1
            self.contatos_ativos += 1
            contato = Contato(id, nome, lista_telefones, lista_emails, sobrenome)
            self.contatos.append(contato)
            contato.tags.append('Ativos')
            contato.tags.append('Todos')
        else:
            opt = input('Agenda cheia. Excluir uma entrada (s ou n)?')
            if opt.lower() == 's':
                self.exclui_contato()
                self.cadastra_contato()


    def altera_contato(self):
        '''
        seleciona um contato e pede um novo valor ao usuário
        '''
        opt = input('1.Ativos\n2.Inativos\n3.Todos\n')
        contato_selecionado = self.seleciona_contato(opt)
        nome = input(f'Entre com o nome do contato [{contato_selecionado.nome}]: ') or contato_selecionado.nome
        sobrenome = input(f'Entre com o sobrenome do contato [{contato_selecionado.sobrenome}]: ') or contato_selecionado.sobrenome
        self.altera_telefone(contato_selecionado)
        self.altera_email(contato_selecionado)
        if 'Ativo' in contato_selecionado.tags:
            excluir = input('contato ativo. Excluir (s ou n)?')
            if excluir.lower() == 's':
                self.inativar_contato(self, contato_selecionado)
        else:
            ativar = input('contato inativo. Ativar (s ou n)?')
            if ativar.lower() == 's':
                self.ativar_contato(self, contato_selecionado)
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
        Altera o atributo ativo para False
        '''
        opt = self.seleciona_contato('1')
        opt.ativo = False
        self.contatos_ativos -= 1


    def inativar_contato(self, contato_selecionado):
            contato_selecionado.tags.remove('Ativos')
            contato_selecionado.tags.append('Inativos')
            self.contatos_ativos -= 1
            print(contato_selecionado.tags)


    def ativar_contato(self, contato_selecionado):
            contato_selecionado.tags.remove('Inativos')
            contato_selecionado.tags.append('Ativos')
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
                for tel in contato.lista_telefones:
                    print(f'\tTelefone {contato.lista_telefones.index(tel)+1}: ({tel[-11:-9]}) {tel[-9:-8]} {tel[-8:-4]}-{tel[-4:]}')
                for email in contato.lista_emails:
                    print(f'\tE-mail {contato.lista_emails.index(email)+1}: {email}')
            else:
                counter += 1
        if counter == len(self.contatos):
                print('não encontrado')


    def cria_grupo(self):
        '''
        Cria um novo grupo para classificar contatos
        '''
        nome_grupo = input('Entre com o nome do grupo de pesquisa a ser criado: ')
        self.grupos.append(nome_grupo)
        print(f'Grupo {nome_grupo} criado com sucesso!')


    def inlui_exclui_contato_em_grupo(self):
        '''
        Seleciona um contato, se a opção é incluir ou excluir e um grupo de classificação.
        Chama função para incluir ou excluir o contato selecionado no grupo escolhido
        '''
        contato_selecionado = self.seleciona_contato('1')
        opt = input('Inluir ou exlcuir Contato de grupo (I ou E): ')
        if opt.lower() == 'i':
            self.lista_grupos()
            tag = input('Selecione grupo a incluir: ')
            self.inclui_contato_no_grupo(contato_selecionado, tag)
        if opt.lower() == 'e':
            self.lista_grupos()
            tag = input('Selecione grupo a excluir: ')
            self.exclui_contato_do_grupo(contato_selecionado, tag) 


    def inclui_contato_no_grupo(self, contato_selecionado, tag):
        '''
        inclui um contato em um dos grupos de classificação
        '''
        contato_selecionado.tags.append(self.grupos[int(tag) - 1])
        print(contato_selecionado.tags)
        print('contato {contato_selecionado} incluído no grupo {self.tags[int(tag) - 1]}!')


    def exclui_contato_do_grupo(self, contato_selecionado, tag):
        '''
        exclui um contato do grupo de classificação
        '''
        contato_selecionado.tags.remove(contato_selecionado.tags[int(tag) - 1])
        print('contato {contato_selecionado} excluído do grupo {self.tags[int(tag) - 1]}!')        


    def lista_contatos(self, *opt):
        '''
        lista os contatos do grupo de classificação selecionado
        '''
        if opt:
            self.imprime_contatos(opt[0])
        else:
            self.lista_grupos()
            opt = input('Escolha o grupo a listar: ')
            self.imprime_contatos(opt)


    def imprime_contatos(self, opt):
        print(f'--------------------AGENDA: {self.nome_agenda}--------------------')
        print('------------------------CONTATOS------------------------')
        print(f'------------------------{self.grupos[int(opt) - 1]}--------------------------')
        print('ID'.ljust(3),' ','Nome')
        for contato in self.contatos:
            for tag in contato.tags:
                if tag == self.grupos[int(opt) - 1]:
                    print(f'{contato.ID:3d}','-',contato.nome,contato.sobrenome)
        print('-------------------------------------------------------')

    def lista_grupos(self):
        '''
        lista os grupos de classificação da Agenda
        '''
        print('Código do grupo\tNome do Grupo')
        for indice, grupo in enumerate(self.grupos):
            print(f'{indice + 1}.\t{grupo}')


    def seleciona_contato(self, opt):
        '''
        seleciona um contato
        '''
        self.lista_contatos(opt)
        opt = int(input('Selecione o contato: '))
        while True:
            if opt > len(self.contatos) or opt < 1:
                opt = int(input('Tente de novo. Selecione o contato: '))
            else:    
                return self.contatos[opt-1]
                break


class Contato():
    def __init__(self, id, nome, lista_telefones, lista_emails, sobrenome=''):
        '''
        Inicializa um objeto da classe Contato
        '''
        self.ID = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.lista_telefones = lista_telefones
        self.lista_emails = lista_emails
        self.ativo = True
        self.tags = []


def main():
    '''
    Função principal, que inicializa o sistema.
    Pede ao usuário uma opção do Menu e chama as funções conforme a opção escolhida
    '''
    while True:
        opt = input('1. Cadastrar agenda: \n2. Acessar agenda: \n3. Listar agendas\n4. Pesquisar agendas\n5. Exclui agenda\n0. Sair\n')
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

def cria_agenda():
    '''
    Pedo ao usuário um valor para o atributo nome e cria um objeto Agenda com este atributo
    '''
    nome_agenda = input('Entre com o nome da agenda (0 para sair): ')
    if nome_agenda != '0':
        agenda = Agenda(nome_agenda)
        Agenda.agendas.append(agenda)
        print(f'Agenda {nome_agenda} criada')


def acessa_agenda():
    '''
    Acessa a agenda selecionada pelo usuário
    '''
    opt = seleciona_agenda()
    while True:
        if opt > len(Agenda.agendas) or opt < 1:
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
    else:
        print('---------AGENDAS---------')
        for agenda in Agenda.agendas:
            print(f'{Agenda.agendas.index(agenda)+1}: {agenda.nome_agenda}')
        print('-------------------------\n')
        opt = int(input('Selecione a agenda: '))   
        return opt 
        
    
def lista_agendas():
    '''
    lista as agendas cadastradas
    '''
    if len(Agenda.agendas) == 0:
        print('Não existem agendas cadastradas.')
    else:
        print('----------AGENDAS----------')
        for agenda in Agenda.agendas:
            print(f'{Agenda.agendas.index(agenda)+1}: {agenda.nome_agenda.title()} - contatos ativos: {agenda.contatos_ativos}, contatos totais: {agenda.contatos_totais}')
            print('---------------------------\n')


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
        excluir = input(f'Tem certeza que deseja excluir a agenda {Agenda.agendas[opt - 1].nome_agenda} (s ou n)?')
        if excluir.lower() == "s":
            Agenda.agendas.remove(Agenda.agendas[opt - 1])
            break
        else:
            print('A agenda não será excluída!')
            break
        

#chama a função main e inicializa o sistema 
main()