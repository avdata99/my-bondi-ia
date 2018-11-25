from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 250  #FIXME ojo que es el límite de contenedores a dibujar en el mapa
    page_size_query_param = 'page_size'
    max_page_size = 1000