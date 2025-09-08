from rest_framework.relations import SlugRelatedField


class CreatableSlugRelatedField(SlugRelatedField):
    def to_internal_value(self, data):
        queryset = self.get_queryset()

        try:
            obj, _ = queryset.get_or_create(**{self.slug_field: data})

            return obj
        except (TypeError, ValueError):
            self.fail('invalid')
