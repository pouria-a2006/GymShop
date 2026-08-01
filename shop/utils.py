from django.utils.text import slugify


def generate_unique_slug(model_class, value, instance=None):
    base_slug = slugify(value)
    slug = base_slug
    counter = 1

    queryset = model_class.objects.filter(slug=slug)

    if instance:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

        queryset = model_class.objects.filter(slug=slug)

        if instance:
            queryset = queryset.exclude(pk=instance.pk)

    return slug