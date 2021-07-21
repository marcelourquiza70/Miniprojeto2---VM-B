class Agenda:
    
    agendas = []

    def __init__(self, nome_agenda):
        self.nome_agenda = nome_agenda
        self.contatos_ativos = 0
        self.contatos_totais = 0
        self.contatos = []

    def menu_agenda(self):
        while True:
            opt = input('1. Cadastrar contato: \n2. Alterar contato: \n3. Exclui contato\n4. Listar contatos\n5. Pesquisar contato\n6. Sair\n')
            if opt == '1':
                self.cadastra_contato()
            elif opt == '2':
                self.altera_contato()
            elif opt == '3':
                self.exclui_contato()
            elif opt == '4':
                opt = input('1.Ativos\n2.Inativos\n3.Todos\n')
                self.lista_contatos(opt)
            elif opt == '5':
                self.busca_contato()
            elif opt == '6':
                print('Voltando para menu de agendas!')
                break
            else:    
                print('Opção inválida')


    def cadastra_contato(self):
        if self.contatos_ativos < 10:
            nome = input('Entre com o nome do contato: ')
            sobrenome = input('Entre com o sobrenome do contato: ') or ''
            telefone = input('Entre com o telefone do contato: ')
            email = input('Entre com o E-mail do contato: ')
            id = self.contatos_totais + 1
            self.contatos_totais += 1
            self.contatos_ativos += 1
            contato = Contato(id, nome.lower(), telefone, email.lower(), sobrenome.lower())
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
        telefone = input(f'Entre com o telefone do contato [{contato_selecionado.telefone}]: ') or contato_selecionado.telefone
        email = input(f'Entre com o email do contato [{contato_selecionado.email}]: ') or contato_selecionado.email
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
        contato_selecionado.telefone = telefone
        contato_selecionado.email = email.lower()


#    def testa_nome(self):
#        if self.nome isalpha:


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
                
                
    def busca_contato(self):
        opt = input('Qual contato vc está buscando: ')
        counter = 0
        for contato in self.contatos:
            busca_exata = contato.nome + ' ' + contato.sobrenome
            if opt in contato.nome or opt in busca_exata or opt in contato.sobrenome or opt in contato.telefone or opt in contato.email:
                print(f'{contato.ID}.\tNome: {contato.nome.title()}')
                print(f'\tSobrenome: {contato.sobrenome.title()}')
                print(f'\tTelefone: {contato.telefone}')
                print(f'\tE-mail: {contato.email.title()}')
            else:
                counter += 1
        if counter == len(self.contatos):
                print('não encontrado')
    
        
    def lista_contatos(self, opt):
        #opt = input('1.Ativos\n2.Inativos\n3.Todos\n')
        print(f'--------------------AGENDA: {self.nome_agenda}--------------------')
        print(f'------------------------CONTATOS------------------------')
        print(f'Id\tNome\tSobrenome\tTelefone\tE-mail')
        for contato in self.contatos:
            if opt == '1' and contato.ativo:
                print(f'{contato.ID:<}\t{contato.nome.title():<}\t{contato.sobrenome.title():<}\t({contato.telefone[-11:-9]:<}) {contato.telefone[-9:-8]:<} {contato.telefone[-8:-4]:<}-{contato.telefone[-4:]:<}\t{contato.email.title():<}')
            elif opt == '2' and contato.ativo == False:
                print(f'{contato.ID}\t{contato.nome.title()}\t{contato.sobrenome.title()}\t({contato.telefone[-11:-9]}) {contato.telefone[-9:-8]} {contato.telefone[-8:-4]}-{contato.telefone[-4:]}\t{contato.email.title()}')
            elif opt == '3':
                print(f'{contato.ID}\t{contato.nome.title()}\t{contato.sobrenome.title()}\t({contato.telefone[-11:-9]}) {contato.telefone[-9:-8]} {contato.telefone[-8:-4]}-{contato.telefone[-4:]}\t{contato.email.title()}')
        print('-------------------------------------------------------')


 #   def conta_ativos(self):
 #       self.contatos_ativos = 0
 #       for contato in self.contatos:
 #           if contato.ativo:
 #               self.contatos_ativos += 1


class Contato():
    def __init__(self, id, nome, telefone, email, sobrenome=''):
        self.ID = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone
        self.email = email
        self.ativo = True


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