from django.http import JsonResponse
from .models import ExtensionPackage


def extension_package(request):
    package = ExtensionPackage.objects.filter(is_active=True).first()
    if not package:
        return JsonResponse({
            'error': 'No active extension package found.'
        })

    return JsonResponse({
        'name': package.name,
        'version': package.version,
        'description': package.description,
        'zip': package.zip.url,
    })
