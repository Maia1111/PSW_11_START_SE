from django.urls import path
from . import views

urlpatterns = [
    
    path('cadastrar_empresa/', views.cadastrar_empresa, name='cadastrar_empresa'),
    path('listar_empresas/', views.listar_empresas, name='listar_empresas'),
    path('empresa/<int:id>/', views.empresa, name='empresa'),
    path('add_doc/<int:id>/', views.add_doc, name='add_doc'), 
    path('delete_doc/<int:id>/', views.delete_doc, name='delete_doc'),
    path('add_metrica/<int:id>', views.add_metrica, name="add_metrica"),
    


]
