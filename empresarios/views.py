from django.shortcuts import render
from .models import Empresas, Documento, Metricas
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse

@login_required(login_url='logar')
def cadastrar_empresa(request):
    if request.method == "GET":
        return render(request, 'cadastrar_empresa.html', {'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices })
   
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        tempo_existencia = request.POST.get('tempo_existencia')
        print(tempo_existencia)
        descricao = request.POST.get('descricao')
        data_final = request.POST.get('data_final')
        percentual_equity = request.POST.get('percentual_equity')
        estagio = request.POST.get('estagio')
        area = request.POST.get('area')
        publico_alvo = request.POST.get('publico_alvo')
        valor = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')

        if len(nome.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Nome é obrigatório')
            return redirect('/empresarios/cadastrar_empresa')
        
        if len(cnpj.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'CNPJ é obrigatório')
            return redirect('/empresarios/cadastrar_empresa')
        
        if len(site.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Site é obrigatório')
            return redirect('/empresarios/cadastrar_empresa')
      
       
        if tempo_existencia not in [chave for chave, _ in Empresas.tempo_existencia_choices]:           
             messages.add_message(request, constants.ERROR, 'Você deve escolher uma opção de tempo de existência válida')
             return redirect('/empresarios/cadastrar_empresa')

        
        if len(descricao.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Descrição é obrigatório')
            return redirect('/empresarios/cadastrar_empresa')
        
        if not data_final:
            messages.add_message(request, constants.ERROR, 'Data final é obrigatório')
            return redirect('/empresarios/cadastrar_empresa')
        
        if len(percentual_equity.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Percentual de equity é obrigatório')
            return redirect('/empresarios/cadastrar_empresa')
        
        if estagio not in dict(Empresas.estagio_choices):
            messages.add_message(request, constants.ERROR, 'Você deve escolher uma opção de estágio válida')
            return redirect('/empresarios/cadastrar_empresa')
        
        if area not in dict(Empresas.area_choices):
            messages.add_message(request, constants.ERROR, 'Você deve escolher uma opção de área válida')
            return redirect('/empresarios/cadastrar_empresa')
        
        if publico_alvo :
            messages.add_message(request, constants.ERROR, 'Insira um público alvo válido')
            return redirect('/empresarios/cadastrar_empresa')
        
        if len(valor.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Valor é obrigatório')
            return redirect('/empresarios/cadastrar_empresa')
        
        if pitch is None:
            messages.add_message(request, constants.ERROR, 'Pitch é obrigatório')
            return redirect('/empresarios/cadastrar_empresa')
        
        if logo is None:
            messages.add_message(request, constants.ERROR, 'Logo é obrigatório')
            return redirect('/empresarios/cadastrar_empresa') 
        
        MAX_FILE_SIZE = 1 * 1024 * 1024  # 2 MB em bytes


        if pitch and pitch.size > MAX_FILE_SIZE:
            messages.add_message(request, constants.ERROR, 'O arquivo de pitch não pode exceder 2 MB.')
            return redirect('/empresarios/cadastrar_empresa')

        if logo and logo.size > MAX_FILE_SIZE:
            messages.add_message(request, constants.ERROR, 'O arquivo de logo não pode exceder 2 MB.')
            return redirect('/empresarios/cadastrar_empresa')


        
        try:
            empresa = Empresas(
            user=request.user,
            nome=nome,
            cnpj=cnpj,
            site=site,
            tempo_existencia=tempo_existencia,
            descricao=descricao,
            data_final_captacao=data_final,
            percentual_equity=percentual_equity,
            estagio=estagio,
            area=area,
            publico_alvo=publico_alvo,
            valor=valor,
            pitch=pitch,
            logo=logo
        )
            empresa.save()
            messages.add_message(request, constants.SUCCESS, 'Empresa cadastrada com sucesso')
            return redirect(reverse('cadastrar_empresa'))
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/empresarios/cadastrar_empresa')


@login_required(login_url='logar')
def listar_empresas(request):
    if request.method == "GET":       
        empresas = Empresas.objects.filter(user = request.user)

        # parametro recebido via GET
        empresa = request.GET.get('empresa')
        if empresa:
            empresas = empresas.filter(nome__icontains=empresa)


        return render(request, 'listar_empresas.html', {'empresas':empresas})
    
    

    
def empresa(request, id):
    if request.method == "GET":
        empresa = Empresas.objects.get(id=id)
        documentos = Documento.objects.filter(empresa=empresa)
        metricas = Metricas.objects.filter(empresa=empresa)      
        return render(request, 'empresa.html', {'empresa':empresa, 'documentos':documentos, 'metricas':metricas})
    

def add_doc(request, id):
    
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    arquivo = request.FILES.get('arquivo')
    extencao = arquivo.name.split('.')[-1]

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa empresa não pertence a você')
        return redirect(f'/empresarios/empresa/{id}')

    if not titulo:
        messages.add_message(request, constants.ERROR, 'Título é obrigatório')
        return redirect(f'/empresarios/empresa/{id}')
    
    if not arquivo:
        messages.add_message(request, constants.ERROR, 'Arquivo é obrigatório')
        return redirect(f'/empresarios/empresa/{id}')
    
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 2 MB em bytes

    if arquivo.size > MAX_FILE_SIZE:
        messages.add_message(request, constants.ERROR, 'O arquivo não pode exceder 10 MB.')
        return redirect(f'/empresarios/empresa/{id}')
    

    if extencao not in 'pdf':
        messages.add_message(request, constants.ERROR, 'O arquivo deve ser um PDF')
        return redirect(f'/empresarios/empresa/{id}')

    
    try:
        doc = Documento(empresa=empresa, titulo=titulo, arquivo=arquivo)
        doc.save()
        messages.add_message(request, constants.SUCCESS, 'Documento cadastrado com sucesso')
        return redirect(f'/empresarios/empresa/{id}')
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return redirect(f'/empresarios/empresa/{id}')
    

def delete_doc(request, id):
    doc = Documento.objects.get(id=id)
    empresa = doc.empresa
    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, 'Esse documento não pertence a você')
        return redirect(f'/empresarios/empresa/{empresa.id}')
    
    doc.delete()
    messages.add_message(request, constants.SUCCESS, 'Documento deletado com sucesso')
    return redirect(f'/empresarios/empresa/{empresa.id}')

def add_metrica(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    valor = request.POST.get('valor')

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa empresa não pertence a você')
        return redirect(f'/empresarios/empresa/{id}')
    
    if not titulo:
        messages.add_message(request, constants.ERROR, 'Título é obrigatório')
        return redirect(f'/empresarios/empresa/{id}')
    
    if not valor:
        messages.add_message(request, constants.ERROR, 'Valor é obrigatório')
        return redirect(f'/empresarios/empresa/{id}')
    
    try:
        metrica = Metricas(empresa=empresa, titulo=titulo, valor=valor)
        metrica.save()
        messages.add_message(request, constants.SUCCESS, 'Métrica cadastrada com sucesso')
        return redirect(f'/empresarios/empresa/{id}')
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return redirect(f'/empresarios/empresa/{id}')
    

